from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Session

from vocab_builder.domain.document import Base
from vocab_builder.domain.word.Word import WordStatus


class Document(Base):
    __tablename__ = 'documents'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    contents = Column(String)

    def get_next_word(self, word_status: WordStatus):
        pass

    @staticmethod
    def init_database(session: Session):
        engine = session.get_bind()
        if not engine.has_table(Document.__tablename__):
            Document.metadata.create_all(engine)
