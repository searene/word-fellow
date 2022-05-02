from vocab_builder.domain.backup.Backup import Backup
from vocab_builder.domain.backup.BackupConfig import BackupConfig
from vocab_builder.domain.settings.SettingsService import SettingsService


class BackupService:

    def __init__(self, settings_service: SettingsService):
        self.__settings_service = settings_service

    def get_backup_config(self) -> BackupConfig:
        return BackupConfig(self.__settings_service.get_settings())

    def get_backups(self) -> [Backup]:
        pass