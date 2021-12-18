import sqlalchemy
from sqlalchemy import Column, Integer, String

from domain.document import Base
from infrastructure.session import engine


class Document(Base):
    __tablename__ = 'documents'

    id = Column(Integer, primary_key=True)
    name = Column(String)


if not sqlalchemy.inspect(engine).has_table("documents"):
    Document.metadata.create_all(engine)
