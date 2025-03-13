from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from jose import jwk
from jose.constants import ALGORITHMS


def _build_key(private_pem, public_pem):
    class _Key:
        pass

    key = _Key()
    key.jose_algorithm = ALGORITHMS.RS256
    key.private_key_pem = private_pem
    key.public_key_pem = public_pem
    key.public_key_jwk = jwk.construct(public_pem, key.jose_algorithm).to_dict()

    # Ensure values are strings and not bytes
    for name in ["n", "e"]:
        value = key.public_key_jwk[name]
        if isinstance(value, bytes):
            key.public_key_jwk[name] = value.decode("utf-8")

    return key


def _get_pem_key_pair():
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    pem_private_key = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )
    pem_public_key = private_key.public_key().public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )
    return pem_private_key.decode("utf-8"), pem_public_key.decode("utf-8")


rsa_key = _build_key(*_get_pem_key_pair())
