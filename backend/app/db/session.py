import sqlite3
from contextlib import contextmanager
from pathlib import Path

from app.core.config import BACKEND_DIR, settings


def _resolve_db_path() -> Path:
    configured = Path(settings.db_path)
    if configured.is_absolute():
        return configured
    return BACKEND_DIR / configured


def init_db() -> None:
    db_path = _resolve_db_path()
    db_path.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(db_path) as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS usage_logs (
                id TEXT PRIMARY KEY,
                created_at TEXT NOT NULL,
                provider TEXT NOT NULL,
                model TEXT NOT NULL,
                input_tokens INTEGER,
                output_tokens INTEGER,
                total_tokens INTEGER,
                cost_usd REAL,
                message TEXT NOT NULL,
                response TEXT NOT NULL
            )
            """
        )
        _ensure_usage_columns(connection)
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS routing_config (
                id INTEGER PRIMARY KEY CHECK (id = 1),
                config_json TEXT NOT NULL
            )
            """
        )


def _ensure_usage_columns(connection: sqlite3.Connection) -> None:
    columns = {
        row[1] for row in connection.execute("PRAGMA table_info(usage_logs)")
    }
    if "success" not in columns:
        connection.execute("ALTER TABLE usage_logs ADD COLUMN success INTEGER")
    if "latency_ms" not in columns:
        connection.execute("ALTER TABLE usage_logs ADD COLUMN latency_ms REAL")
    if "error_message" not in columns:
        connection.execute("ALTER TABLE usage_logs ADD COLUMN error_message TEXT")


@contextmanager
def get_connection() -> sqlite3.Connection:
    db_path = _resolve_db_path()
    connection = sqlite3.connect(db_path)
    connection.row_factory = sqlite3.Row
    try:
        yield connection
    finally:
        connection.close()
