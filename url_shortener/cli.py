"""Command-line interface for the URL shortener."""

import sys

from . import config
from .shortener import Shortener
from .storage import BaseStorage, JSONStorage, SQLStorage


def get_storage_from_config() -> BaseStorage:
    """Build the configured storage backend."""
    backend = config.STORAGE_BACKEND.strip().lower()
    if backend == "json":
        return JSONStorage(config.STORAGE_FILE)
    if backend == "sql":
        database_url = config.SQL_DATABASE_URL.strip() or None
        return SQLStorage(db_path=config.SQL_DB_PATH, database_url=database_url)

    raise ValueError("Unsupported STORAGE_BACKEND in config.py. Use 'json' or 'sql'.")


def run_cli(app: Shortener) -> None:
    """Run the interactive CLI loop."""
    print("--- URL Shortener CLI ---")
    menu = "\n1. Shorten URL\n2. Resolve URL\n3. Show Total Count\n4. Exit"

    def print_result(label: str, result: str) -> None:
        if result.startswith("Error:"):
            print(result)
        else:
            print(f"{label}: {result}")

    while True:
        print(menu)
        choice = input("Select an option: ").strip()

        if choice == "1":
            url = input("Enter long URL: ").strip()
            print_result("Shortened", app.shorten(url))
        elif choice == "2":
            url = input("Enter shortened URL: ").strip()
            print_result("Original", app.resolve(url))
        elif choice == "3":
            print(f"Total URLs shortened: {app.get_count()}")
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")


def main() -> None:
    """Entry point for the CLI executable."""
    try:
        storage = get_storage_from_config()
    except ValueError as exc:
        print(str(exc))
        sys.exit(1)

    if not config.BASE_URL.strip():
        print("BASE_URL in config.py must not be empty.")
        sys.exit(1)

    app = Shortener(storage, base_url=config.BASE_URL)
    run_cli(app)
