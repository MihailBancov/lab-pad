from pydantic import BaseModel, EmailStr, field_validator


MAX_BCRYPT_PASSWORD_BYTES = 72


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    role: str = "user"

    @field_validator("password")
    @classmethod
    def _validate_password(cls, value: str) -> str:
        if not value:
            raise ValueError("Password is required")
        if len(value.encode("utf-8")) > MAX_BCRYPT_PASSWORD_BYTES:
            raise ValueError("Password too long (max 72 bytes for bcrypt)")
        return value


class LoginRequest(BaseModel):
    email: EmailStr
    password: str

    @field_validator("password")
    @classmethod
    def _validate_password(cls, value: str) -> str:
        if not value:
            raise ValueError("Password is required")
        if len(value.encode("utf-8")) > MAX_BCRYPT_PASSWORD_BYTES:
            raise ValueError("Password too long (max 72 bytes for bcrypt)")
        return value


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class MeResponse(BaseModel):
    user_id: int
    email: EmailStr
    role: str
