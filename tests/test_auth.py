from app.db import get_connection
from app.repositories import users as users_repo


def _bootstrap_admin(username="admin", password="secret12"):
    with get_connection() as conn:
        return users_repo.create_user_with_bingo(
            conn, username=username, password=password, role="admin"
        )


def test_login_success_and_fail(client):
    _bootstrap_admin()
    ok = client.post("/auth/login", json={"username": "admin", "password": "secret12"})
    assert ok.status_code == 200
    body = ok.json()
    assert "access_token" in body
    assert body["role"] == "admin"
    assert body["username"] == "admin"

    bad = client.post("/auth/login", json={"username": "admin", "password": "wrong"})
    assert bad.status_code == 401
    assert bad.json()["detail"] == "Credenciales inválidas"

    unknown = client.post("/auth/login", json={"username": "nope", "password": "secret12"})
    assert unknown.status_code == 401
    assert unknown.json()["detail"] == "Credenciales inválidas"


def test_deactivated_cannot_login(client):
    admin = _bootstrap_admin()
    with get_connection() as conn:
        users_repo.update_user(conn, admin["id"], active=False)

    res = client.post("/auth/login", json={"username": "admin", "password": "secret12"})
    assert res.status_code == 401


def test_operador_forbidden_on_abm(client):
    _bootstrap_admin()
    login_admin = client.post("/auth/login", json={"username": "admin", "password": "secret12"})
    admin_token = login_admin.json()["access_token"]

    created = client.post(
        "/api/users/",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={"username": "op1", "password": "secret12", "role": "operador"},
    )
    assert created.status_code == 201

    login_op = client.post("/auth/login", json={"username": "op1", "password": "secret12"})
    op_token = login_op.json()["access_token"]

    denied = client.get(
        "/api/users/",
        headers={"Authorization": f"Bearer {op_token}"},
    )
    assert denied.status_code == 403
