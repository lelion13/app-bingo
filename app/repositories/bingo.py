import json
import random
import sqlite3
from typing import Any


def _fresh_pool() -> list[int]:
    pool = list(range(1, 91))
    random.shuffle(pool)
    return pool


def get_by_user_id(conn: sqlite3.Connection, user_id: int) -> dict[str, Any] | None:
    row = conn.execute(
        "SELECT user_id, disponibles, salidas FROM bingos WHERE user_id = ?",
        (user_id,),
    ).fetchone()
    if not row:
        return None
    return {
        "user_id": row["user_id"],
        "disponibles": json.loads(row["disponibles"]),
        "salidas": json.loads(row["salidas"]),
    }


def get_estado_by_username(conn: sqlite3.Connection, username: str) -> dict[str, Any] | None:
    row = conn.execute(
        """
        SELECT b.disponibles, b.salidas
        FROM bingos b
        JOIN users u ON u.id = b.user_id
        WHERE u.username = ?
        """,
        (username,),
    ).fetchone()
    if not row:
        return None
    disponibles = json.loads(row["disponibles"])
    salidas = json.loads(row["salidas"])
    return {
        "restantes": len(disponibles),
        "salidas": salidas,
        "total": 90,
    }


def reset_bingo(conn: sqlite3.Connection, user_id: int) -> dict[str, Any]:
    pool = _fresh_pool()
    conn.execute(
        """
        UPDATE bingos
        SET disponibles = ?, salidas = ?, updated_at = datetime('now')
        WHERE user_id = ?
        """,
        (json.dumps(pool), json.dumps([]), user_id),
    )
    return {"mensaje": "✅ Bingo (90) iniciado", "total": len(pool)}


def draw_ball(conn: sqlite3.Connection, user_id: int) -> dict[str, Any]:
    bingo = get_by_user_id(conn, user_id)
    if not bingo:
        return {"error": "Bingo no encontrado", "mensaje": "Bingo no encontrado"}
    disponibles: list[int] = bingo["disponibles"]
    salidas: list[int] = bingo["salidas"]
    if not disponibles:
        return {
            "error": "No quedan más bolillas",
            "mensaje": "🎊 ¡Bingo completo!",
        }
    bolilla = disponibles.pop(0)
    salidas.append(bolilla)
    conn.execute(
        """
        UPDATE bingos
        SET disponibles = ?, salidas = ?, updated_at = datetime('now')
        WHERE user_id = ?
        """,
        (json.dumps(disponibles), json.dumps(salidas), user_id),
    )
    return {
        "bolilla": bolilla,
        "restantes": len(disponibles),
        "salidas": salidas,
    }


def estado_for_user(conn: sqlite3.Connection, user_id: int) -> dict[str, Any]:
    bingo = get_by_user_id(conn, user_id)
    if not bingo:
        return {"restantes": 90, "salidas": [], "total": 90}
    return {
        "restantes": len(bingo["disponibles"]),
        "salidas": bingo["salidas"],
        "total": 90,
    }
