import os
import sys
import tempfile
import unittest
from pathlib import Path

from PyQt5.QtWidgets import QApplication

from tests.utils import get_test_vocab_builder_db
from vocab_builder.domain.backup.Backup import Backup
from vocab_builder.domain.backup.BackupService import BackupService
from vocab_builder.domain.settings.SettingsService import SettingsService
from vocab_builder.domain.utils import FileUtils
from vocab_builder.ui.dialog.settings.BackupTab import BackupTab


class BackupTabTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.__app = QApplication(sys.argv)

    def setUp(self) -> None:
        self.db = get_test_vocab_builder_db()
        settings_service = SettingsService(self.db)
        self.backup_service = BackupService(settings_service)
        self.__update_backup_folder_path_to_temp_folder(self.backup_service)
        self.__create_fake_backups(self.backup_service)

        self.form = BackupTab(self.backup_service)

    def tearDown(self) -> None:
        FileUtils.remove_dir_if_exists(self.backup_service.get_backup_config().backup_folder_path)

    def test_show_backup_config(self):
        backup_config = self.backup_service.get_backup_config()
        self.assertEqual(self.form._enable_backup_checkbox.isChecked(), backup_config.backup_enabled)
        self.assertEqual(self.form._backup_count_spin_box.value(), backup_config.backup_count)
        self.assertEqual(self.form._backup_path_line_edit.text(), backup_config.backup_folder_path)

    def test_show_backups(self):
        backups = self.backup_service.get_backups()
        self.assertEqual(self.form._backup_list_widget.count(), len(backups))
        for i in range(len(backups)):
            self.assertEqual(self.form._backup_list_widget.item(i).text(), backups[i].get_backup_name())

    def test_toggle_enable_backup(self):
        backup_config = self.backup_service.get_backup_config()
        self.form._enable_backup_checkbox.setChecked(not backup_config.backup_enabled)

        new_backup_config = self.backup_service.get_backup_config()
        self.assertEqual(new_backup_config.backup_enabled, not backup_config.backup_enabled)

    def test_change_backup_count(self):
        backup_config = self.backup_service.get_backup_config()
        self.form._backup_count_spin_box.setValue(backup_config.backup_count + 2)

        new_backup_config = self.backup_service.get_backup_config()
        self.assertEqual(new_backup_config.backup_count, backup_config.backup_count + 2)

    def test_should_show_backup_list(self):
        backups = self.backup_service.get_backups()
        for i in range(self.form._backup_list_widget.count()):
            self.assertTrue(self.form._backup_list_widget.item(i).text(), backups[i].get_backup_name())

    def __create_fake_backups(self, backup_service: BackupService):
        backup_folder_path = backup_service.get_backup_config().backup_folder_path
        self.__add_backup_file(backup_folder_path, "2022050111000300")
        self.__add_backup_file(backup_folder_path, "2022050111000500")

    def __update_backup_folder_path_to_temp_folder(self, backup_service: BackupService) -> None:
        tempdir = FileUtils.create_temp_dir("anki_vocab_builder_backup")
        backup_service.update_backup_folder_path(tempdir)

    def __add_backup_file(self, backup_folder_path: str, backup_date_time: str) -> str:
        backup_file = os.path.join(backup_folder_path, f"{Backup.name_prefix}{backup_date_time}{Backup.name_suffix}")
        Path(backup_file).touch()
        return backup_file
