import sys
import unittest

from PyQt5.QtWidgets import QApplication

from tests.utils import get_test_vocab_builder_db
from vocab_builder.domain.backup.BackupService import BackupService
from vocab_builder.domain.settings.SettingsService import SettingsService
from vocab_builder.ui.dialog.settings.BackupTab import BackupTab
from vocab_builder.ui.dialog.settings.SettingsDialog import SettingsDialog


class BackupTabTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.__app = QApplication(sys.argv)

    def setUp(self) -> None:
        self.db = get_test_vocab_builder_db()
        settings_service = SettingsService(self.db)
        self.backup_service = BackupService(settings_service)
        self.form = BackupTab(self.backup_service)

    def test_show_backup_settings_in_ui(self):
        backup_config = self.backup_service.get_backup_config()
        self.assertEqual(self.form._enable_backup_checkbox.isChecked(), backup_config.backup_enabled)
        self.assertEqual(self.form._backup_count_spin_box.value(), backup_config.backup_count)
        self.assertEqual(self.form._backup_path_line_edit.text(), backup_config.backup_folder_path)
