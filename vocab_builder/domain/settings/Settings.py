from typing import Any, Dict

from vocab_builder.infrastructure import VocabBuilderDB
import json


class Settings:

    def __init__(self, backup_enabled: bool, backup_count: int, backup_folder_path: str):
        self.backup_enabled = backup_enabled
        self.backup_count = backup_count
        self.backup_folder_path = backup_folder_path

    def to_dict(self) -> Dict[str, Any]:
        return {
            "backup_enabled": self.backup_enabled,
            "backup_count": self.backup_count,
            "backup_folder_path": self.backup_folder_path
        }

    def __eq__(self, other):
        if not isinstance(other, Settings):
            return False
        return self.backup_enabled == other.backup_enabled and self.backup_count == other.backup_count and self.backup_folder_path == other.backup_folder_path