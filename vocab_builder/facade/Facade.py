from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker

from vocab_builder.domain.document.Document import Document


class Facade:
    def __init__(self, sql_engine: Engine):
        maker = sessionmaker(bind=sql_engine)
        self.session = maker()
        self.__init_database(sql_engine)

    def create_new_document(self, document_name: str) -> Document:
        document = Document(name=document_name)
        self.session.add(document)
        self.session.commit()
        return document

    def get_document_list(self) -> [Document]:
        return self.session.query(Document).all()

    @staticmethod
    def __init_database(engine: Engine):
        if not engine.has_table("documents"):
            Document.metadata.create_all(engine)