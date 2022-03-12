from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from vocab_builder.domain import utils
from vocab_builder.infrastructure.VocabBuilderDB import VocabBuilderDB


def get_test_vocab_builder_db():
    return VocabBuilderDB(get_test_sqlite_url())


def get_test_sqlite_url():
    return ":memory:"