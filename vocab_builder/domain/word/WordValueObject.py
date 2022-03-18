from typing import Dict, List, TYPE_CHECKING

if TYPE_CHECKING:
    from vocab_builder.domain.document.Document import Document


class WordContext:

    def __init__(self, word: str, context: str, word_pos_in_context: int):
        self.word = word
        self.context = context
        self.word_pos_in_context = word_pos_in_context

    def __eq__(self, other):
        if not isinstance(other, WordContext):
            return False
        return self.word == other.word and self.context == other.context and \
               self.word_pos_in_context == other.word_pos_in_context


class WordValueObject:

    def __init__(self, text: str, document_id: int, word_to_start_pos_dict: Dict[str, List[int]], skipped: bool):
        """
        Args:
            text: The word text, e.g. "beautiful", "python", etc.
            document_id: The document to which the word belongs.
            word_to_start_pos_dict: word -> start pos of the word
            skipped: Whether the reader decides to skip the word for the current document.
        """
        self.text = text
        self.document_id = document_id
        self.word_to_start_pos_dict = word_to_start_pos_dict
        self.skipped = skipped

    def get_long_context(self, doc: 'Document', word: str, pos: int) -> WordContext:
        return self.__get_context(200, doc, word, pos)

    def get_short_context(self, doc: 'Document', word: str, pos: int) -> WordContext:
        return self.__get_context(50, doc, word, pos)

    def __get_context(self, length_to_end: int, doc: 'Document', word: str, pos: int) -> WordContext:
        start_index = pos - length_to_end if pos - length_to_end >= 0 else 0
        end_index = pos + len(word) + length_to_end if pos + len(word) + length_to_end < len(doc.contents) else len(
            doc.contents) - 1
        word_pos_in_context = length_to_end if pos - length_to_end >= 0 else pos
        return WordContext(word, doc.contents[start_index: end_index], word_pos_in_context)
