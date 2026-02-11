"""SQLite storage backend."""

import os
import sqlite3

from .base_storage import BaseStorage


class SQLStorage(BaseStorage):
    """Storage implementation that saves URL mappings in a SQLite database."""

    def __init__(
        self, db_path: str = "data/links.db", database_url: str | None = None
    ) -> None:
        self.db_path = db_path
        self.database_url = database_url
        if self.database_url is None:
            directory = os.path.dirname(self.db_path)
            if directory:
                os.makedirs(directory, exist_ok=True)
        self._create_table()

    def _connect(self) -> sqlite3.Connection:
        """Create a SQLite connection from configured settings."""
        if self.database_url is None:
            return sqlite3.connect(self.db_path)
        if self.database_url.startswith("sqlite://") or self.database_url.startswith(
            "file:"
        ):
            return sqlite3.connect(self.database_url, uri=True)
        raise ValueError(
            "Only SQLite URLs are supported (sqlite:///path.db or file:path.db)."
        )

    def _create_table(self) -> None:
        """Ensure the database schema exists."""
        with self._connect() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS urls (
                    short_id TEXT PRIMARY KEY,
                    long_url TEXT UNIQUE
                )
            """)

    def load_all(self) -> tuple[dict[str, str], int]:
        with self._connect() as conn:
            cursor = conn.execute("SELECT short_id, long_url FROM urls")
            mappings = {row[0]: row[1] for row in cursor.fetchall()}
            return mappings, len(mappings)

    def save(self, short_id: str, long_url: str) -> None:
        with self._connect() as conn:
            conn.execute(
                "INSERT INTO urls (short_id, long_url) VALUES (?, ?)",
                (short_id, long_url),
            )
