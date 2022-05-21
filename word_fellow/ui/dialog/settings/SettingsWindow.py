from PyQt5.QtWidgets import QVBoxLayout, QTabWidget, QWidget

from word_fellow.ui.dialog.settings.backup.ExportImportTab import ExportImportTab
from ....domain.backup.BackupService import BackupService
from ....domain.reset.ResetService import ResetService
from ....domain.settings.SettingsService import SettingsService
from ....infrastructure import WordFellowDB
from ....ui.dialog.settings.ResetTab import ResetTab
from ....ui.dialog.settings.backup.BackupTab import BackupTab
from ....ui.util.DatabaseUtils import get_test_word_fellow_db


class SettingsWindow(QWidget):
    def __init__(self, db: WordFellowDB):
        super(SettingsWindow, self).__init__()
        self.__db = db
        self.__settings_service = SettingsService(self.__db)
        self.__reset_service = ResetService(self.__db)
        self.__backup_service = BackupService(self.__settings_service, self.__db)
        self.__setup_ui()

    def __setup_ui(self) -> None:
        self.setWindowTitle("Settings")
        vbox = QVBoxLayout()
        tab_widget = QTabWidget()
        tab_widget.addTab(BackupTab(self.__backup_service), "Backup")
        tab_widget.addTab(ResetTab(self, self.__reset_service), "Reset")
        tab_widget.addTab(ExportImportTab(self, self.__db), "Export/Import")
        vbox.addWidget(tab_widget)
        self.setLayout(vbox)


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    db = get_test_word_fellow_db()
    w = SettingsWindow(db)
    w.show()
    app.exec_()
    db.destroy()