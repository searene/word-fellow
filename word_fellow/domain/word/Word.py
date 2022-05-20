from typing import List, Dict

from ...domain.word.WordValueObject import WordValueObject


class Word(WordValueObject):

    def __init__(self, word_id: int, text: str, document_id: int, word_to_start_pos_dict: Dict[str, List[int]]):
        """
        Args:
            word_id: The word id.
            text: The word text, e.g. "beautiful", "python", etc.
            document_id: The document to which the word belongs.
            word_to_start_pos_dict: word -> start pos of the word
        """
        super().__init__(text, document_id, word_to_start_pos_dict)
        self.word_id = word_id

    def __eq__(self, other):
        if not isinstance(other, Word):
            return False
        return self.word_id == other.word_id and self.text == other.text and self.document_id == other.document_id \
               and self.word_to_start_pos_dict == other.word_to_start_pos_dict

    def has_same_values(self, word_value_object: WordValueObject):
        return self.text == word_value_object.text \
               and self.document_id == word_value_object.document_id \
               and self.word_to_start_pos_dict == word_value_object.word_to_start_pos_dict


