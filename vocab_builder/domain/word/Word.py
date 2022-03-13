import enum

from vocab_builder.infrastructure import VocabBuilderDB


class WordStatus(enum.Enum):
    UNKNOWN = 0
    KNOWN = 1
    STUDYING = 2


class WordPosition:

    def __init__(self, key: str, positions: [int]):
        self.key = key
        self.positions = positions


class Word:

    def __init__(self, id: int, text: str, document_id: int, positions: str, status: WordStatus):
        self.id = id
        self.text = text
        self.document_id = document_id
        self.positions = positions
        self.status = status

    @staticmethod
    def init_database(db: VocabBuilderDB):
        db.execute("""
        CREATE TABLE IF NOT EXISTS words (
            id INTEGER PRIMARY KEY,
            text TEXT,
            document_id INTEGER,
            positions TEXT,
            status TEXT
        )
        """)
