import os.path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from vocab_builder.infrastructure.VocabBuilderDB import VocabBuilderDB


def get_db_path(addon_path: str) -> str:
    return os.path.join(addon_path, 'vocab.db')


def get_vocab_builder_db(addon_path: str) -> VocabBuilderDB:
    return VocabBuilderDB(get_db_path(addon_path))


def get_session(addon_path: str) -> Session:
    db_path = get_db_path(addon_path)
    engine = create_engine(f'sqlite:///{db_path}', echo=True)
    maker = sessionmaker(bind=engine)
    return maker()
