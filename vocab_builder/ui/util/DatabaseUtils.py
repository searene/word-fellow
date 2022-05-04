from typing import Optional

from vocab_builder.infrastructure import create_prod_vocab_builder_db, VocabBuilderDB


def get_prod_vocab_builder_db() -> VocabBuilderDB:
    return create_prod_vocab_builder_db()
