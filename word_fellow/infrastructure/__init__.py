import os.path

from word_fellow.infrastructure.WordFellowDB import WordFellowDB


def get_prod_db_path() -> str:
    home_dir = os.path.expanduser("~")
    config_folder = os.path.join(home_dir, ".word-fellow")
    if not os.path.exists(config_folder):
        os.makedirs(config_folder)
    return os.path.join(config_folder, "word-fellow.db")


def create_prod_word_fellow_db() -> WordFellowDB:
    return WordFellowDB(get_prod_db_path())