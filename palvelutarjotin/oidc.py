from django.conf import settings
from django.contrib.auth.models import update_last_login
from django.utils import timezone
from helusers.oidc import ApiTokenAuthentication


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
