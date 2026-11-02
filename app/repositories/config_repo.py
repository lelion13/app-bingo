import sqlite3
from typing import Any


def get_config(conn: sqlite3.Connection, user_id: int) -> dict[str, Any]:
    row = conn.execute(
        "SELECT modal_seconds, modal_cm FROM configs WHERE user_id = ?",
        (user_id,),
    ).fetchone()
    if not row:
        return {"modal_seconds": 3, "modal_cm": 8.0}
    return {
        "modal_seconds": int(row["modal_seconds"]),
        "modal_cm": float(row["modal_cm"]),
    }


def upsert_config(
    conn: sqlite3.Connection,
    user_id: int,
    *,
    modal_seconds: int,
    modal_cm: float,
) -> dict[str, Any]:
    conn.execute(
        """
        INSERT INTO configs (user_id, modal_seconds, modal_cm)
        VALUES (?, ?, ?)
        ON CONFLICT(user_id) DO UPDATE SET
            modal_seconds = excluded.modal_seconds,
            modal_cm = excluded.modal_cm
        """,
        (user_id, modal_seconds, modal_cm),
    )
    return {"modal_seconds": modal_seconds, "modal_cm": modal_cm}
