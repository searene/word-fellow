from vocab_builder.domain.document.Document import Document
from vocab_builder.domain.settings.Settings import Settings
from vocab_builder.domain.status.GlobalWordStatus import GlobalWordStatus
from vocab_builder.domain.utils import init_database
from vocab_builder.domain.word import Word
from vocab_builder.infrastructure.VocabBuilderDB import VocabBuilderDB


def get_test_vocab_builder_db() -> VocabBuilderDB:
    db = VocabBuilderDB(get_test_sqlite_url())
    init_database(db)
    return db


def get_test_sqlite_url():
    return ":memory:"