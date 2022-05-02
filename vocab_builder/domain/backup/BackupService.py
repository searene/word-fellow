import os.path

from vocab_builder.domain.backup.Backup import Backup
from vocab_builder.domain.backup.BackupConfig import BackupConfig
from vocab_builder.domain.settings.SettingsService import SettingsService


class BackupService:

    def __init__(self, settings_service: SettingsService):
        self.__settings_service = settings_service

    def get_backup_config(self) -> BackupConfig:
        return BackupConfig(self.__settings_service.get_settings())

    def get_backups(self) -> [Backup]:
        backup_config = self.get_backup_config()
        if not os.path.exists(backup_config.backup_folder_path):
            return []
        file_names = os.listdir(backup_config.backup_folder_path)
        res = []
        for file_name in file_names:
            if not self.is_backup_file(file_name):
                continue
            file_path = os.path.join(backup_config.backup_folder_path, file_name)
            res.append(Backup(file_name, file_path))
        return res

    def is_backup_file(self, file_name: str) -> bool:
        return file_name.startswith("anki_vocab_builder_backup_")