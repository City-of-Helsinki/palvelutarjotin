import datetime
from unittest import mock

import jwt
from authlib.jose.rfc7519.claims import JWTClaims
from django.test import TestCase
from django.test.client import RequestFactory

from palvelutarjotin.oidc import GraphQLApiTokenAuthentication


class TestOIDC(TestCase):
    def setUp(self):
        # Every test needs access to the request factory.
        self.auth_backend = GraphQLApiTokenAuthentication()
        self.id_token_payload = {
            "iss": "https://tunnistamo.test.kuva.hel.ninja/openid",
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

    def test_authenticate(self):
        with mock.patch(
            "helusers.oidc.ApiTokenAuthentication.decode_jwt",
            return_value=JWTClaims(
                jwt.decode(self.encoded_jwt, options={"verify_signature": False}), None
            ),
        ):
            request = RequestFactory().get(
                "/fake-path", HTTP_AUTHORIZATION="Bearer {}".format(self.encoded_jwt),
            )
            user = self.auth_backend.authenticate(request)
            self.assertEqual(user.email, self.id_token_payload["email"])
