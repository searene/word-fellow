import sys
import unittest

from PyQt5.QtCore import Qt
from PyQt5.QtTest import QTest
from PyQt5.QtWidgets import QApplication

from tests.utils import get_test_vocab_builder_db, get_test_db_path
from vocab_builder.domain.backup.Backup import Backup
from vocab_builder.domain.backup.BackupService import BackupService
from vocab_builder.domain.settings.SettingsService import SettingsService
from vocab_builder.ui.dialog.settings.backup.BackupDetailDialog import BackupDetailDialog


class BackupDetailDialogTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.__app = QApplication(sys.argv)

    def setUp(self):
        db = get_test_vocab_builder_db()
        settings_service = SettingsService(db)
        self.__backup_service = BackupService(settings_service, db_path=db.db_path)

        self.__backup = self.__backup_service.run_backup(force_run=True)
        self.__form = BackupDetailDialog(None, self.__backup, self.__backup_service, False)

    def test_restore(self) -> None:

        # make some changes
        backup_config = self.__backup_service.get_backup_config()
        self.__backup_service.update_backup_count(backup_config.backup_count + 1)

        # restore
        QTest.mouseClick(self.__form._restore_button, Qt.LeftButton)

        # verify
        new_db = get_test_vocab_builder_db()
        new_settings_service = SettingsService(new_db)
        new_backup_service = BackupService(new_settings_service, db_path=get_test_db_path())
        new_backup_config = new_backup_service.get_backup_config()
        self.assertEqual(new_backup_config, backup_config)


if __name__ == '__main__':
    unittest.main()
