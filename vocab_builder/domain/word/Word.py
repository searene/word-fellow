import json
from typing import List, Tuple, Dict

from vocab_builder.domain.word.WordValueObject import WordValueObject
from vocab_builder.infrastructure import VocabBuilderDB


class Word(WordValueObject):

    def __init__(self, word_id: int, text: str, document_id: int, word_to_start_pos_dict: Dict[str, List[int]],
                 skipped: bool):
        """
        Args:
            word_id: The word id.
            text: The word text, e.g. "beautiful", "python", etc.
            document_id: The document to which the word belongs.
            word_to_start_pos_dict: word -> start pos of the word
            skipped: Whether the reader decides to skip the word for the current document.
        """
        super().__init__(text, document_id, word_to_start_pos_dict, skipped)
        self.word_id = word_id

    def __eq__(self, other):
        if not isinstance(other, Word):
            return False
        return self.word_id == other.word_id and self.text == other.text and self.document_id == other.document_id \
               and self.word_to_start_pos_dict == other.word_to_start_pos_dict and self.skipped == other.skipped

    def has_same_values(self, word_value_object: WordValueObject):
        return self.text == word_value_object.text \
               and self.document_id == word_value_object.document_id \
               and self.word_to_start_pos_dict == word_value_object.word_to_start_pos_dict \
               and self.skipped == word_value_object.skipped


def get_words_by_document_id(document_id, db: VocabBuilderDB) -> [Word]:
    words_data_objects = db.all("""SELECT * from words WHERE document_id = ?""", document_id)
    return __convert_word_data_objects_to_words(words_data_objects)


def init_database(db: VocabBuilderDB):
    db.execute("""
    CREATE TABLE IF NOT EXISTS words (
        id INTEGER PRIMARY KEY,
        text TEXT NOT NULL,
        document_id INTEGER NOT NULL,
        positions TEXT NOT NULL,
        skipped BOOLEAN NOT NULL CHECK (skipped IN (0, 1))
    )
    """)


def __convert_word_data_objects_to_words(word_data_objects: List[Tuple]) -> List[Word]:
    res = []
    for word_data_object in word_data_objects:
        word_id = word_data_object[0]
        text = word_data_object[1]
        document_id = word_data_object[2]
        word_to_start_pos_dict = json.loads(word_data_object[3])
        skipped = True if word_data_object[4] == 1 else False
        res.append(Word(word_id, text, document_id, word_to_start_pos_dict, skipped))
    return res
