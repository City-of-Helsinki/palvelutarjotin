import contextlib
import datetime
import jwt
from authlib.jose.rfc7519.claims import JWTClaims
from django.test import override_settings, TestCase
from django.test.client import RequestFactory
from django.utils import timezone
from freezegun import freeze_time
from unittest import mock

from organisations.factories import UserFactory
from palvelutarjotin.oidc import GraphQLApiTokenAuthentication


@contextlib.contextmanager
def mocked_jwt_request(encoded_jwt):
    with mock.patch(
        "helusers.oidc.ApiTokenAuthentication.decode_jwt",
        return_value=JWTClaims(
            jwt.decode(encoded_jwt, options={"verify_signature": False}), None
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
            "iss": "https://tunnistamo.test.hel.ninja/openid",
            "sub": "sub",
            "aud": "https://api.hel.fi/auth/palvelutarjotin",
            "exp": int(
                (datetime.datetime.utcnow() + datetime.timedelta(seconds=30)).strftime(
                    "%s"
                )
            ),
            "iat": int(datetime.datetime.utcnow().strftime("%s")),
            "auth_time": int(datetime.datetime.utcnow().strftime("%s")),
            "name": "Test Guy",
            "given_name": "Test",
            "family_name": "Guy",
            "nickname": "tester",
            "email": "test.test@test.com",
            "email_verified": False,
            "azp": "https://api.hel.fi/auth/palvelutarjotin-admin",
            "amr": "github",
            "loa": "low",
            "https://api.hel.fi/auth": ["palvelutarjotin"],
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
        UPDATE_LAST_LOGIN={
            "ENABLED": True,
            "UPDATE_INTERVAL_MINUTES": 60,
        }
    )
    def test_authenticate(self):
        """Successful authentication and last_login is set"""
        with mocked_jwt_request(self.encoded_jwt) as request:
            user = self.auth_backend.authenticate(request)
            self.assertEqual(user.email, self.id_token_payload["email"])
            self.assertIsNotNone(user.last_login)

    @override_settings(
        UPDATE_LAST_LOGIN={
            "ENABLED": False,
            "UPDATE_INTERVAL_MINUTES": 60,
        }
    )
    def test_authenticate_with_update_last_login_disabled(self):
        """Last login should not be set, because the feature is disabled."""
        with mocked_jwt_request(self.encoded_jwt) as request:
            user = self.auth_backend.authenticate(request)
            self.assertEqual(user.email, self.id_token_payload["email"])
            self.assertIsNone(user.last_login)

    @override_settings(
        UPDATE_LAST_LOGIN={
            "ENABLED": True,
            "UPDATE_INTERVAL_MINUTES": 60,
        }
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
        UPDATE_LAST_LOGIN={
            "ENABLED": True,
            "UPDATE_INTERVAL_MINUTES": 60,
        }
    )
    @freeze_time("2023-01-18 12:00:00")
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
