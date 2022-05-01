import unittest

from tests.utils import get_test_vocab_builder_db
from vocab_builder.domain.status.GlobalWordStatus import GlobalWordStatus, insert_word_status, Status


class GlobalWordStatusTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.__db = get_test_vocab_builder_db()
        GlobalWordStatus.init_database(self.__db)

    # TODO test we can call upsert twice on the same word
    def test_word_should_be_unique(self):
        insert_word_status("test", Status.KNOWN, self.__db)
        with self.assertRaises(Exception):
            insert_word_status("test", Status.KNOWN, self.__db)


if __name__ == '__main__':
    unittest.main()
