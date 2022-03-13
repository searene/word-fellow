import enum

from vocab_builder.infrastructure import VocabBuilderDB


class Status(enum.Enum):
    KNOWN = "KNOWN",
    STUDYING = "STUDYING"


class GlobalWordStatus:
    """
    A class to record each word's status, regardless which document it belongs to.
    """
    def __init__(self, word: str, global_status: Status):
        """
        Parameters
        ----------
            word: a word
            global_status: The word's status
        """
        self.word = word
        self.global_status = global_status

    @staticmethod
    def init_database(db: VocabBuilderDB):
        db.execute("""
        CREATE TABLE IF NOT EXISTS global_word_status (
            id INTEGER PRIMARY KEY,
            word TEXT,
            status TEXT
        )
        """)
