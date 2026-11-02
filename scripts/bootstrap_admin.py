#!/usr/bin/env python3
"""One-shot: create the first admin (+ bingo + default config)."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.db import get_connection, init_db
from app.repositories import users as users_repo
from app.schemas import normalize_username


def main() -> int:
    parser = argparse.ArgumentParser(description="Bootstrap first admin user")
    parser.add_argument("--username", required=True)
    parser.add_argument("--password", required=True)
    args = parser.parse_args()

    try:
        username = normalize_username(args.username)
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    if len(args.password) < 6:
        print("Error: password mínimo 6 caracteres", file=sys.stderr)
        return 1

    init_db()
    with get_connection() as conn:
        if users_repo.admin_exists(conn):
            print("Error: ya existe un admin. Abortando.", file=sys.stderr)
            return 1
        if users_repo.get_by_username(conn, username):
            print("Error: el username ya existe.", file=sys.stderr)
            return 1
        user = users_repo.create_user_with_bingo(
            conn,
            username=username,
            password=args.password,
            role="admin",
        )
    print(f"Admin creado: {user['username']} (id={user['id']})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
