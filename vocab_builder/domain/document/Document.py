from vocab_builder.domain.word.Word import WordStatus
from vocab_builder.infrastructure.VocabBuilderDB import VocabBuilderDB


class Document:

    def __init__(self, id: int, name: str, contents: str):
        self.id = id
        self.name = name
        self.contents = contents

    def get_next_word(self, word_status: WordStatus):
        pass

    def __eq__(self, other):
        if not isinstance(other, Document):
            return False
        return self.id == other.id and self.name == other.name and self.contents == other.contents

    @staticmethod
    def init_database(db: VocabBuilderDB):
        db.execute("""
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY,
            name TEXT,
            contents TEXT
        )
        """)
