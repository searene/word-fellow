from PyQt5.QtCore import QObject, pyqtSignal

from vocab_builder.domain.backup.BackupService import BackupService
from vocab_builder.domain.settings.SettingsService import SettingsService
from vocab_builder.infrastructure import VocabBuilderDB


class BackupWorker(QObject):
    """This class is used as a QThread worker for asynchronous backup."""

    finished = pyqtSignal()

    def __init__(self, db_path: str):
        super().__init__()
        self.__backup_service = self.__get_backup_service(db_path)

    def run(self):
        self.__backup_service.run_backup()

    def __get_backup_service(self, db_path: str) -> BackupService:
        db = VocabBuilderDB(db_path)
        settings_service = SettingsService(db)
        return BackupService(settings_service)