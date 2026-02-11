"""Storage backend interfaces and implementations."""

from abc import ABC, abstractmethod


class BaseStorage(ABC):
    """Abstract storage interface for URL mappings."""

    @abstractmethod
    def save(self, short_id: str, long_url: str) -> None:
        """Persist a new mapping to storage."""
        raise NotImplementedError

    @abstractmethod
    def load_all(self) -> tuple[dict[str, str], int]:
        """Return all mappings and the current global counter."""
        raise NotImplementedError
