from sqlalchemy.orm import Session

from vocab_builder.domain.document.Document import Document


class DocumentService:

    def __init__(self, session: Session):
        self.session = session

    def get_document_list(self) -> [Document]:
        return self.session.query(Document).all()

