import sys
import unittest

from PyQt5.QtWidgets import QApplication

from tests.utils import get_test_vocab_builder_db
from vocab_builder.domain.settings.SettingsService import SettingsService
from vocab_builder.ui.dialog.settings.BackupTab import BackupTab
from vocab_builder.ui.dialog.settings.SettingsDialog import SettingsDialog


class BackupTabTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.__app = QApplication(sys.argv)

    def setUp(self) -> None:
        self.db = get_test_vocab_builder_db()
        self.settings_service = SettingsService(self.db)
        self.form = BackupTab(self.db)

    def test_show_backup_settings_in_ui(self):
        settings = self.settings_service._get_default_settings()
        self.assertEqual(self.form._enable_backup_checkbox.isChecked(), settings.backup_enabled)
        self.assertEqual(self.form._backup_count_spin_box.value(), settings.backup_count)
        self.assertEqual(self.form._back_path_line_edit.text(), settings.backup_folder_path)