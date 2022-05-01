import enum

from vocab_builder.domain.word.WordStatus import WordStatus
from vocab_builder.infrastructure import VocabBuilderDB


class Status(enum.Enum):
    KNOWN = "KNOWN",
    STUDYING = "STUDYING",
    IGNORED = "IGNORED",
    STUDY_LATER = "STUDY_LATER"


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
        db.execute("""
        CREATE TABLE IF NOT EXISTS global_word_status (
            id INTEGER PRIMARY KEY,
            word TEXT NOT NULL UNIQUE,
            status TEXT NOT NULL
        )
        """)


def insert_word_status(word: str, status: Status, db: VocabBuilderDB) -> GlobalWordStatus:
    global_word_status_id = db.insert("""
    INSERT INTO global_word_status (word, status) VALUES (?, ?)
    """, (word, status.name))
    return GlobalWordStatus(global_word_status_id, word, status)


def upsert_word_status(word: str, status: Status, db: VocabBuilderDB) -> None:
    cnt = db.fetch_one("select count(*) as cnt from global_word_status where word = ?", (word, ))[0]
    if cnt == 0:
        db.execute("insert into global_word_status (word, status) values (?, ?)", (word, status.name))
    else:
        db.execute("""
        UPDATE global_word_status SET status = ? WHERE word = ?
        """, (status.name, word))
