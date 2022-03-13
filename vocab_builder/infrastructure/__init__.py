import os.path

from vocab_builder.infrastructure.VocabBuilderDB import VocabBuilderDB


def get_db_path(addon_path: str) -> str:
    return os.path.join(addon_path, 'vocab.db')


def get_vocab_builder_db(addon_path: str) -> VocabBuilderDB:
    return VocabBuilderDB(get_db_path(addon_path))