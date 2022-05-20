from typing import Optional

from ..word import WordFactory
from ..word.Word import Word
from ..word.WordService import get_words_by_document_id
from ..word.WordStatus import WordStatus
from ...infrastructure.WordFellowDB import WordFellowDB


class Document:

    def __init__(self, document_id: int, name: str, contents: str):
        self.document_id = document_id
        self.name = name
        self.contents = contents

    def get_next_word(self, offset: int, word_status: WordStatus, db: WordFellowDB) -> Optional[Word]:
        return WordFactory.get_next_word(self.document_id, offset, word_status, db)

    def get_words(self, db: WordFellowDB) -> [Word]:
        return get_words_by_document_id(self.document_id, db)

    def get_word_count(self, status: WordStatus, db: WordFellowDB) -> int:
        return WordFactory.get_word_count(self.document_id, status, db)

    def __eq__(self, other):
        if not isinstance(other, Document):
            return False
        return self.document_id == other.document_id and self.name == other.name and self.contents == other.contents
