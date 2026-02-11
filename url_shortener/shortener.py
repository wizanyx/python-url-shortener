"""Core URL shortening logic."""

import re
from typing import TYPE_CHECKING
from urllib.parse import urlparse, urlunparse

if TYPE_CHECKING:
    from .storage.base_storage import BaseStorage


class Shortener:
    """Create and resolve shortened URLs using a storage backend."""

    URL_REGEX = re.compile(
        r"^https?://"
        r"(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|"
        r"localhost|"
        r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"
        r"(?::\d+)?"
        r"(?:/?|[/?]\S+)$",
        re.IGNORECASE,
    )

    def __init__(
        self, storage: "BaseStorage", base_url: str = "https://myapp.com"
    ) -> None:
        self.storage = storage
        self.alphabet = (
            "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        )
        self.base_url = base_url.rstrip("/")
        # Initial load of existing mappings and counter from storage
        self.mappings, self.counter = self.storage.load_all()
        self.url_to_id = {v: k for k, v in self.mappings.items()}

    def _normalize_long_url(self, url: str) -> str:
        parsed = urlparse(url)
        if parsed.path == "/":
            parsed = parsed._replace(path="")
        return urlunparse(parsed)

    def is_valid_url(self, url: str) -> bool:
        """Validate a URL using a conservative regex check."""
        return self.URL_REGEX.match(url) is not None

    def encode(self, n: int) -> str:
        """Encode an integer into a base62 string."""
        if n == 0:
            return self.alphabet[0]
        arr: list[str] = []
        while n:
            n, rem = divmod(n, 62)
            arr.append(self.alphabet[rem])
        arr.reverse()
        return "".join(arr)

    def shorten(self, long_url: str) -> str:
        """Shorten a URL and return the full short link."""
        normalized_url = self._normalize_long_url(long_url)
        if not self.is_valid_url(normalized_url):
            return "Error: Invalid URL format."

        if normalized_url in self.url_to_id:
            return f"{self.base_url}/{self.url_to_id[normalized_url]}"

        self.counter += 1
        short_id = self.encode(self.counter)

        self.storage.save(short_id, normalized_url)
        self.url_to_id[normalized_url] = short_id
        self.mappings[short_id] = normalized_url

        return f"{self.base_url}/{short_id}"

    def resolve(self, short_url: str) -> str:
        """Resolve a short URL into the original URL."""
        short_id = short_url.split("/")[-1]
        if not short_id:
            return "Error: Shortened URL not found."
        return self.mappings.get(short_id, "Error: Shortened URL not found.")

    def get_count(self) -> int:
        """Return the in-memory total number of URLs shortened."""
        return self.counter
