from typing import Optional

from vocab_builder.domain.word import WordFactory
from vocab_builder.domain.word.Word import Word, get_words_by_document_id
from vocab_builder.domain.word.WordStatus import WordStatus
from vocab_builder.infrastructure.VocabBuilderDB import VocabBuilderDB


class Document:

    def __init__(self, document_id: int, name: str, contents: str):
        self.document_id = document_id
        self.name = name
        self.contents = contents

    def get_next_word(self, offset: int, word_status: WordStatus, db: VocabBuilderDB) -> Optional[Word]:
        return WordFactory.get_next_word(self.document_id, offset, word_status, db)

    def get_words(self, db: VocabBuilderDB) -> [Word]:
        return get_words_by_document_id(self.document_id, db)

    def __eq__(self, other):
        if not isinstance(other, Document):
            return False
        return self.document_id == other.document_id and self.name == other.name and self.contents == other.contents

    @staticmethod
    def init_database(db: VocabBuilderDB):
        db.execute("""
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY,
            name TEXT,
            contents TEXT
        )
        """)