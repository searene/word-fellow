import unittest

from tests.base.BaseTestCase import BaseTestCase
from word_fellow.domain.status.GlobalWordStatus import insert_word_status, Status, \
    upsert_word_status


class GlobalWordStatusTestCase(BaseTestCase):
    def setUp(self) -> None:
        super().setUp()

    def tearDown(self) -> None:
        super().tearDown()

    def test_word_should_be_unique(self):
        insert_word_status("test", Status.KNOWN, self.db)
        with self.assertRaises(Exception):
            insert_word_status("test", Status.KNOWN, self.db)

    def test_we_can_call_upsert_with_the_same_word_twice(self):
        upsert_word_status("test", Status.KNOWN, self.db)
        upsert_word_status("test", Status.IGNORED, self.db)


if __name__ == '__main__':
    unittest.main()
