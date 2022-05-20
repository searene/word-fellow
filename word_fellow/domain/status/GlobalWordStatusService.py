from ...infrastructure import WordFellowDB


class GlobalWordStatusService:

    def __init__(self, db: WordFellowDB):
        self.__db = db

    def init_database(self):
        self.__db.execute("""
        CREATE TABLE IF NOT EXISTS global_word_status (
            id INTEGER PRIMARY KEY,
            word TEXT NOT NULL UNIQUE,
            status TEXT NOT NULL
        )
        """)
