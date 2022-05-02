from vocab_builder.domain.document.Document import Document
from vocab_builder.domain.settings.Settings import Settings
from vocab_builder.domain.settings.SettingsService import SettingsService
from vocab_builder.domain.status.GlobalWordStatus import GlobalWordStatus
from vocab_builder.domain.word import Word
from vocab_builder.infrastructure import VocabBuilderDB


def init_database(db: VocabBuilderDB):
    Document.init_database(db)
    Word.init_database(db)
    GlobalWordStatus.init_database(db)

    settings_service = SettingsService(db)
    settings_service.init_database()
