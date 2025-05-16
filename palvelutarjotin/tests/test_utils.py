import pytest

from palvelutarjotin.tests.utils.jwt_utils import is_valid_256_bit_key


@pytest.mark.parametrize(
    "key_string, expected_result",
    [
        (
            "0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef",
            True,
        ),  # Valid key
        (
            "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff",
            True,
        ),  # All Fs
        (
            "0000000000000000000000000000000000000000000000000000000000000000",
            True,
        ),  # All 0s
        (
            "abcdef0123456789abcdef0123456789abcdef0123456789abcdef01234567",
            False,
        ),  # Too short
        (
            "0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef0",
            False,
        ),  # Too long
        (
            "0123456789abcdef0123456789abcdef0123456789abcdeF0123456789abcdef",
            True,
        ),  # Upper and lowercase
        (
            "0123456789abcdefg0123456789abcdef0123456789abcdef0123456789abcde",
            False,
        ),  # Invalid char 'g'
        ("", False),  # Empty string
        ("   ", False),  # Whitespace
        (None, False),  # None
        (12345, False),  # Integer
        ("dda26ea70e53b156594d97b97c1e50c4e0e3687bec29f3463e86764b258dd5b6", True),
    ],
)
def test_is_valid_256_bit_key(key_string, expected_result):
    """Test the is_valid_256_bit_key function with various inputs."""
    result = is_valid_256_bit_key(key_string)
    assert result == expected_result
