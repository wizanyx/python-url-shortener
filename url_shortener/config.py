"""Configuration settings for the URL shortener application."""

from typing import Literal

# STORAGE_BACKEND can be "json" or "sql".
STORAGE_BACKEND: Literal["json", "sql"] = "json"

# Path for JSON storage.
STORAGE_FILE: str = "data/links.json"

# Base URL for generated short links (no trailing slash).
BASE_URL: str = "https://myapp.com"

# SQL settings.
SQL_DB_PATH: str = "data/links.db"
# Use a SQLite URI when you want an explicit database URL.
# Examples: "sqlite:///data/links.db" or "file:data/links.db"
SQL_DATABASE_URL: str = ""
