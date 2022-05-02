import os.path

from vocab_builder.infrastructure.VocabBuilderDB import VocabBuilderDB


def get_db_path() -> str:
    # TODO consider supporting auto-backup and suggesting restore when there's no data
    # TODO Allow user to reset the data
    home_dir = os.path.expanduser("~")
    config_folder = os.path.join(home_dir, ".anki-vocab-builder")
    if not os.path.exists(config_folder):
        os.makedirs(config_folder)
    return os.path.join(config_folder, "vocab_builder.db")


def get_vocab_builder_db() -> VocabBuilderDB:
    return VocabBuilderDB(get_db_path())