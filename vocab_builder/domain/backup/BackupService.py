import datetime
import os.path
import shutil
import time
from pathlib import Path
from typing import Optional

from vocab_builder.domain.backup.Backup import Backup
from vocab_builder.domain.backup.BackupConfig import BackupConfig
from vocab_builder.domain.settings.SettingsService import SettingsService
from vocab_builder.domain.utils import FileUtils
from vocab_builder.infrastructure import get_db_path


class BackupService:

    def __init__(self, settings_service: SettingsService, db_path = get_db_path()):
        self.__settings_service = settings_service
        self.__db_path = db_path

    def update_backup_enabled(self, backup_enabled: bool) -> None:
        settings = self.__settings_service.get_settings()
        settings.backup_enabled = backup_enabled
        self.__settings_service.update_settings(settings)

    def update_backup_count(self, backup_count: int) -> None:
        settings = self.__settings_service.get_settings()
        settings.backup_count = backup_count
        self.__settings_service.update_settings(settings)

    def update_backup_folder_path(self, backup_folder: str) -> None:
        settings = self.__settings_service.get_settings()
        settings.backup_folder_path = backup_folder
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
        return file_name.startswith(Backup.name_prefix) and file_name.endswith(Backup.name_suffix)

    def run_backup(self, force_run=False) -> Optional[Backup]:
        backup_config = self.get_backup_config()
        if force_run or (backup_config.backup_enabled and self.should_backup_today()):
            return self.__do_run_backup(backup_config)

    def __do_run_backup(self, backup_config: BackupConfig) -> Backup:
        backup_file_name = Backup.name_prefix + self.__get_date_time_str() + Backup.name_suffix
        backup_file_path = os.path.join(backup_config.backup_folder_path, backup_file_name)
        if not os.path.exists(Path(backup_file_path).parent):
            os.makedirs(Path(backup_file_path).parent)
        shutil.copyfile(self.__db_path, backup_file_path + ".tmp")
        os.rename(backup_file_path + ".tmp", backup_file_path)
        self.__remove_extra_backups()
        return Backup(backup_file_path)

    def delete_all_backups(self):
        backup_config = self.get_backup_config()
        FileUtils.remove_all_files_in_dir(backup_config.backup_folder_path)

    def should_backup_today(self) -> bool:
        """Return True if we haven't backed up today yet."""
        backups = self.__sort_by_backup_time_desc(self.get_backups())
        if len(backups) == 0:
            return True
        last_backup = backups[0]
        last_backup_date = last_backup.get_backup_time()
        today = datetime.datetime.today()
        return last_backup_date.day != today.day or last_backup_date.month != today.month or last_backup_date.year != today.year

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