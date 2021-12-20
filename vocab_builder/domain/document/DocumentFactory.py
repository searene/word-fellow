from sqlalchemy.orm import Session

from vocab_builder.domain.document.Document import Document
from vocab_builder.domain.document.analyzer import IDocumentAnalyzer
from vocab_builder.domain.word.WordService import save_words


class DocumentFactory:

    def __init__(self, session: Session):
        self.session = session

    def create_new_document(self, name: str, contents: str) -> Document:
        document = Document(name=name, contents=contents)
        self.session.add(document)
        self.session.commit()
        return document

    def import_document(self, name, contents, document_analyzer: IDocumentAnalyzer) -> Document:
        doc = self.create_new_document(name, contents)
        words = document_analyzer.get_words(doc)
        save_words(words)
        return doc

    def get_document_list(self) -> [Document]:
        return self.session.query(Document).all()
