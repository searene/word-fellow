from sqlalchemy.orm import Session

from vocab_builder.domain.document.Document import Document
from vocab_builder.domain.word.Word import Word


def init_database(session: Session):
    Document.init_database(session)
    Word.init_database(session)
