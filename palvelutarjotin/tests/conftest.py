import secrets

import pytest
from django.contrib.auth import get_user_model

from organisations.factories import UserFactory
from palvelutarjotin.tests.utils.jwt_utils import generate_symmetric_test_jwt

User = get_user_model()


@pytest.fixture(autouse=True)
def oidc_browser_test_api_token_auth_settings(settings):
    settings.OIDC_BROWSER_TEST_API_TOKEN_AUTH = {
        "ENABLED": True,
        "AUDIENCE": ["kultus-api-dev", "profile-api-test", "kultus-admin-ui-test"],
        "API_SCOPE_PREFIX": "",
        "REQUIRE_API_SCOPE_FOR_AUTHENTICATION": False,
        "API_AUTHORIZATION_FIELD": "authorization.permissions.scopes",
        "ISSUER": "https://kultus-admin-ui.test.hel.ninja",
        "JWT_SIGN_SECRET": secrets.token_bytes(32).hex(),
    }


@pytest.fixture
def get_browser_test_bearer_token_for_user(oidc_browser_test_api_token_auth_settings):
    """Returns a test JWT token generator function.

    The generator function returns a signed bearer token to authenticate through
    the authentcation made for browser testing."""

    def generate_test_jwt_token(user: User | None = None):
        user = user or UserFactory.build()
        return generate_symmetric_test_jwt(user)

    return generate_test_jwt_token
