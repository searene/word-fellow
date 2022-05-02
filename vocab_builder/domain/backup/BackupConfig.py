from vocab_builder.domain.settings.Settings import Settings


class BackupConfig:

    def __init__(self, settings: Settings):
        self.backup_enabled = settings.backup_enabled
        self.backup_count = settings.backup_count
        self.backup_folder_path = settings.backup_folder_path