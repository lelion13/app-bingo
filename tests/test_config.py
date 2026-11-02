from app.db import get_connection
from app.repositories import users as users_repo


def test_config_persists_per_user(client):
    with get_connection() as conn:
        users_repo.create_user_with_bingo(
            conn, username="cfguser", password="secret12", role="operador"
        )
    login = client.post("/auth/login", json={"username": "cfguser", "password": "secret12"})
    token = login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    put = client.put(
        "/api/config/",
        headers=headers,
        json={"modal_seconds": 7, "modal_cm": 10},
    )
    assert put.status_code == 200
    assert put.json() == {"modal_seconds": 7, "modal_cm": 10.0}

    got = client.get("/api/config/", headers=headers)
    assert got.status_code == 200
    assert got.json()["modal_seconds"] == 7
    assert got.json()["modal_cm"] == 10.0


def test_config_requires_auth(client):
    res = client.get("/api/config/")
    assert res.status_code == 401


def test_visor_public_html(client):
    with get_connection() as conn:
        users_repo.create_user_with_bingo(
            conn, username="viewer", password="secret12", role="operador"
        )
    page = client.get("/visor/viewer")
    assert page.status_code == 200
    assert b"viewer" in page.content

    bare = client.get("/visor")
    assert bare.status_code == 404
