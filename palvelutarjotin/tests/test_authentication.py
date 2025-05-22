from contextlib import contextmanager
from datetime import timedelta
from unittest.mock import Mock, patch

import pytest
import requests
from django.contrib.auth.models import AnonymousUser
from django.core.exceptions import ImproperlyConfigured
from django.http import HttpRequest
from django.utils import timezone
from freezegun import freeze_time
from helusers.authz import UserAuthorization
from helusers.jwt import JWT
from helusers.oidc import AuthenticationError
from jose import ExpiredSignatureError, JWTError

from common.tests.utils import assert_match_error_code, assert_permission_denied
from organisations.factories import PersonFactory, UserFactory
from palvelutarjotin.consts import (
    AUTHENTICATION_ERROR,
    AUTHENTICATION_EXPIRED_ERROR,
)
from palvelutarjotin.oidc import BrowserTestAwareJWTAuthentication
from palvelutarjotin.tests.utils.jwt_utils import TEST_JWT_EXP_TIME_IN_SECONDS

KULTUS_IS_BROWSER_TESTING_ENABLED = "palvelutarjotin.oidc.BrowserTestAwareJWTAuthentication.is_browser_testing_jwt_enabled"  # noqa: E501
HELUSERS_AUTHENTICATE = "palvelutarjotin.oidc.RequestJWTAuthentication.authenticate"
KULTUS_AUTHENTICATE = (
    "palvelutarjotin.oidc.BrowserTestAwareJWTAuthentication.authenticate"  # noqa: E501
)
SENTRY_CAPTURE_EXCEPTION = "sentry_sdk.capture_exception"

MY_PROFILE_QUERY = """
query MyProfile {
  myProfile {
    emailAddress
  }
}
"""


@pytest.fixture
def request_factory(get_browser_test_bearer_token_for_user):
    auth_header = get_browser_test_bearer_token_for_user()

    def _request_factory(auth_header=auth_header):
        request = HttpRequest()
        request.headers = {"Authorization": auth_header}
        return request

    return _request_factory


@contextmanager
def set_authenticated_user(user):
    with patch(KULTUS_AUTHENTICATE, return_value=user):
        yield


def graphql_request(live_server, query=MY_PROFILE_QUERY, headers=None):
    return requests.post(
        live_server.url + "/graphql", json={"query": query}, headers=headers
    )


def test_authentication_unauthenticated(live_server):
    with set_authenticated_user(AnonymousUser()):
        with patch(SENTRY_CAPTURE_EXCEPTION) as sentry:
            response = graphql_request(live_server)

            assert_permission_denied(response.json())
            # PermissionDenied should not be sent to Sentry
            sentry.assert_not_called()


def test_authentication_authenticated(live_server):
    person = PersonFactory(email_address="jane.doe@example.com")

    with set_authenticated_user(person.user):
        response = graphql_request(
            live_server, headers={"Authorization": "Bearer something-is-needed"}
        )
        json = response.json()
        assert json["data"]["myProfile"]["emailAddress"] == "jane.doe@example.com"


def test_authentication_error(live_server):
    with patch(SENTRY_CAPTURE_EXCEPTION) as sentry:
        with patch(
            KULTUS_AUTHENTICATE,
            side_effect=AuthenticationError("JWT verification failed."),
        ):
            response = graphql_request(
                live_server, headers={"Authorization": "Bearer something-is-needed"}
            )
            assert_match_error_code(response.json(), AUTHENTICATION_ERROR)
            sentry.assert_called()


def test_authentication_expired_error(live_server):
    with patch(
        KULTUS_IS_BROWSER_TESTING_ENABLED,
        return_value=False,
    ):
        with patch(SENTRY_CAPTURE_EXCEPTION) as sentry:
            with patch(
                HELUSERS_AUTHENTICATE,
                side_effect=ExpiredSignatureError(),
            ):
                response = graphql_request(
                    live_server, headers={"Authorization": "Bearer something-is-needed"}
                )
                assert_match_error_code(response.json(), AUTHENTICATION_EXPIRED_ERROR)
                sentry.assert_not_called()


def test_browser_test_authentication_using_live_server(
    live_server, get_browser_test_bearer_token_for_user
):
    """The test JWT should be valid for authentication."""
    person = PersonFactory(
        email_address="email_from_person@example.org",
        user=UserFactory(email="email_from_user@example.org"),
    )
    response = graphql_request(
        live_server,
        headers={"authorization": get_browser_test_bearer_token_for_user(person.user)},
    )
    json = response.json()
    assert json["data"]["myProfile"]["emailAddress"] == "email_from_user@example.org"


@patch("palvelutarjotin.oidc.helusers_get_or_create_user")
@patch(
    "palvelutarjotin.oidc.BrowserTestAwareJWTAuthentication._validate_symmetrically_signed_jwt"
)
@pytest.mark.django_db()
def test_authenticate_test_user_calls_validate_jwt(
    mock_validate_jwt, mock_helusers_get_or_create_user
):
    """
    The test JWT validation should be called when a test token is used.
    """
    jwt_claims = {"iss": "test_issuer", "sub": "test_user_id"}
    jwt = Mock(spec=JWT, claims=jwt_claims)
    test_user = UserFactory()
    mock_helusers_get_or_create_user.return_value = test_user
    auth = BrowserTestAwareJWTAuthentication()
    result = auth.authenticate_test_user(jwt)
    assert isinstance(result, UserAuthorization)
    assert result.user == test_user
    mock_validate_jwt.assert_called_once_with(jwt)


@patch("palvelutarjotin.oidc.helusers_get_or_create_user")
@patch(
    "palvelutarjotin.oidc.BrowserTestAwareJWTAuthentication._validate_symmetrically_signed_jwt"
)
@pytest.mark.django_db()
def test_authenticate_test_user_result(
    mock_validate_jwt, mock_helusers_get_or_create_user
):
    """
    User & person should be set up correctly after successful test JWT authentication.
    """
    jwt_claims = {
        "iss": "test_issuer",
        "sub": "test_user_id",
        "email": "email_from_jwt_claim@example.org",
        "given_name": "Given name in JWT claim",
        "family_name": "Family name in JWT claim",
    }
    jwt = Mock(spec=JWT, claims=jwt_claims)
    test_user = UserFactory(
        first_name="User first name",
        last_name="User last name",
        email="email_from_user@example.org",
    )
    mock_helusers_get_or_create_user.return_value = test_user
    auth = BrowserTestAwareJWTAuthentication()
    result = auth.authenticate_test_user(jwt)
    assert isinstance(result, UserAuthorization)
    assert result.user == test_user
    assert result.user.first_name == "User first name"
    assert result.user.last_name == "User last name"
    assert result.user.email == "email_from_user@example.org"
    assert result.user.is_active is True
    assert result.user.is_staff is False
    assert result.user.is_event_staff is True
    assert result.user.is_superuser is False
    mock_validate_jwt.assert_called_once_with(jwt)
    assert result.user.person is not None
    assert result.user.person.name == "Given name in JWT claim"
    assert result.user.person.email_address == "email_from_jwt_claim@example.org"

    # Organisations linked to the person should be
    # exactly the ones intended for browser testing
    assert result.user.person.organisations.count() == 3
    org1, org2, org3 = sorted(
        result.user.person.organisations.all(), key=lambda org: org.name
    )

    assert org1.name == "Kulttuurin ja vapaa-ajan toimiala"
    assert org1.type == "provider"
    assert org1.publisher_id == "ahjo:u480400"

    assert org2.name == "Kulttuuripalvelukokonaisuus"
    assert org2.type == "provider"
    assert org2.publisher_id == "ahjo:u48040010"

    assert org3.name == "Kultus"
    assert org3.type == "user"
    assert org3.publisher_id == "kultus:0"


def test_get_auth_header_jwt_valid(request_factory):
    request = request_factory()
    auth = BrowserTestAwareJWTAuthentication()
    jwt = auth._get_auth_header_jwt(request)
    assert isinstance(jwt, JWT)


def test_get_auth_header_jwt_invalid_scheme(request_factory):
    request = request_factory("Basic invalid")
    auth = BrowserTestAwareJWTAuthentication()
    jwt = auth._get_auth_header_jwt(request)
    assert jwt is None


def test_get_auth_header_jwt_invalid_bearer(request_factory):
    request = request_factory("bearer invalid.jwt.structure")
    auth = BrowserTestAwareJWTAuthentication()
    with pytest.raises(JWTError):
        auth._get_auth_header_jwt(request)


def test_get_auth_header_jwt_no_header(request_factory):
    request = request_factory(None)
    auth = BrowserTestAwareJWTAuthentication()
    jwt = auth._get_auth_header_jwt(request)
    assert jwt is None


def test_browser_test_auth_enabled_without_issuer_should_raise(settings):
    """Issuer is a mandatory config when test auth is enabled."""
    settings.OIDC_BROWSER_TEST_API_TOKEN_AUTH["ENABLED"] = True
    settings.OIDC_BROWSER_TEST_API_TOKEN_AUTH["ISSUER"] = None
    with pytest.raises(ImproperlyConfigured):
        BrowserTestAwareJWTAuthentication()


@patch("helusers.oidc.RequestJWTAuthentication.authenticate")
def test_browser_test_auth_disabled_should_always_call_helusers_authenticate(
    mock_helusers_authenticate,
    settings,
    request_factory,
):
    """When browser test authentication is disabled,
    the helusers authentication is used for test JWTs.
    """
    settings.OIDC_BROWSER_TEST_API_TOKEN_AUTH["ENABLED"] = False
    request = request_factory()
    auth = BrowserTestAwareJWTAuthentication()
    auth.authenticate(request)
    mock_helusers_authenticate.assert_called_once_with(request)


@pytest.mark.django_db()
def test_browser_test_auth_with_expired_token(request_factory):
    """Advance time after issuing a JWT so that the AuthenticationError
    is thrown for using an expired token
    """
    datetime_for_expired_token = timezone.now() + timedelta(
        TEST_JWT_EXP_TIME_IN_SECONDS + 1
    )
    # advance time so that the JWT expires
    with freeze_time(datetime_for_expired_token.isoformat()):
        request = request_factory()
        with pytest.raises(AuthenticationError):
            auth = BrowserTestAwareJWTAuthentication()
            auth.authenticate(request)


@pytest.mark.django_db()
def test_browser_test_auth_with_valid_token(request_factory):
    request = request_factory()
    auth = BrowserTestAwareJWTAuthentication()
    assert auth.authenticate(request) is not None
