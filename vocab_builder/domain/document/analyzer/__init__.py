from typing import Protocol
from abc import abstractmethod
from vocab_builder.domain.document.Document import Document
from vocab_builder.domain.word.Word import Word


class IDocumentAnalyzer(Protocol):

    @abstractmethod
    def get_words(self, document: Document) -> [Word]:
        pass