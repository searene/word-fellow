from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker


def get_test_session() -> Session:
    engine = create_engine('sqlite:///:memory:', echo=True)
    maker = sessionmaker(bind=engine)
    return maker()
