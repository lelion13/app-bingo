from fastapi import APIRouter, HTTPException, status

from app.db import get_connection
from app.repositories import users as users_repo
from app.schemas import LoginRequest, TokenResponse
from app.security import create_access_token, verify_password

router = APIRouter(prefix="/auth", tags=["auth"])

_GENERIC_AUTH_ERROR = "Credenciales inválidas"


@router.post("/login", response_model=TokenResponse)
def login(body: LoginRequest) -> TokenResponse:
    with get_connection() as conn:
        user = users_repo.get_by_username(conn, body.username)
        if not user or not user["active"]:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=_GENERIC_AUTH_ERROR,
            )
        if not verify_password(body.password, user["password_hash"]):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=_GENERIC_AUTH_ERROR,
            )
        token = create_access_token(
            user_id=user["id"],
            username=user["username"],
            role=user["role"],
        )
    return TokenResponse(
        access_token=token,
        role=user["role"],
        username=user["username"],
    )
