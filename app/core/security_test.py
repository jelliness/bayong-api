import jwt
import pytest

from app.core.security import create_access_token, decode_access_token, hash_password, verify_password


def test_hash_password_and_verify_roundtrip():
    hashed = hash_password("s3cret-Pass!")

    assert hashed != "s3cret-Pass!"
    assert verify_password("s3cret-Pass!", hashed) is True


def test_verify_password_rejects_wrong_password():
    hashed = hash_password("s3cret-Pass!")

    assert verify_password("wrong-password", hashed) is False


def test_create_and_decode_access_token_roundtrip():
    token = create_access_token(subject="alice", role="admin")

    payload = decode_access_token(token)

    assert payload["sub"] == "alice"
    assert payload["role"] == "admin"


def test_decode_access_token_rejects_expired_token():
    token = create_access_token(subject="alice", role="admin", expires_minutes=-1)

    with pytest.raises(jwt.ExpiredSignatureError):
        decode_access_token(token)


def test_decode_access_token_rejects_garbage_token():
    with pytest.raises(jwt.InvalidTokenError):
        decode_access_token("not-a-real-token")
