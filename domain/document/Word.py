from sqlalchemy import Integer, String, Column


class Word:
    __tablename__ = 'words'

    id = Column(Integer, primary_key=True)
    text = Column(String)
    document_id = Column(Integer)
    positions = Column(String)
    status = Column(String)
