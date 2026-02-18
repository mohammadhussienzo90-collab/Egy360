"""
Token encryption utilities using Fernet symmetric encryption.
Uses Django's SECRET_KEY as the encryption key base.
Depends on cryptography>=42.0.0 (already in requirements.txt).
"""
import base64
import hashlib
from cryptography.fernet import Fernet
from django.conf import settings


def _get_fernet_key():
    """Derive a Fernet key from Django's SECRET_KEY."""
    key_bytes = hashlib.sha256(settings.SECRET_KEY.encode()).digest()
    return base64.urlsafe_b64encode(key_bytes)


def encrypt_token(plaintext: str) -> str:
    """Encrypt a token string. Returns base64-encoded ciphertext."""
    if not plaintext:
        return ''
    f = Fernet(_get_fernet_key())
    return f.encrypt(plaintext.encode()).decode()


def decrypt_token(ciphertext: str) -> str:
    """Decrypt a token string. Returns plaintext."""
    if not ciphertext:
        return ''
    f = Fernet(_get_fernet_key())
    return f.decrypt(ciphertext.encode()).decode()
