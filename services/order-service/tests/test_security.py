import time

import jwt
import pytest
from fastapi import HTTPException


def test_get_current_user_requires_bearer() -> None:
    from app.core.security import get_current_user

    with pytest.raises(HTTPException) as exc:
        get_current_user(authorization=None)
    assert exc.value.status_code == 401


def test_get_current_user_decodes_token() -> None:
    from app.core.config import settings
    from app.core.security import get_current_user

    token = jwt.encode(
        {"sub": "123", "role": "user", "iat": int(time.time()), "exp": int(time.time()) + 60},
        settings.jwt_secret,
        algorithm="HS256",
    )
    user = get_current_user(authorization=f"Bearer {token}")
    assert user["sub"] == "123"
