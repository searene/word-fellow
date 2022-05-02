import unittest

from tests.utils import get_test_vocab_builder_db
from vocab_builder.domain.settings.Settings import Settings


class SettingsTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.__db = get_test_vocab_builder_db()



if __name__ == '__main__':
    unittest.main()
