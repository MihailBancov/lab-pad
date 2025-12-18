import time

import jwt
import pytest
from fastapi import HTTPException


def test_get_current_user_and_require_admin() -> None:
    from app.core.config import settings
    from app.core.security import get_current_user, require_admin

    token = jwt.encode(
        {"sub": "1", "role": "admin", "iat": int(time.time()), "exp": int(time.time()) + 60},
        settings.jwt_secret,
        algorithm="HS256",
    )

    user = get_current_user(authorization=f"Bearer {token}")
    assert user["role"] == "admin"
    assert require_admin(user)["sub"] == "1"

    with pytest.raises(HTTPException) as exc:
        require_admin({"sub": "1", "role": "user"})
    assert exc.value.status_code == 403
