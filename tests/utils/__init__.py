import os
import tempfile

from word_fellow.domain.utils import init_database
from word_fellow.infrastructure.WordFellowDB import WordFellowDB


def get_test_word_fellow_db() -> WordFellowDB:
    db = WordFellowDB(get_test_db_path())
    init_database(db)
    return db


def get_test_db_path() -> str:
    config_folder = tempfile.mkdtemp()
    if not os.path.exists(config_folder):
        os.makedirs(config_folder)
    return os.path.join(config_folder, "word-fellow.db")
