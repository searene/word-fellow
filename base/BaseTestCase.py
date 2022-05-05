import os
import unittest

from tests.utils import get_test_vocab_builder_db


class BaseTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.db = get_test_vocab_builder_db()

    def tearDown(self) -> None:
        os.remove(self.db.db_path)
