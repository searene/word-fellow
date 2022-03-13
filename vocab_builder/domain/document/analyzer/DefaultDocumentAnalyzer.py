from interface import implements

from vocab_builder.domain.document.Document import Document
from vocab_builder.domain.word.Word import Word
from vocab_builder.domain.word.WordService import batch_insert
from vocab_builder.domain.document.analyzer import IDocumentAnalyzer
from vocab_builder.infrastructure import VocabBuilderDB


class DefaultDocumentAnalyzer(implements(IDocumentAnalyzer)):
    def __init__(self, db: VocabBuilderDB):
        self.db = db

    def analyze(self, document: Document) -> [Word]:
        words = self.__split_document_contents_into_words(document.contents)
        return batch_insert(words, self.db)

    def __split_document_contents_into_words(self, contents: str) -> [Word]:
        # TODO
        return []
