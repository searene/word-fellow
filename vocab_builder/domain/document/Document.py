from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Session

from vocab_builder.domain.document import Base
from vocab_builder.domain.word.Word import WordStatus
from vocab_builder.infrastructure.VocabBuilderDB import VocabBuilderDB


class Document(Base):
    __tablename__ = 'documents'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    contents = Column(String)

    def get_next_word(self, word_status: WordStatus):
        pass

    @staticmethod
    def init_database(db: VocabBuilderDB):
        db.execute("""
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY,
            name TEXT,
            contents TEXT
        )
        """)
