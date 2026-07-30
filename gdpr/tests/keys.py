from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from jwt.algorithms import RSAAlgorithm


def _build_key(private_pem, public_pem):
    class _Key:
        pass

    key = _Key()
    key.algorithm = "RS256"
    key.private_key_pem = private_pem
    key.public_key_pem = public_pem

    public_key = serialization.load_pem_public_key(public_pem.encode("utf-8"))
    key.public_key_jwk = RSAAlgorithm.to_jwk(public_key, as_dict=True)

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
