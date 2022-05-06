from word_fellow.domain.document.DocumentService import DocumentService
from word_fellow.domain.settings.SettingsService import SettingsService
from word_fellow.domain.status.GlobalWordStatusService import GlobalWordStatusService
from word_fellow.domain.word import WordService
from word_fellow.infrastructure import WordFellowDB


def init_database(db: WordFellowDB):
    DocumentService(db).init_database()
    WordService.init_database(db)
    GlobalWordStatusService(db).init_database()

    SettingsService(db).init_database()
