class Backup:

    def __init__(self, backup_name: str, backup_path: str):
        self.backup_name = backup_name
        self.backup_path = backup_path

    def __eq__(self, other):
        if isinstance(other, Backup):
            return self.backup_name == other.backup_name and self.backup_path == other.backup_path
        return False
