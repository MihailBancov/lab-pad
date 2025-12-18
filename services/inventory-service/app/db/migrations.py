from __future__ import annotations

import pathlib
from typing import Iterable

import psycopg

from app.core.config import settings


def _list_migration_files(migrations_dir: pathlib.Path) -> list[pathlib.Path]:
    return sorted([p for p in migrations_dir.glob("*.sql") if p.is_file()])


def _ensure_migrations_table(conn: psycopg.Connection) -> None:
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS schema_migrations (
          version TEXT PRIMARY KEY,
          applied_at TIMESTAMPTZ NOT NULL DEFAULT now()
        );
        """
    )


def _get_applied_versions(conn: psycopg.Connection) -> set[str]:
    rows: Iterable[tuple[str]] = conn.execute("SELECT version FROM schema_migrations;").fetchall()
    return {r[0] for r in rows}


def apply_migrations() -> None:
    migrations_dir = pathlib.Path(__file__).resolve().parent.parent / "migrations"
    migration_files = _list_migration_files(migrations_dir)

    conninfo = settings.database_url.replace("postgresql+psycopg://", "postgresql://")
    with psycopg.connect(conninfo, autocommit=False) as conn:
        _ensure_migrations_table(conn)
        applied = _get_applied_versions(conn)

        for path in migration_files:
            version = path.stem
            if version in applied:
                continue
            sql = path.read_text(encoding="utf-8")
            conn.execute(sql)
            conn.execute("INSERT INTO schema_migrations(version) VALUES (%s)", (version,))

        conn.commit()
