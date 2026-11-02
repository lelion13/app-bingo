from fastapi import APIRouter, HTTPException, status

from app.db import get_connection
from app.deps import AdminUser
from app.repositories import users as users_repo
from app.schemas import UserCreate, UserOut, UserUpdate

router = APIRouter(prefix="/api/users", tags=["users"])


def _to_out(row: dict) -> UserOut:
    return UserOut(
        id=row["id"],
        username=row["username"],
        role=row["role"],
        active=bool(row["active"]) if not isinstance(row["active"], bool) else row["active"],
    )


@router.get("/", response_model=list[UserOut])
def list_users(_admin: AdminUser) -> list[UserOut]:
    with get_connection() as conn:
        return [_to_out(u) for u in users_repo.list_users(conn)]


@router.post("/", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def create_user(body: UserCreate, _admin: AdminUser) -> UserOut:
    with get_connection() as conn:
        if users_repo.get_by_username(conn, body.username):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="El usuario ya existe",
            )
        created = users_repo.create_user_with_bingo(
            conn,
            username=body.username,
            password=body.password,
            role=body.role,
        )
    return _to_out(created)


@router.patch("/{user_id}", response_model=UserOut)
def update_user(user_id: int, body: UserUpdate, _admin: AdminUser) -> UserOut:
    if body.role is None and body.password is None and body.active is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Nada para actualizar",
        )
    with get_connection() as conn:
        updated = users_repo.update_user(
            conn,
            user_id,
            role=body.role,
            password=body.password,
            active=body.active,
        )
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
    return _to_out(updated)
