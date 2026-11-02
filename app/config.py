import os
from pathlib import Path

APP_ENV = os.getenv("APP_ENV", "development").lower()
IS_PRODUCTION = APP_ENV in ("production", "prod")

_cors_raw = os.getenv("CORS_ORIGINS", "*").strip()
CORS_ORIGINS = (
    ["*"]
    if _cors_raw == "*"
    else [origin.strip() for origin in _cors_raw.split(",") if origin.strip()]
)

DATABASE_PATH = Path(
    os.getenv("DATABASE_PATH", str(Path(__file__).resolve().parent.parent / "data" / "bingo.db"))
)

JWT_SECRET = os.getenv("JWT_SECRET", "").strip()
JWT_ALGORITHM = "HS256"
JWT_EXPIRE_HOURS = int(os.getenv("JWT_EXPIRE_HOURS", "12"))

# Dev-only fallback; production must set JWT_SECRET.
_DEV_JWT_FALLBACK = "dev-only-change-me-bingo"


def require_jwt_secret() -> str:
    if JWT_SECRET:
        return JWT_SECRET
    if IS_PRODUCTION:
        raise RuntimeError("JWT_SECRET must be set when APP_ENV=production")
    return _DEV_JWT_FALLBACK
