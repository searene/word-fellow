from typing import Any, Dict

from vocab_builder.infrastructure import VocabBuilderDB
import json


class Settings:

    def __init__(self, enable_backup: bool, backup_count: int, backup_folder_path: str):
        self.__enable_backup = enable_backup
        self.__backup_count = backup_count
        self.__backup_folder_path = backup_folder_path

    def to_dict(self) -> Dict[str, Any]:
        return {
            "enable_backup": self.__enable_backup,
            "backup_count": self.__backup_count,
            "backup_folder_path": self.__backup_folder_path
        }

    def __eq__(self, other):
        if not isinstance(other, Settings):
            return False
        return self.__enable_backup == other.__enable_backup and self.__backup_count == other.__backup_count and self.__backup_folder_path == other.__backup_folder_path