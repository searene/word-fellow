from datetime import datetime
from pathlib import Path


class Backup:
    name_prefix = "anki_vocab_builder_backup_"
    name_suffix = ".db"

    def __init__(self, backup_path: str):
        self.backup_path = backup_path

    def get_backup_file_name(self) -> str:
        return Path(self.backup_path).name

    def get_backup_name(self) -> str:
        return Path(self.backup_path).name

    def get_backup_time(self) -> datetime:
        """Get backup time from backup name"""
        date_time_str = self.get_backup_name()[len(self.name_prefix):-len(self.name_suffix)]
        return datetime.strptime(date_time_str, "%Y%m%d%H%M%S")

    def __eq__(self, other):
        if isinstance(other, Backup):
            return self.backup_path == other.backup_path
        return False
