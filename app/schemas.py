from typing import Literal

from pydantic import BaseModel, Field, field_validator

Role = Literal["admin", "operador"]


def normalize_username(value: str) -> str:
    cleaned = value.strip().lower()
    if not cleaned or len(cleaned) > 32:
        raise ValueError("username inválido")
    allowed = set("abcdefghijklmnopqrstuvwxyz0123456789_-")
    if any(ch not in allowed for ch in cleaned):
        raise ValueError("username solo permite a-z, 0-9, _ y -")
    return cleaned


class LoginRequest(BaseModel):
    username: str
    password: str

    @field_validator("username")
    @classmethod
    def _username(cls, v: str) -> str:
        return normalize_username(v)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: Role
    username: str


class UserCreate(BaseModel):
    username: str
    password: str = Field(min_length=6, max_length=128)
    role: Role = "operador"

    @field_validator("username")
    @classmethod
    def _username(cls, v: str) -> str:
        return normalize_username(v)


class UserUpdate(BaseModel):
    role: Role | None = None
    password: str | None = Field(default=None, min_length=6, max_length=128)
    active: bool | None = None


class UserOut(BaseModel):
    id: int
    username: str
    role: Role
    active: bool


class BingoEstado(BaseModel):
    restantes: int
    salidas: list[int]
    total: int = 90


class ConfigOut(BaseModel):
    modal_seconds: int
    modal_cm: float


class ConfigUpdate(BaseModel):
    modal_seconds: int = Field(ge=1, le=30)
    modal_cm: float = Field(ge=3, le=20)
