import enum

from vocab_builder.domain.word.WordStatus import WordStatus
from vocab_builder.infrastructure import VocabBuilderDB


class Status(enum.Enum):
    KNOWN = "KNOWN",
    STUDYING = "STUDYING"


class GlobalWordStatus:
    """
    A class to record each word's status, regardless which document it belongs to.
    """
    def __init__(self, id: int, word: str, global_status: Status):
        """
        Parameters
        ----------
            id: id
            word: a word
            global_status: The word's status
        """
        self.id = id
        self.word = word
        self.global_status = global_status

    @staticmethod
    def init_database(db: VocabBuilderDB):
        # TODO unique key
        db.execute("""
        CREATE TABLE IF NOT EXISTS global_word_status (
            id INTEGER PRIMARY KEY,
            word TEXT,
            status TEXT
        )
        """)


def insert_word_status(word: str, status: Status, db: VocabBuilderDB) -> GlobalWordStatus:
    global_word_status_id = db.insert("""
    INSERT INTO global_word_status (word, status) VALUES (?, ?)
    """, (word, status.name))
    return GlobalWordStatus(global_word_status_id, word, status)
