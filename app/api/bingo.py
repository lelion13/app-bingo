from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse

from app.db import get_connection
from app.deps import CurrentUser
from app.repositories import bingo as bingo_repo

router = APIRouter(tags=["bingo"])


@router.get("/iniciar_bingo/")
def iniciar_bingo(user: CurrentUser):
    with get_connection() as conn:
        result = bingo_repo.reset_bingo(conn, user["id"])
    return JSONResponse(result)


@router.get("/sacar_bolilla/")
def sacar_bolilla(user: CurrentUser):
    with get_connection() as conn:
        result = bingo_repo.draw_ball(conn, user["id"])
    return JSONResponse(result)


@router.get("/estado/")
def estado_propio(user: CurrentUser):
    with get_connection() as conn:
        return bingo_repo.estado_for_user(conn, user["id"])


@router.get("/estado/{username}")
def estado_publico(username: str):
    slug = username.strip().lower()
    with get_connection() as conn:
        estado = bingo_repo.get_estado_by_username(conn, slug)
    if estado is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
    return estado
