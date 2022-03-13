from vocab_builder.domain.word.WordValueObject import WordValueObject
from vocab_builder.infrastructure import VocabBuilderDB


class Word(WordValueObject):

    def __init__(self, word_id: int, text: str, document_id: int, word_to_start_pos_dict: dict[str, [int]],
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
        self.id = word_id

    def has_same_values(self, word_value_object: WordValueObject):
        return self.text == word_value_object.text \
               and self.document_id == word_value_object.document_id \
               and self.word_to_start_pos_dict == word_value_object.word_to_start_pos_dict \
               and self.skipped == word_value_object.skipped

    @staticmethod
    def init_database(db: VocabBuilderDB):
        # TODO Use json as the type of positions?
        # TODO Use bool as the type of skipped?
        db.execute("""
        CREATE TABLE IF NOT EXISTS words (
            id INTEGER PRIMARY KEY,
            text TEXT,
            document_id INTEGER,
            positions TEXT,
            skipped TEXT
        )
        """)


