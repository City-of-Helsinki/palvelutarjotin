import logging
from typing import Optional

from django.conf import settings
from django.contrib.auth.models import update_last_login
from django.core.exceptions import ImproperlyConfigured
from django.utils import timezone
from helusers.authz import UserAuthorization
from helusers.jwt import JWT, ValidationError
from helusers.oidc import (
    ApiTokenAuthentication,
    AuthenticationError,
    RequestJWTAuthentication,
)
from helusers.settings import api_token_auth_settings
from helusers.user_utils import get_or_create_user
from jose import ExpiredSignatureError
from jose import jwt as jose_jwt

from palvelutarjotin.exceptions import AuthenticationExpiredError
from palvelutarjotin.tests.utils.jwt_utils import is_valid_256_bit_key

logger = logging.getLogger(__name__)


class ApiTokenAuthSettings:
    def __init__(self, **entries):
        self.__dict__.update(entries)


class BrowserTestAwareJWTAuthentication(RequestJWTAuthentication):
    def __init__(self):
        super().__init__()
        combined_settings = {
            **api_token_auth_settings._settings,
            **settings.OIDC_BROWSER_TEST_API_TOKEN_AUTH,
        }
        self._api_token_auth_settings = ApiTokenAuthSettings(**combined_settings)
        self.algorithms = ["HS256"]

        if self._api_token_auth_settings.ENABLED:
            if not self._api_token_auth_settings.ISSUER:
                raise ImproperlyConfigured(
                    "ISSUER must be configured when test JWT auth is enabled."
                )
            if not is_valid_256_bit_key(self._api_token_auth_settings.JWT_SIGN_SECRET):
                raise ImproperlyConfigured(
                    "JWT_SIGN_SECRET (JWT secret key) must be 256 bits"
                )

    def _get_auth_header_jwt(self, request) -> Optional[JWT]:
        """
        Extracts a JWT from the request's "Authorization" header.

        Returns the JWT if found and valid, otherwise None.
        """
        auth_header = request.headers.get("Authorization")  # Use .get() for safety

        if not auth_header:
            return None

        try:
            auth_scheme, jwt_value = auth_header.split()
            if auth_scheme.lower() == "bearer":
                return JWT(jwt_value, self._api_token_auth_settings)
        except ValueError:
            # Handle potential errors from splitting the header
            return None

        return None

    def _validate_symmetrically_signed_jwt(self, jwt: JWT):
        """
        Validate a symmetrically signed JWT that is signed by a shared secret.

        NOTE: This function is implemented since the `django_helusers`
        does not verify symmetrically signed JWT that are signed by a shared secret.
        The `helusers` always uses a issuer specific `OIDCConfig` that fetches the
        keys from a server (from a path "/.well-known/openid-configuration").
        """
        logger.debug(
            "Validating a symmetrically signed test JWT",
            extra={"jwt_claims": jwt.claims if jwt else None},
        )
        try:
            jwt.validate_issuer()
        except ValidationError as e:
            raise AuthenticationError(str(e)) from e
        try:
            jose_jwt.decode(
                token=jwt._encoded_jwt,
                key=self._api_token_auth_settings.JWT_SIGN_SECRET,
                audience=jwt.claims.get("aud"),
                issuer=jwt.claims.get("iss"),
                subject=jwt.claims.get("sub"),
                algorithms=self.algorithms,
            )
        except ValidationError as e:
            raise AuthenticationError(str(e)) from e
        except Exception as e:
            raise AuthenticationError(f"JWT verification failed: {e}")

    def has_auth_token_for_testing(self, request) -> Optional[JWT]:
        """Checks whether the request contains a JWT which is
        issued for end-to-end browser testing use only.

        Args:
            request: the request object.

        Returns:
            Optional[JWT]: JWT if it is issued for brower test use. Otherwise None.
        """
        jwt = self._get_auth_header_jwt(request)
        if jwt and jwt.claims.get("iss") in self._api_token_auth_settings.ISSUER:
            return jwt
        return None

    def is_browser_testing_jwt_enabled(self) -> bool:
        return self._api_token_auth_settings.ENABLED

    def authenticate_test_user(self, jwt: JWT) -> UserAuthorization:
        """Authenticates a user with a JWT issued for browser testing.

        Validates the JWT, retrieves or creates the user, and returns a
        UserAuthorization object.
        """
        logger.info("Authenticating with a test JWT!")
        self._validate_symmetrically_signed_jwt(jwt)
        logger.debug(
            "The symmetrically signed JWT was valid.", extra={"jwt_claims": jwt.claims}
        )
        user = get_or_create_user(jwt.claims, oidc=True)
        logger.debug(
            "User authenticated: %s",
            user,
            extra={"user": getattr(user, "__dict__", str(user))},
        )
        return UserAuthorization(user, jwt.claims)

    def authenticate(self, request, **credentials):
        """
        Looks for a JWT from the request's "Authorization" header.
        If the header is not found, or it doesn't contain a JWT, returns None.
        If the header is found and contains a JWT then the JWT gets verified.

        Test whether the JWT is issued for the end-to-end browser test use.
        IF the JWT is for test use, then handle it with `authenticate_test_user`,
        since the `django_helusers` does not support symmetrically signed JWT.

        If verification passes, takes a user's id from the JWT's "sub" claim.
        Creates a User if it doesn't already exist.

        On success returns a UserAuthorization object.

        The authentications raises an AuthenticationError on authentication failure.
        """
        try:
            if self.is_browser_testing_jwt_enabled():
                if jwt := self.has_auth_token_for_testing(request):
                    return self.authenticate_test_user(jwt).user
            user_auth = super().authenticate(request)
            return getattr(user_auth, "user", None)
        except ExpiredSignatureError as e:
            raise AuthenticationExpiredError(e)


class FixTunnistamoMixin:
    def __convert_amr_to_list(self, id_token):
        """
        OIDC's amr validation fails, since Tunnistamo sends the amr as a string
        instead of a list:
        https://github.com/City-of-Helsinki/tunnistamo/commit/a1b434bbbff92466a144f914a98985008d0ea836.

        To fix the claim validation issue, convert the id_token amr to list
        when a string is given.
        """
        if id_token["amr"] and not isinstance(id_token["amr"], list):
            id_token["amr"] = [id_token["amr"]]

    def validate_claims(self, id_token):
        self.__convert_amr_to_list(id_token)
        super().validate_claims(id_token)


class FixLastLoginMixin:
    def update_last_login_after_interval(self, user):
        """
        Update the user object last_login field if enough time has passed.
        The setting UPDATE_LAST_LOGIN["UPDATE_INTERVAL_MINUTES"] determines
        whether or not enough time has passed for update.
        We don't want to update on every request,
        because then there would be too much writes when there are lot of users.
        """
        minutes_since_last_update = None
        if user.last_login:
            minutes_since_last_update = (
                timezone.now() - user.last_login
            ).total_seconds() / 60
        if (
            minutes_since_last_update is None
            or minutes_since_last_update
            > settings.UPDATE_LAST_LOGIN["UPDATE_INTERVAL_MINUTES"]
        ):
            update_last_login(sender=None, user=user)


class GraphQLApiTokenAuthentication(
    FixTunnistamoMixin, FixLastLoginMixin, ApiTokenAuthentication
):
    """
    Custom wrapper for the helusers.oidc.ApiTokenAuthentication backend.
    Needed to make it work with graphql_jwt.middleware.JSONWebTokenMiddleware,
    which in turn calls django.contrib.auth.middleware.AuthenticationMiddleware.
    Authenticate function should:
    1. accept kwargs, or django's auth middleware will not call it
    2. return only the user object, or django's auth middleware will fail
    """

    def authenticate(self, request, **kwargs):
        user_auth_tuple = super().authenticate(request)
        if not user_auth_tuple:
            return None
        user, auth = user_auth_tuple

        if settings.UPDATE_LAST_LOGIN and settings.UPDATE_LAST_LOGIN["ENABLED"]:
            self.update_last_login_after_interval(user)

        return user


class KultusApiTokenAuthentication(FixTunnistamoMixin, ApiTokenAuthentication):
    """
    Custom wrapper for the helusers.oidc.ApiTokenAuthentication backend.
    Implemented to fix Tunnistamo AMR-issue, when needed.
    Tunnistamo is fixed with FixTunnistamoMixin.
    """

    pass
