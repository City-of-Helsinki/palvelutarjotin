import time
import uuid
from typing import Optional

from django.conf import settings
from django.contrib.auth import get_user_model
from jose import jwt

User = get_user_model()

TEST_JWT_EXP_TIME_IN_SECONDS = 60


def get_epoch_timeframe_for_test_jwt():
    """Get test JWT valid timeframe as epoch times

    Returns:
        tuple[int, int]: issued at (epoch), expiration (epoch)
    """
    epoch_time = int(time.time())
    return epoch_time, epoch_time + TEST_JWT_EXP_TIME_IN_SECONDS


def generate_symmetric_test_jwt(
    user: User,
    shared_secret_for_signature: Optional[str] = None,
    issuer="https://kultus-admin-ui.test.hel.ninja",
    prefix="bearer",
):
    headers = {
        "alg": "HS256",
        "typ": "JWT",
    }
    epoch_time, exp_epoch = get_epoch_timeframe_for_test_jwt()
    payload = {
        "iat": epoch_time,
        "auth_time": epoch_time,
        "exp": exp_epoch,
        "jti": str(uuid.uuid4()),
        "iss": issuer,
        "aud": "kultus-api-test",
        "sub": str(user.uuid),
        "typ": "Bearer",
        "authorization": {"permissions": [{"scopes": ["access"]}]},
        "scope": "profile email",
        "email_verified": False,
        "amr": ["helsinki_tunnus"],
        "name": f"{user.first_name} {user.last_name}",
        "preferred_username": user.username,
        "given_name": user.first_name,
        "family_name": user.last_name,
        "email": user.email,
        "loa": "low",
    }
    token = jwt.encode(
        claims=payload,
        key=shared_secret_for_signature
        or settings.OIDC_BROWSER_TEST_API_TOKEN_AUTH["JWT_SIGN_SECRET"],
        headers=headers,
    )
    return f"{prefix} {token}"


def is_valid_256_bit_key(key):
    """Checks if the provided key is a 256-bit hexadecimal string."""
    return (
        isinstance(key, str)
        and len(key) == 64  # 256-bit key is 64 hexadecimal digits
        and all(c in "0123456789abcdefABCDEF" for c in key)  # Is hexadecimal
    )
