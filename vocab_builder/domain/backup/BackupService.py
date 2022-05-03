import datetime
import os.path
import shutil

from vocab_builder.domain.backup.Backup import Backup
from vocab_builder.domain.backup.BackupConfig import BackupConfig
from vocab_builder.domain.settings.SettingsService import SettingsService
from vocab_builder.domain.utils import FileUtils


class BackupService:

    def __init__(self, settings_service: SettingsService):
        self.__settings_service = settings_service

    def update_backup_enabled(self, backup_enabled: bool) -> None:
        settings = self.__settings_service.get_settings()
        settings.backup_enabled = backup_enabled
        self.__settings_service.update_settings(settings)

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
            res.append(Backup(file_path))
        return res

    def is_backup_file(self, file_name: str) -> bool:
        return file_name.startswith("anki_vocab_builder_backup_")

    def run_backup(self, db_path: str) -> Backup:
        backup_config = self.get_backup_config()
        backup_file_name = Backup.name_prefix + self.__get_date_time_str() + Backup.name_suffix
        backup_file_path = os.path.join(backup_config.backup_folder_path, backup_file_name)
        shutil.copyfile(db_path, backup_file_path)
        self.__remove_extra_backups()
        return Backup(backup_file_path)

    def restore(self, backup: Backup, db_path: str) -> None:
        db_dir = os.path.dirname(db_path)
        target_backup_path = os.path.join(db_dir, backup.get_backup_file_name())
        shutil.copyfile(backup.backup_path, target_backup_path)
        os.remove(db_path)
        os.rename(target_backup_path, db_path)

    def __remove_extra_backups(self) -> None:
        backups = self.__sort_by_backup_time_desc(self.get_backups())
        backup_config = self.get_backup_config()
        for i in range(backup_config.backup_count, len(backups)):
            os.remove(backups[i].backup_path)

    def __sort_by_backup_time_desc(self, backups: [Backup]) -> [Backup]:
        return sorted(backups, key=lambda backup: backup.get_backup_time(), reverse=True)

    def __get_date_time_str(self) -> str:
        now = datetime.datetime.now()
        return now.strftime("%Y%m%d%H%M%S")