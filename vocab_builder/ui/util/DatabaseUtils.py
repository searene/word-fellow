from typing import Optional

from vocab_builder.infrastructure import get_vocab_builder_db, VocabBuilderDB


db: Optional[VocabBuilderDB] = None


def get_prod_vocab_builder_db() -> VocabBuilderDB:
    global db
    if db is not None:
        return db
    db = get_vocab_builder_db()
    return db
