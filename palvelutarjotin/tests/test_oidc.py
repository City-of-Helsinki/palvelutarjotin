import contextlib
import datetime
from datetime import timedelta
from unittest import mock

import jwt
import pytest
from authlib.jose.rfc7519.claims import JWTClaims
from django.test import override_settings, TestCase
from django.test.client import RequestFactory
from django.utils import timezone
from freezegun import freeze_time

from organisations.factories import UserFactory
from palvelutarjotin.oidc import GraphQLApiTokenAuthentication

# Test settings for OIDC
_TOKEN_AUTH_SETTINGS = {
    "TOKEN_AUTH_REQUIRE_SCOPE_PREFIX": True,
    "TOKEN_AUTH_ACCEPTED_AUDIENCE": "https://api.hel.fi/auth/palvelutarjotin",
    "TOKEN_AUTH_ACCEPTED_SCOPE_PREFIX": "palvelutarjotin",
    "TOKEN_AUTH_AUTHSERVER_URL": "https://tunnistamo.test.hel.ninja/openid",
}
_TOKEN_AUTH_SETTINGS["OIDC_API_TOKEN_AUTH"] = {
    "AUDIENCE": _TOKEN_AUTH_SETTINGS["TOKEN_AUTH_ACCEPTED_AUDIENCE"],
    "ISSUER": _TOKEN_AUTH_SETTINGS["TOKEN_AUTH_AUTHSERVER_URL"],
    "REQUIRE_API_SCOPE_FOR_AUTHENTICATION": _TOKEN_AUTH_SETTINGS[
        "TOKEN_AUTH_REQUIRE_SCOPE_PREFIX"
    ],
    "API_SCOPE_PREFIX": _TOKEN_AUTH_SETTINGS["TOKEN_AUTH_ACCEPTED_SCOPE_PREFIX"],
    "OIDC_CONFIG_EXPIRATION_TIME": 600,
}

_FROZEN_TEST_TIME = timezone.now()


# Freeze time for OIDC tests, so that token expiration/validity checks pass
@pytest.fixture(autouse=True)
def freeze_oidc_test_time():
    with freeze_time(_FROZEN_TEST_TIME):
        yield


@contextlib.contextmanager
def mocked_jwt_request(encoded_jwt):
    with mock.patch(
        "helusers.oidc.ApiTokenAuthentication.decode_jwt",
        return_value=JWTClaims(
            jwt.decode(
                encoded_jwt,
                key="secret",
                options={"verify_signature": True},
                algorithms=["HS256"],
                audience=_TOKEN_AUTH_SETTINGS["TOKEN_AUTH_ACCEPTED_AUDIENCE"],
            ),
            None,
        ),
    ):
        yield RequestFactory().get(
            "/fake-path",
            HTTP_AUTHORIZATION=f"Bearer {encoded_jwt}",
        )


class TestOIDC(TestCase):
    def setUp(self):
        # Every test needs access to the request factory.
        self.auth_backend = GraphQLApiTokenAuthentication()
        self.id_token_payload = {
            "iss": _TOKEN_AUTH_SETTINGS["TOKEN_AUTH_AUTHSERVER_URL"],
            "sub": "sub",
            "aud": _TOKEN_AUTH_SETTINGS["TOKEN_AUTH_ACCEPTED_AUDIENCE"],
            "exp": int((_FROZEN_TEST_TIME + timedelta(seconds=30)).timestamp()),
            "iat": int(_FROZEN_TEST_TIME.timestamp()),
            "auth_time": int(_FROZEN_TEST_TIME.timestamp()),
            "name": "Test Guy",
            "given_name": "Test",
            "family_name": "Guy",
            "nickname": "tester",
            "email": "test.test@test.com",
            "email_verified": False,
            "azp": "https://api.hel.fi/auth/palvelutarjotin-admin",
            "amr": "github",
            "loa": "low",
            "https://api.hel.fi/auth": [
                _TOKEN_AUTH_SETTINGS["TOKEN_AUTH_ACCEPTED_SCOPE_PREFIX"]
            ],
        }
        self.encoded_jwt = jwt.encode(
            self.id_token_payload, "secret", algorithm="HS256"
        )

    @mock.patch("helusers.oidc.ApiTokenAuthentication.validate_claims")
    def test_validate_claims_converts_str_amr(self, mock_super):
        id_token = {
            "amr": "github",
        }
        self.auth_backend.validate_claims(id_token)
        self.assertTrue(mock_super.called)
        self.assertEqual(id_token["amr"], ["github"])

    @mock.patch("helusers.oidc.ApiTokenAuthentication.validate_claims")
    def test_validate_claims_has_no_effect_on_list_amr(self, mock_super):
        id_token = {
            "amr": ["github"],
        }
        self.auth_backend.validate_claims(id_token)
        self.assertTrue(mock_super.called)
        self.assertEqual(id_token["amr"], ["github"])

    @override_settings(
        **_TOKEN_AUTH_SETTINGS,
        UPDATE_LAST_LOGIN={
            "ENABLED": True,
            "UPDATE_INTERVAL_MINUTES": 60,
        },
    )
    def test_authenticate(self):
        """Successful authentication and last_login is set"""
        with mocked_jwt_request(self.encoded_jwt) as request:
            user = self.auth_backend.authenticate(request)
            self.assertEqual(user.email, self.id_token_payload["email"])
            self.assertIsNotNone(user.last_login)

    @override_settings(
        **_TOKEN_AUTH_SETTINGS,
        UPDATE_LAST_LOGIN={
            "ENABLED": False,
            "UPDATE_INTERVAL_MINUTES": 60,
        },
    )
    def test_authenticate_with_update_last_login_disabled(self):
        """Last login should not be set, because the feature is disabled."""
        with mocked_jwt_request(self.encoded_jwt) as request:
            user = self.auth_backend.authenticate(request)
            self.assertEqual(user.email, self.id_token_payload["email"])
            self.assertIsNone(user.last_login)

    @override_settings(
        **_TOKEN_AUTH_SETTINGS,
        UPDATE_LAST_LOGIN={
            "ENABLED": True,
            "UPDATE_INTERVAL_MINUTES": 60,
        },
    )
    def test_update_last_login_before_interval(self):
        """Last login should not be updated, because the interval has not yet passed."""
        last_login = timezone.now() - datetime.timedelta(minutes=50)
        user = UserFactory(last_login=last_login)
        with mocked_jwt_request(self.encoded_jwt) as request:
            with mock.patch(
                "helusers.oidc.ApiTokenAuthentication.authenticate",
                return_value=[user, None],
            ):
                user = self.auth_backend.authenticate(request)
                self.assertEqual(user.last_login, last_login)

    @override_settings(
        **_TOKEN_AUTH_SETTINGS,
        UPDATE_LAST_LOGIN={
            "ENABLED": True,
            "UPDATE_INTERVAL_MINUTES": 60,
        },
    )
    def test_update_last_login_after_interval(self):
        """Last login should be updated, because the interval has passed."""
        login_time = timezone.now()
        last_login = timezone.now() - datetime.timedelta(minutes=70)
        user = UserFactory(last_login=last_login)
        with mocked_jwt_request(self.encoded_jwt) as request:
            with mock.patch(
                "helusers.oidc.ApiTokenAuthentication.authenticate",
                return_value=[user, None],
            ):
                user = self.auth_backend.authenticate(request)
                self.assertEqual(user.last_login, login_time)
