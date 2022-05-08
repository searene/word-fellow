import os
import sys
import unittest

from PyQt5.QtCore import Qt
from PyQt5.QtTest import QTest
from PyQt5.QtWidgets import QApplication

from tests.base.BaseTestCase import BaseTestCase
from word_fellow.ui.util.DatabaseUtils import get_test_word_fellow_db
from word_fellow.domain.backup.BackupService import BackupService
from word_fellow.domain.settings.SettingsService import SettingsService
from word_fellow.ui.dialog.settings.backup.BackupDetailDialog import BackupDetailDialog


class BackupDetailDialogTestCase(BaseTestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.__app = QApplication(sys.argv)

    def setUp(self):
        super(BackupDetailDialogTestCase, self).setUp()
        settings_service = SettingsService(self.db)
        self.__backup_service = BackupService(settings_service, db_path=self.db.db_path)

        self.__backup = self.__backup_service.run_backup(force_run=True)
        self.__form = BackupDetailDialog(None, self.__backup, self.__backup_service, False)

    def test_restore(self) -> None:

        # make some changes
        backup_config = self.__backup_service.get_backup_config()
        self.__backup_service.update_backup_count(backup_config.backup_count + 1)

        # restore
        QTest.mouseClick(self.__form._restore_button, Qt.LeftButton)

        # verify
        new_db = get_test_word_fellow_db()
        new_settings_service = SettingsService(new_db)
        new_backup_service = BackupService(new_settings_service, db_path=self.db.db_path)
        new_backup_config = new_backup_service.get_backup_config()
        self.assertEqual(new_backup_config, backup_config)

        os.remove(new_db.db_path)


if __name__ == '__main__':
    unittest.main()
