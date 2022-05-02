import os
import unittest
import tempfile

from tests.utils import get_test_vocab_builder_db
from vocab_builder.domain.backup.Backup import Backup
from vocab_builder.domain.backup.BackupService import BackupService
from vocab_builder.domain.settings.Settings import Settings
from vocab_builder.domain.settings.SettingsService import SettingsService
from pathlib import Path

from vocab_builder.domain.utils import FileUtils


class BackupTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.__db = get_test_vocab_builder_db()
        self.__settings_service = SettingsService(self.__db)
        self.__settings = Settings(True, 3, os.path.join(tempfile.gettempdir(), "anki_vocab_builder_backup"))
        self.__settings_service.update_settings(self.__settings)
        FileUtils.remove_dir_if_exists(self.__settings.backup_folder_path)
        FileUtils.mkdirs(self.__settings.backup_folder_path)
        self.__backup_file_name1 = "anki_vocab_builder_backup_20220501214903.db"
        self.__backup_file_name2 = "anki_vocab_builder_backup_20220502214950.db"
        self.__add_backup_files(self.__settings.backup_folder_path, [self.__backup_file_name1, self.__backup_file_name2])
        self.__backup_service = BackupService(self.__settings_service)

    def test_get_backups(self):
        # Add an extra file to the backup folder and check that it is not returned
        self.__add_backup_files(self.__settings.backup_folder_path, ["extra_file.db"])

        backups = self.__backup_service.get_backups()

        self.assertEqual(len(backups), 2)
        expected_backup1 = Backup(self.__get_backup_file_path(self.__backup_file_name1))
        expected_backup2 = Backup(self.__get_backup_file_path(self.__backup_file_name2))
        self.assertTrue(expected_backup1 in backups)
        self.assertTrue(expected_backup2 in backups)

    def __add_backup_files(self, backup_folder_path: str, backup_file_names: [str]) -> None:
        for backup_file_name in backup_file_names:
            backup_file_path = os.path.join(backup_folder_path, backup_file_name)
            Path(backup_file_path).touch()

    def __get_backup_file_path(self, backup_file_name: str) -> str:
        return os.path.join(self.__settings.backup_folder_path, backup_file_name)


if __name__ == '__main__':
    unittest.main()
