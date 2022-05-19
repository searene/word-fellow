from ..settings.Settings import Settings


class BackupConfig:

    def __init__(self, settings: Settings):
        self.backup_enabled = settings.backup_enabled
        self.backup_count = settings.backup_count
        self.backup_folder_path = settings.backup_folder_path

    def __eq__(self, other) -> bool:
        if not isinstance(other, BackupConfig):
            return False
        return self.backup_enabled == other.backup_enabled and self.backup_count == other.backup_count and self.backup_folder_path == other.backup_folder_path