import json
import random
import sqlite3
from typing import Any

from app.security import hash_password


def _fresh_pool() -> list[int]:
    pool = list(range(1, 91))
    random.shuffle(pool)
    return pool


def get_by_username(conn: sqlite3.Connection, username: str) -> dict[str, Any] | None:
    row = conn.execute(
        "SELECT id, username, password_hash, role, active FROM users WHERE username = ?",
        (username,),
    ).fetchone()
    return dict(row) if row else None


def get_by_id(conn: sqlite3.Connection, user_id: int) -> dict[str, Any] | None:
    row = conn.execute(
        "SELECT id, username, password_hash, role, active FROM users WHERE id = ?",
        (user_id,),
    ).fetchone()
    return dict(row) if row else None


def list_users(conn: sqlite3.Connection) -> list[dict[str, Any]]:
    rows = conn.execute(
        "SELECT id, username, role, active FROM users ORDER BY username"
    ).fetchall()
    return [dict(r) for r in rows]


def admin_exists(conn: sqlite3.Connection) -> bool:
    row = conn.execute(
        "SELECT 1 FROM users WHERE role = 'admin' LIMIT 1"
    ).fetchone()
    return row is not None


def create_user_with_bingo(
    conn: sqlite3.Connection,
    *,
    username: str,
    password: str,
    role: str,
) -> dict[str, Any]:
    password_hash = hash_password(password)
    cur = conn.execute(
        "INSERT INTO users (username, password_hash, role, active) VALUES (?, ?, ?, 1)",
        (username, password_hash, role),
    )
    user_id = int(cur.lastrowid)
    pool = _fresh_pool()
    conn.execute(
        "INSERT INTO bingos (user_id, disponibles, salidas) VALUES (?, ?, ?)",
        (user_id, json.dumps(pool), json.dumps([])),
    )
    conn.execute(
        "INSERT INTO configs (user_id, modal_seconds, modal_cm) VALUES (?, 3, 8.0)",
        (user_id,),
    )
    return {
        "id": user_id,
        "username": username,
        "role": role,
        "active": True,
    }


def update_user(
    conn: sqlite3.Connection,
    user_id: int,
    *,
    role: str | None = None,
    password: str | None = None,
    active: bool | None = None,
) -> dict[str, Any] | None:
    user = get_by_id(conn, user_id)
    if not user:
        return None
    if role is not None:
        conn.execute("UPDATE users SET role = ? WHERE id = ?", (role, user_id))
    if password is not None:
        conn.execute(
            "UPDATE users SET password_hash = ? WHERE id = ?",
            (hash_password(password), user_id),
        )
    if active is not None:
        conn.execute(
            "UPDATE users SET active = ? WHERE id = ?",
            (1 if active else 0, user_id),
        )
    updated = get_by_id(conn, user_id)
    assert updated is not None
    return {
        "id": updated["id"],
        "username": updated["username"],
        "role": updated["role"],
        "active": bool(updated["active"]),
    }
