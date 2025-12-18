import pytest


def test_password_hash_and_verify() -> None:
    from app.core.security import hash_password, verify_password

    hashed = hash_password("test123")
    assert isinstance(hashed, str)
    assert verify_password("test123", hashed) is True
    assert verify_password("wrong", hashed) is False


def test_token_roundtrip() -> None:
    from app.core.security import create_access_token, decode_token

    token = create_access_token(sub="1", role="user", expires_in_seconds=60)
    payload = decode_token(token)
    assert payload["sub"] == "1"
    assert payload["role"] == "user"


def test_decode_rejects_invalid_token() -> None:
    from app.core.security import decode_token

    with pytest.raises(Exception):
        decode_token("not-a-jwt")
