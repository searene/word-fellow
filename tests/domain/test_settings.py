import unittest

from tests.utils import get_test_vocab_builder_db
from vocab_builder.domain.settings.Settings import Settings


class SettingsTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.__db = get_test_vocab_builder_db()

    def test_something(self):
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
