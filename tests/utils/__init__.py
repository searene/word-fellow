import os
import tempfile

from vocab_builder.domain.document.Document import Document
from vocab_builder.domain.settings.Settings import Settings
from vocab_builder.domain.status.GlobalWordStatus import GlobalWordStatus
from vocab_builder.domain.utils import init_database
from vocab_builder.domain.word import Word
from vocab_builder.infrastructure.VocabBuilderDB import VocabBuilderDB


def get_test_vocab_builder_db() -> VocabBuilderDB:
    db = VocabBuilderDB(get_test_db_path())
    init_database(db)
    return db


# TODO remove the test data when tests are finished
def get_test_db_path() -> str:
    config_folder = tempfile.mkdtemp()
    if not os.path.exists(config_folder):
        os.makedirs(config_folder)
    return os.path.join(config_folder, "vocab_builder.db")
