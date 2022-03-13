from vocab_builder.domain.document.Document import Document
from vocab_builder.domain.word.Word import Word
from vocab_builder.infrastructure import VocabBuilderDB


def init_database(db: VocabBuilderDB):
    Document.init_database(db )
    Word.init_database(db)
