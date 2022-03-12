from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from vocab_builder.domain import utils
from vocab_builder.infrastructure.VocabBuilderDB import VocabBuilderDB


def get_test_vocab_builder_db():
    return VocabBuilderDB(get_test_sqlite_url())


def get_test_sqlite_url():
    return ":memory:"


def get_test_session() -> Session:
    engine = create_engine(get_test_sqlite_url(), echo=True)
    maker = sessionmaker(bind=engine)
    session = maker()

    utils.init_database(session)

    return session
