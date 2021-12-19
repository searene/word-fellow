from interface import implements

from vocab_builder.domain.document.Document import Document
from vocab_builder.domain.word.Word import Word
from vocab_builder.domain.document.analyzer import IDocumentAnalyzer


class TraceOriginDocumentAnalyzer(implements(IDocumentAnalyzer)):
    def __init__(self):
        pass

    def analyze(self, document: Document) -> [Word]:
        pass