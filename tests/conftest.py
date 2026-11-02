import os
from pathlib import Path

import pytest

os.environ.setdefault("APP_ENV", "development")
os.environ.setdefault("JWT_SECRET", "test-secret-bingo-multi")


@pytest.fixture()
def client(tmp_path, monkeypatch):
    db_path = tmp_path / "test.db"
    monkeypatch.setenv("DATABASE_PATH", str(db_path))

    import app.config as cfg

    monkeypatch.setattr(cfg, "DATABASE_PATH", Path(db_path))
    monkeypatch.setattr(cfg, "JWT_SECRET", "test-secret-bingo-multi")
    monkeypatch.setattr(cfg, "IS_PRODUCTION", False)

    from app.db import init_db
    from fastapi.testclient import TestClient
    import main

    init_db(Path(db_path))

    with TestClient(main.app) as c:
        yield c
