import os
import sys
import unittest
from pathlib import Path

from PyQt5.QtCore import Qt
from PyQt5.QtTest import QTest
from PyQt5.QtWidgets import QApplication, QListWidgetItem

from tests.utils import get_test_vocab_builder_db
from vocab_builder.domain.backup.Backup import Backup
from vocab_builder.domain.backup.BackupService import BackupService
from vocab_builder.domain.settings.SettingsService import SettingsService
from vocab_builder.domain.utils import FileUtils
from vocab_builder.ui.dialog.settings.backup.BackupTab import BackupTab


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

    def test_should_change_backup_list_when_changing_backup_folder_path(self):
        tmp_dir = FileUtils.create_temp_dir()
        backup_file = self.__add_backup_file(tmp_dir, "20220301110000")
        self.form._backup_path_line_edit.textChanged.emit(tmp_dir)
        self.assertEqual(self.form._backup_list_widget.count(), 1)
        self.assertEqual(self.form._backup_list_widget.item(0).text(), Backup(backup_file).get_backup_name())

        FileUtils.remove_dir_if_exists(tmp_dir)

    def test_should_disable_backup_widgets_when_its_disabled(self):
        self.form._enable_backup_checkbox.stateChanged.emit(Qt.Unchecked)
        self.assertFalse(self.form._backup_path_line_edit.isEnabled())
        self.assertFalse(self.form._backup_count_spin_box.isEnabled())
        self.assertFalse(self.form._backup_list_widget.isEnabled())

    def test_should_enable_backup_widgets_when_starting_up(self):
        self.assertTrue(self.form._backup_path_line_edit.isEnabled())
        self.assertTrue(self.form._backup_count_spin_box.isEnabled())
        self.assertTrue(self.form._backup_list_widget.isEnabled())

    def test_should_enable_backup_widgets_when_its_enabled(self):
        self.form._enable_backup_checkbox.stateChanged.emit(Qt.Checked)
        self.assertTrue(self.form._backup_path_line_edit.isEnabled())
        self.assertTrue(self.form._backup_count_spin_box.isEnabled())

    def test_restore(self):
        original_backup_config = self.backup_service.get_backup_config()
        backup = self.backup_service.run_backup()
        self.form._update_ui()

        # make some changes
        self.backup_service.update_backup_count(original_backup_config.backup_count + 1)

        # restore
        backup_item = self.__get_backup_item(backup)
        QTest.mouseClick(self.form._backup_list_widget.viewport(), Qt.LeftButton,
                         pos=self.form._backup_list_widget.visualItemRect(backup_item).center())
        QTest.mouseClick(self.form._backup_detail_dialog._restore_button, Qt.LeftButton)

        # check
        restored_config = self.backup_service.get_backup_config()
        self.assertEqual(restored_config.backup_count, original_backup_config.backup_count)

    def __create_fake_backups(self, backup_service: BackupService):
        backup_folder_path = backup_service.get_backup_config().backup_folder_path
        self.__add_backup_file(backup_folder_path, "20220501110003")
        self.__add_backup_file(backup_folder_path, "20220501110005")

    def __update_backup_folder_path_to_temp_folder(self, backup_service: BackupService) -> None:
        tempdir = FileUtils.create_temp_dir("anki_vocab_builder_backup")
        backup_service.update_backup_folder_path(tempdir)

    def __add_backup_file(self, backup_folder_path: str, backup_date_time: str) -> str:
        backup_file = os.path.join(backup_folder_path, f"{Backup.name_prefix}{backup_date_time}{Backup.name_suffix}")
        Path(backup_file).touch()
        return backup_file

    def __get_backups_item_from_backup_list_widget(self) -> [QListWidgetItem]:
        res = []
        for i in range(self.form._backup_list_widget.count()):
            res.append(self.form._backup_list_widget.item(i))
        return res

    def __get_backup_item(self, backup: Backup) -> QListWidgetItem:
        items = self.__get_backups_item_from_backup_list_widget()
        for item in items:
            if item.text() == backup.get_backup_name():
                return item
        raise Exception(f"Backup {backup.get_backup_name()} not found")
