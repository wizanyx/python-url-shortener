"""JSON file storage backend."""

import json
import os
from typing import TypedDict

from .base_storage import BaseStorage


class StorageData(TypedDict):
    count: int
    mappings: dict[str, str]


class JSONStorage(BaseStorage):
    """Storage implementation that saves URL mappings to a JSON file."""

    def __init__(self, file_path: str = "data/links.json") -> None:
        self.file_path = file_path
        directory = os.path.dirname(self.file_path)
        if directory:
            os.makedirs(directory, exist_ok=True)
        if not os.path.exists(self.file_path):
            with open(self.file_path, "w") as f:
                json.dump({"count": 0, "mappings": {}}, f)

    def load_all(self) -> tuple[dict[str, str], int]:
        with open(self.file_path, "r") as f:
            data: StorageData = json.load(f)
            return data["mappings"], data["count"]

    def save(self, short_id: str, long_url: str) -> None:
        mappings, count = self.load_all()
        mappings[short_id] = long_url
        with open(self.file_path, "w") as f:
            json.dump({"count": count + 1, "mappings": mappings}, f, indent=4)
