from interface import Interface

from vocab_builder.domain.document.Document import Document
from vocab_builder.domain.word.Word import Word


class IDocumentAnalyzer(Interface):

    def get_words(self, document: Document) -> [Word]:
        pass