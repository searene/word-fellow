from typing import Protocol
from abc import abstractmethod
from word_fellow.domain.document.Document import Document
from word_fellow.domain.word.Word import Word


class IDocumentAnalyzer(Protocol):

    @abstractmethod
    def import_words(self, document: Document) -> [Word]:
        pass