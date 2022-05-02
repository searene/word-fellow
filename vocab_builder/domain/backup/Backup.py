from pathlib import Path

class Backup:

    def __init__(self, backup_path: str):
        self.backup_path = backup_path

    def get_backup_name(self) -> str:
        return Path(self.backup_path).name

    def __eq__(self, other):
        if isinstance(other, Backup):
            return self.backup_name == other.backup_name and self.backup_path == other.backup_path
        return False
