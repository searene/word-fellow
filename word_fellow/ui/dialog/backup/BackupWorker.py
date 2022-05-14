from PyQt5.QtCore import QObject, pyqtSignal, QThread

from word_fellow.domain.backup.BackupService import BackupService
from word_fellow.domain.settings.SettingsService import SettingsService
from word_fellow.infrastructure import WordFellowDB


class BackupWorker(QObject):
    """This class is used as a QThread worker for asynchronous backup."""

    def __init__(self, db_path: str):
        super().__init__()
        self.__db_path = db_path

    def run(self):
        backup_service = self.__get_backup_service(self.__db_path)
        backup_service.run_backup()
        QThread.currentThread().quit()

    def __get_backup_service(self, db_path: str) -> BackupService:
        db = WordFellowDB(db_path)
        settings_service = SettingsService(db)
        return BackupService(settings_service)