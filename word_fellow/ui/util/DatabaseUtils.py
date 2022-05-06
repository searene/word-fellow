from word_fellow.infrastructure import create_prod_word_fellow_db, WordFellowDB


def get_prod_word_fellow_db() -> WordFellowDB:
    return create_prod_word_fellow_db()
