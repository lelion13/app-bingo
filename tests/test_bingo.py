from app.db import get_connection
from app.repositories import users as users_repo


def _create(username, password="secret12", role="operador"):
    with get_connection() as conn:
        return users_repo.create_user_with_bingo(
            conn, username=username, password=password, role=role
        )


def _token(client, username, password="secret12"):
    res = client.post("/auth/login", json={"username": username, "password": password})
    assert res.status_code == 200
    return res.json()["access_token"]


def test_bingo_isolation_and_public_estado(client):
    _create("alice", role="operador")
    _create("bob", role="operador")
    ta = _token(client, "alice")
    tb = _token(client, "bob")

    draw_a = client.get("/sacar_bolilla/", headers={"Authorization": f"Bearer {ta}"})
    assert draw_a.status_code == 200
    ball_a = draw_a.json()["bolilla"]

    estado_b = client.get("/estado/bob")
    assert estado_b.status_code == 200
    assert estado_b.json()["salidas"] == []

    estado_a = client.get("/estado/alice")
    assert estado_a.status_code == 200
    assert estado_a.json()["salidas"] == [ball_a]

    own_b = client.get("/estado/", headers={"Authorization": f"Bearer {tb}"})
    assert own_b.json()["salidas"] == []


def test_estado_unknown_user_404(client):
    res = client.get("/estado/nadie")
    assert res.status_code == 404


def test_draw_requires_jwt(client):
    res = client.get("/sacar_bolilla/")
    assert res.status_code == 401


def test_restart_keeps_state(client, tmp_path, monkeypatch):
    """Same DB file keeps salidas after re-init schema (idempotent)."""
    from pathlib import Path
    import app.config as cfg
    from app.db import init_db

    _create("carol")
    token = _token(client, "carol")
    drawn = client.get("/sacar_bolilla/", headers={"Authorization": f"Bearer {token}"})
    ball = drawn.json()["bolilla"]

    init_db(Path(cfg.DATABASE_PATH))
    estado = client.get("/estado/carol")
    assert estado.json()["salidas"] == [ball]
