import os
import tempfile

from word_fellow.domain.utils import init_database
from word_fellow.infrastructure import create_prod_word_fellow_db, WordFellowDB


def get_prod_word_fellow_db() -> WordFellowDB:
    return create_prod_word_fellow_db()


def get_test_word_fellow_db() -> WordFellowDB:

    def get_test_db_path() -> str:
        config_folder = tempfile.mkdtemp()
        if not os.path.exists(config_folder):
            os.makedirs(config_folder)
        return os.path.join(config_folder, "word-fellow.db")

    db = WordFellowDB(get_test_db_path())
    init_database(db)
    return db
