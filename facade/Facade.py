from domain.document.Document import Document
from domain.document.Word import Word
from infrastructure.session import session


def get_next_unknown_word(self, document_id) -> Word:
    pass


def create_new_document(document_name: str) -> Document:
    document = Document(name=document_name)
    session.add(document)
    session.commit()
    return document


def get_document_list() -> [Document]:
    return session.query(Document).all()