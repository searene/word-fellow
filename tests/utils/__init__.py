from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from vocab_builder.domain import utils


def get_test_sqlite_url():
    return ":memory:"


def get_test_session() -> Session:
    engine = create_engine(get_test_sqlite_url(), echo=True)
    maker = sessionmaker(bind=engine)
    session = maker()

    utils.init_database(session)

    return session
