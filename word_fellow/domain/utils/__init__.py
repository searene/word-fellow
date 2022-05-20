from ...domain.document.DocumentService import DocumentService
from ...domain.settings.SettingsService import SettingsService
from ...domain.status.GlobalWordStatusService import GlobalWordStatusService
from ...domain.word import WordService
from ...infrastructure import WordFellowDB


def init_database(db: WordFellowDB):
    DocumentService(db).init_database()
    WordService.init_database(db)
    GlobalWordStatusService(db).init_database()

    SettingsService(db).init_database()


