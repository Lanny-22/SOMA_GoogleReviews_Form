import sqlite3
from datetime import datetime, timezone
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "data" / "submissions.db"


def _connect() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    with _connect() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS submissions (
                token TEXT PRIMARY KEY,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                created_at TEXT NOT NULL,
                claimed_at TEXT
            )
            """
        )


def email_exists(email: str) -> bool:
    with _connect() as conn:
        row = conn.execute(
            "SELECT 1 FROM submissions WHERE lower(email) = lower(?)",
            (email.strip(),),
        ).fetchone()
    return row is not None


def create_submission(
    token: str,
    first_name: str,
    last_name: str,
    email: str,
) -> None:
    now = datetime.now(timezone.utc).isoformat()
    with _connect() as conn:
        conn.execute(
            """
            INSERT INTO submissions (token, first_name, last_name, email, created_at)
            VALUES (?, ?, ?, ?, ?)
            """,
            (token, first_name.strip(), last_name.strip(), email.strip().lower(), now),
        )


def get_submission(token: str) -> sqlite3.Row | None:
    with _connect() as conn:
        return conn.execute(
            "SELECT * FROM submissions WHERE token = ?",
            (token.strip(),),
        ).fetchone()


def mark_claimed(token: str) -> None:
    now = datetime.now(timezone.utc).isoformat()
    with _connect() as conn:
        conn.execute(
            "UPDATE submissions SET claimed_at = ? WHERE token = ?",
            (now, token.strip()),
        )
