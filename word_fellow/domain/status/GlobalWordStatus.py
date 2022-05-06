import enum

from word_fellow.domain.word.WordStatus import WordStatus
from word_fellow.infrastructure import WordFellowDB


class Status(enum.Enum):
    KNOWN = "KNOWN",
    STUDYING = "STUDYING",
    IGNORED = "IGNORED",
    STUDY_LATER = "STUDY_LATER"


def to_status(word_status: WordStatus) -> Status:
    if word_status == WordStatus.KNOWN:
        return Status.KNOWN
    elif word_status == WordStatus.STUDYING:
        return Status.STUDYING
    elif word_status == WordStatus.IGNORED:
        return Status.IGNORED
    elif word_status == WordStatus.STUDY_LATER:
        return Status.STUDY_LATER
    else:
        raise ValueError("Unknown word status: {}".format(word_status))


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



def insert_word_status(word: str, status: Status, db: WordFellowDB) -> GlobalWordStatus:
    global_word_status_id = db.insert("""
    INSERT INTO global_word_status (word, status) VALUES (?, ?)
    """, (word, status.name))
    return GlobalWordStatus(global_word_status_id, word, status)


def upsert_word_status(word: str, status: Status, db: WordFellowDB) -> None:
    cnt = db.fetch_one("select count(*) as cnt from global_word_status where word = ?", (word, ))[0]
    if cnt == 0:
        db.execute("insert into global_word_status (word, status) values (?, ?)", (word, status.name))
    else:
        db.execute("""
        UPDATE global_word_status SET status = ? WHERE word = ?
        """, (status.name, word))


def delete_word_status(word: str, status: Status, db: WordFellowDB) -> None:
    db.execute("""
    DELETE FROM global_word_status WHERE word = ? AND status = ?
    """, (word, status.name))