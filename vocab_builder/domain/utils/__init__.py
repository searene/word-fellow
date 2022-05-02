from vocab_builder.domain.document.DocumentService import DocumentService
from vocab_builder.domain.settings.SettingsService import SettingsService
from vocab_builder.domain.status.GlobalWordStatusService import GlobalWordStatusService
from vocab_builder.domain.word import WordService
from vocab_builder.infrastructure import VocabBuilderDB


def init_database(db: VocabBuilderDB):
    DocumentService(db).init_database()
    WordService.init_database(db)
    GlobalWordStatusService(db).init_database()

    SettingsService(db).init_database()
