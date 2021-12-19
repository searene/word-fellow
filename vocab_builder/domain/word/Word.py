import enum

from sqlalchemy import Integer, String, Column, ForeignKey, Enum
from sqlalchemy.orm import Session

from vocab_builder.domain.document import Base
from vocab_builder.domain.word.WordContext import WordContext


class WordStatus(enum.Enum):
    UNKNOWN = 0
    KNOWN = 1
    STUDYING = 2


class WordPosition:

    def __init__(self, key: str, positions: [int]):
        self.key = key
        self.positions = positions


class Word(Base):
    __tablename__ = 'words'

    id = Column(Integer, primary_key=True)
    text = Column(String)
    document_id = Column(Integer, ForeignKey('documents.id'))
    positions = Column(String)
    status = Column(Enum(WordStatus))

    def __init__(self):
        self.position_list = self.parse_positions(self.positions)
        self.word_contexts: [WordContext] = self.get_word_contexts(self.position_list)

    def parse_positions(self, positions: str) -> [WordPosition]:
        pass

    def get_word_contexts(self, position_list: [WordPosition]) -> [WordContext]:
        pass

    @staticmethod
    def init_database(session: Session):
        engine = session.get_bind()
        if not engine.has_table(Word.__tablename__):
            Word.metadata.create_all(engine)
