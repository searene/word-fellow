import os
import unittest

from word_fellow.ui.util.DatabaseUtils import get_test_word_fellow_db


class BaseTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.db = get_test_word_fellow_db()

    def tearDown(self) -> None:
        self.db.destroy()
