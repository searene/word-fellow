import os
import tempfile
import unittest
from datetime import datetime

from base.BaseTestCase import BaseTestCase
from word_fellow.domain.backup.Backup import Backup
from word_fellow.domain.backup.BackupService import BackupService
from word_fellow.domain.settings.Settings import Settings
from word_fellow.domain.settings.SettingsService import SettingsService
from word_fellow.domain.utils import FileUtils


class BackupTestCase(BaseTestCase):

    def setUp(self) -> None:
        super().setUp()
        self.__settings_service = SettingsService(self.db)
        self.__settings = Settings(True, 3, os.path.join(tempfile.gettempdir(), "word_fellow_backup"))
        self.__settings_service.update_settings(self.__settings)
        FileUtils.remove_dir_if_exists(self.__settings.backup_folder_path)
        FileUtils.mkdirs(self.__settings.backup_folder_path)
        self.__backup_file_name1 = "word_fellow_backup_20220501214903.db"
        self.__backup_file_name2 = "word_fellow_backup_20220502214950.db"
        self.__add_backup_files(self.__settings.backup_folder_path, [self.__backup_file_name1, self.__backup_file_name2])
        db_path = self.__create_test_db_file("contents1")
        self.__backup_service = BackupService(self.__settings_service, db_path)

    def tearDown(self) -> None:
        super().setUp()
        FileUtils.remove_dir_if_exists(self.__settings.backup_folder_path)

    def test_get_backups(self):
        # Add an extra file to the backup folder and check that it is not returned
        self.__add_backup_files(self.__settings.backup_folder_path, ["extra_file.db"])

        backups = self.__backup_service.get_backups()

        self.assertEqual(len(backups), 2)
        expected_backup1 = Backup(self.__get_backup_file_path(self.__backup_file_name1))
        expected_backup2 = Backup(self.__get_backup_file_path(self.__backup_file_name2))
        self.assertTrue(expected_backup1 in backups)
        self.assertTrue(expected_backup2 in backups)

    def test_restore(self):
        backup = self.__backup_service.run_backup()
        db_path = self.__create_test_db_file("contents2")
        self.__backup_service.restore(backup)
        self.assertTrue(os.path.exists(db_path))
        with open(db_path, 'r') as f:
            self.assertEqual(f.read(), "contents1")

    def test_should_create_new_backup_file_when_the_number_of_backups_is_less_than_backup_count(self):
        backup = self.__backup_service.run_backup()
        self.assertTrue(backup.backup_path.startswith(self.__settings.backup_folder_path))
        self.assertTrue(os.path.exists(backup.backup_path))

    def test_should_remove_oldest_backup_file_when_the_number_of_backups_is_equal_to_backup_count(self):
        self.__settings.backup_count = 2
        self.__settings_service.update_settings(self.__settings)
        backup = self.__backup_service.run_backup()

        backups = self.__backup_service.get_backups()
        self.assertEqual(len(backups), 2)
        self.assertTrue(backup in backups)

    def test_should_backup_if_we_have_not_backed_up_today(self):
        should_backup = self.__backup_service.should_backup_today()

        self.assertTrue(should_backup)

    def test_should_not_backup_if_we_have_backed_up_today(self):
        self.__add_backup_files(self.__settings.backup_folder_path, [f"{Backup.name_prefix}{datetime.now().strftime('%Y%m%d%H%M%S')}.db"])

        should_backup = self.__backup_service.should_backup_today()

        self.assertFalse(should_backup)

    def __add_backup_files(self, backup_folder_path: str, backup_file_names: [str]) -> None:
        for backup_file_name in backup_file_names:
            backup_file_path = os.path.join(backup_folder_path, backup_file_name)
            with open(backup_file_path, 'w') as f:
                f.write(backup_file_name)

    def __get_backup_file_path(self, backup_file_name: str) -> str:
        return os.path.join(self.__settings.backup_folder_path, backup_file_name)

    def __create_test_db_file(self, test_file_contents: str) -> str:
        """Create an empty db file and return its absolute path."""
        db_file_path = os.path.join(tempfile.gettempdir(), "word-fellow.db")
        with open(db_file_path, 'w') as f:
            f.write(test_file_contents)
        return db_file_path


if __name__ == '__main__':
    unittest.main()
