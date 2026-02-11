# Python URL Shortener

A small, local URL shortener with JSON or SQLite storage and a simple CLI.

## Features

- Shorten and resolve URLs from the terminal
- JSON file storage for quick local use
- SQLite storage for a more durable local database
- Config-driven setup

## Project Layout

- url_shortener/cli.py: CLI entry point
- url_shortener/shortener.py: core shortening logic
- url_shortener/config.py: configuration values
- url_shortener/storage/: storage backends

## Configuration

Update settings in url_shortener/config.py:

- STORAGE_BACKEND: "json" or "sql"
- STORAGE_FILE: JSON file path when using JSON storage
- BASE_URL: base URL for generated short links
- SQL_DB_PATH: SQLite file path when using SQL storage
- SQL_DATABASE_URL: SQLite URI (optional)

## Run

Option A (no install):

```bash
python -m url_shortener
```

Option B (installed CLI):

```bash
pip install -e .
url-shortener
```

## Storage Notes

- JSON storage writes to STORAGE_FILE and keeps a simple counter in that file.
- SQLite storage uses SQL_DB_PATH or SQL_DATABASE_URL (SQLite only).

## Development

This project has no third-party runtime dependencies.

### Dev Install

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
```
