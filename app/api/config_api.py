from fastapi import APIRouter

from app.db import get_connection
from app.deps import CurrentUser
from app.repositories import config_repo
from app.schemas import ConfigOut, ConfigUpdate

router = APIRouter(prefix="/api/config", tags=["config"])


@router.get("/", response_model=ConfigOut)
def get_config(user: CurrentUser) -> ConfigOut:
    with get_connection() as conn:
        data = config_repo.get_config(conn, user["id"])
    return ConfigOut(**data)


@router.put("/", response_model=ConfigOut)
def put_config(body: ConfigUpdate, user: CurrentUser) -> ConfigOut:
    rounded_cm = round(float(body.modal_cm) * 10) / 10
    with get_connection() as conn:
        data = config_repo.upsert_config(
            conn,
            user["id"],
            modal_seconds=int(body.modal_seconds),
            modal_cm=rounded_cm,
        )
    return ConfigOut(**data)
