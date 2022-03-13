from vocab_builder.domain.document.Document import Document
from vocab_builder.domain.word import Word
from vocab_builder.infrastructure.VocabBuilderDB import VocabBuilderDB


def get_test_vocab_builder_db() -> VocabBuilderDB:
    db = VocabBuilderDB(get_test_sqlite_url())
    Document.init_database(db)
    Word.init_database(db)
    return db


def get_test_sqlite_url():
    return ":memory:"