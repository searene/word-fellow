from typing import Dict, List, TYPE_CHECKING
from html import escape

if TYPE_CHECKING:
    from vocab_builder.domain.document.Document import Document


class WordContext:

    def __init__(self, word: str, context: str, word_pos_in_context: int):
        self.word = word
        self.context = context
        self.word_pos_in_context = word_pos_in_context

    def get_prefix(self):
        return self.context[:self.word_pos_in_context]

    def get_suffix(self):
        return self.context[self.word_pos_in_context + len(self.word):]

    def to_html(self):
        return f"{self.__preprocess(self.get_prefix())}<b>{self.__preprocess(self.word)}</b>{self.__preprocess(self.get_suffix())}"

    def __preprocess(self, text: str):
        return escape(text).replace("\n", "<br>")

    def __eq__(self, other):
        if not isinstance(other, WordContext):
            return False
        return self.word == other.word and self.context == other.context and \
               self.word_pos_in_context == other.word_pos_in_context


class ShortAndLongContext:

    def __init__(self, short_context: WordContext, long_context: WordContext):
        self.short = short_context
        self.long = long_context

    def __eq__(self, other):
        if not isinstance(other, ShortAndLongContext):
            return False
        return self.short == other.short and self.long == other.long


class WordValueObject:

    def __init__(self, text: str, document_id: int, word_to_start_pos_dict: Dict[str, List[int]]):
        """
        Args:
            text: The word text, e.g. "beautiful", "python", etc.
            document_id: The document to which the word belongs.
            word_to_start_pos_dict: word -> start pos of the word
        """
        self.text = text
        self.document_id = document_id
        self.word_to_start_pos_dict = word_to_start_pos_dict

    def get_long_context(self, doc: 'Document', word: str, pos: int) -> WordContext:
        return self._get_context(200, doc, word, pos)

    def get_short_context(self, doc: 'Document', word: str, pos: int) -> WordContext:
        return self._get_context(50, doc, word, pos)

    def get_short_and_long_contexts(self, doc: 'Document', limit=5) -> [ShortAndLongContext]:
        word_contexts = []
        for word in self.word_to_start_pos_dict:
            for pos in self.word_to_start_pos_dict[word]:
                short_context = self.get_short_context(doc, word, pos)
                long_context = self.get_long_context(doc, word, pos)
                word_contexts.append(ShortAndLongContext(short_context, long_context))
                if len(word_contexts) >= limit:
                    return word_contexts
        return word_contexts

    def _get_context(self, length_to_end: int, doc: 'Document', word: str, pos: int) -> WordContext:
        """
        Args:
            length_to_end: The maximum number of characters allowed after the word
            doc: The document to which the word belongs.
            word: The word to get the context for.
            pos: The position of the word in the document.
        """
        start_index = pos - length_to_end if pos - length_to_end >= 0 else 0
        end_index = pos + len(word) + length_to_end if pos + len(word) + length_to_end < len(doc.contents) else len(
            doc.contents)

        word_pos_in_context = length_to_end if pos - length_to_end >= 0 else pos
        return WordContext(word, doc.contents[start_index: end_index], word_pos_in_context)
