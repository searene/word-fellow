from typing import Protocol
from abc import abstractmethod
from ....domain.document.Document import Document
from ....domain.word.Word import Word


class IDocumentAnalyzer(Protocol):

    @abstractmethod
    def import_words(self, document: Document) -> [Word]:
        pass