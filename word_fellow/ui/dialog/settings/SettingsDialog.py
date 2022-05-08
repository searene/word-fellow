import os

from PyQt5.QtWidgets import QDialog, QVBoxLayout, QTabWidget

from word_fellow.domain.backup.BackupService import BackupService
from word_fellow.domain.reset.ResetService import ResetService
from word_fellow.domain.settings.SettingsService import SettingsService
from word_fellow.infrastructure import WordFellowDB
from word_fellow.ui.util.DatabaseUtils import get_test_word_fellow_db
from word_fellow.ui.dialog.settings.backup.BackupTab import BackupTab
from word_fellow.ui.dialog.settings.ResetTab import ResetTab


class SettingsDialog(QDialog):
    def __init__(self, db: WordFellowDB):
        super(SettingsDialog, self).__init__()
        self.__db = db
        self.__settings_service = SettingsService(self.__db)
        self.__reset_service = ResetService(self.__db)
        self.__backup_service = BackupService(self.__settings_service)
        self.__setup_ui()

    def __setup_ui(self) -> None:
        self.setWindowTitle("Settings")
        vbox = QVBoxLayout()
        tab_widget = QTabWidget()
        tab_widget.addTab(BackupTab(self.__backup_service), "Backup")
        tab_widget.addTab(ResetTab(self, self.__reset_service), "Reset")
        vbox.addWidget(tab_widget)
        self.setLayout(vbox)


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    db = get_test_word_fellow_db()
    w = SettingsDialog(db)
    w.show()
    app.exec_()
    os.remove(db.db_path)