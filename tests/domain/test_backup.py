import os
import unittest
from datetime import datetime

from word_fellow.domain.backup.Backup import Backup


class BackupTestCase(unittest.TestCase):

    def setUp(self):
        self.backup_name = "word_fellow_backup_20220501110003.db"
        self.backup = Backup(os.path.join("/tmp", self.backup_name))

    def test_get_backup_name(self):
        self.assertEqual(self.backup.get_backup_name(), self.backup_name)

    def test_get_backup_time(self):
        self.assertEqual(self.backup.get_backup_time(), datetime(2022, 5, 1, 11, 0, 3))
