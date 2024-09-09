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
    """Get a PEM-key pair.

    NOTE: Follow the following instructions to create a new pair of PEM keys.

    You can install ``cryptography`` with ``pip``:
    - ``pip install cryptography``

    The following script can be used to create a new pair of PEM keys.

    >>> # doctest: +SKIP
    ... from cryptography.hazmat.primitives.asymmetric import rsa
    ... from cryptography.hazmat.primitives import serialization
    ...
    ... private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    ... pem_private_key = private_key.private_bytes(
    ...     encoding=serialization.Encoding.PEM,
    ...     format=serialization.PrivateFormat.PKCS8,
    ...     encryption_algorithm=serialization.NoEncryption(),
    ... )
    ... pem_public_key = private_key.public_key().public_bytes(
    ...     encoding=serialization.Encoding.PEM,
    ...     format=serialization.PublicFormat.SubjectPublicKeyInfo,
    ... )
    ... print(pem_private_key.decode("utf-8"))
    ... print(pem_public_key.decode("utf-8"))
    """
    return (
        """-----BEGIN PRIVATE KEY-----
MIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQC/2Fgt2rRchA7t
GP6FG3t9bcbQLPlZa3XEFTndv/snAaUBlP8rDiTvoToymNV82prOheYTdmN/sLP4
a9c6nMcbilQjhkHGDZKxC9lOCakd4qL0iyfRO30IL7M5sX/sZP0tnAAOohEY1ljB
MjNNmp45jIZE9LD0/fZ9pM1lv3BzURkKt/Diww8H9EfPG6Y5z44TYO0kfATUBF2z
IZAJzgHAiIWS8BJ2lyidGGi2+Gx4K7f5fFmotjwMPYORiqbwpgSshVefUapedvJC
VFGKPY6f+Beb6PzLE4kEK8+/ctnRdZt2pgbRrom776gUdg59OKL60EL5LExpb/kA
DtRto/txAgMBAAECggEAMa9JHw8OOQumhfc8K6Lzd4ePvuh255ayGEdbBjgrRm3h
myhIcZEnNbxuwx3b5IsFHsmEzbOSj0ZnRcZAJpjl5BcONWkW7cEkJaAo9lIAL5I7
m9PSSxj6B7260A1NUR7ShxZo2WFVxjX1JIvox4dsxQDE4WTx03FWfjHJVDmhWOvL
L0DRjXgTrYj1dBBEnUAWwkIlFDNFzqAVsiZHF+6XOuRUT+vEZPv02IkmUrn3uwos
mBELDelOqL/m5t7EYkxW7apTuGXoxc8NOctDj10+OVcus0Kia8v1REJpkL2hF+AB
gnAQSI8x6OeWjFOZuhUEUsSZLARnkT/K9EFxM4IOsQKBgQD8Ek5/SCAAUT7CFtmM
MdZFpQ0I9ZjywtyrTZFY1g405HpGvzc+sBxu3+K1TPPO+GDz+zmHspaVKFw+4W6J
i8oO6hf1H9N16xR+EqTMosSDX3ud8P1Awswu2TUdNMbCzqx2ICZauLjY1ArZnuPI
BaJMwTY1z12wlZSgB8Gc7wIETQKBgQDC1cBp+5/yvbKoI2kUl/GABVaCumW7ieTz
Yog31RwLR6mvef5LNFomONvDrNxKxSEHj3fo409ZoqNzArVGz3A0iK/CHKVjKpUp
YMXOYMWBOHidC5D0wI3sb/UGoDj7CjCboBvvHbBCB+RVA5atuodLDUoshrVSNrgQ
28JQBR81tQKBgQCHTqBaTHH5GaNxdeiDC8F0EvvjQko+jYD8Zx/NKuHnXHmSflP+
T3SDw6QjI9J/1+3bKZChGakhGdAiZMn8BVCKHviLOPE+i9itL/7MZdbMmjV1+4VF
/QqzXx7WtZy3t071/Z349s0qfu/wDw1AMl4Di3c4/T3SawijumYggl93xQKBgDjs
EDImlJ1rtKWQ6uNcXO8lIBhDcvNunxhIYjnFplLZVgbxYk0Ad5IRLIunlhi2LScz
UDoXJxit/ojccq/EbSi8AnV4vw0Q5NFY95GLDkjpgbuIJIqNMymvr+uGpf8aBAeD
qIWcq+EuwxPfX4dUJrDTqicGGDVzzSUHv2Z3iJ29AoGBAK/8kuvvz7fl7nvR80zG
xv4qkLETZPmGcssma1TskdNn8eYADcDgnnzI3Lldr6DoouGQ8eKNOUQC6X53GU12
0k/+6od92VNGkQI8g7DCPwPC8cTPvvUGFkxg3J8v2nBcaLMmDVUaXrDfj+QG+jUB
MG7YFa0LPJ8R79pFieleUm1O
-----END PRIVATE KEY-----""",
        """-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAv9hYLdq0XIQO7Rj+hRt7
fW3G0Cz5WWt1xBU53b/7JwGlAZT/Kw4k76E6MpjVfNqazoXmE3Zjf7Cz+GvXOpzH
G4pUI4ZBxg2SsQvZTgmpHeKi9Isn0Tt9CC+zObF/7GT9LZwADqIRGNZYwTIzTZqe
OYyGRPSw9P32faTNZb9wc1EZCrfw4sMPB/RHzxumOc+OE2DtJHwE1ARdsyGQCc4B
wIiFkvASdpconRhotvhseCu3+XxZqLY8DD2DkYqm8KYErIVXn1GqXnbyQlRRij2O
n/gXm+j8yxOJBCvPv3LZ0XWbdqYG0a6Ju++oFHYOfTii+tBC+SxMaW/5AA7UbaP7
cQIDAQAB
-----END PUBLIC KEY-----""",
    )


rsa_key = _build_key(*_get_pem_key_pair())
