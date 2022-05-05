from PyQt5.QtWidgets import QDialog, QVBoxLayout, QTabWidget

from vocab_builder.domain.backup.BackupService import BackupService
from vocab_builder.domain.reset.ResetService import ResetService
from vocab_builder.domain.settings.SettingsService import SettingsService
from vocab_builder.infrastructure import VocabBuilderDB
from vocab_builder.ui.dialog.settings.backup.BackupTab import BackupTab
from vocab_builder.ui.dialog.settings.ResetTab import ResetTab
from vocab_builder.ui.util.DatabaseUtils import get_prod_vocab_builder_db


class SettingsDialog(QDialog):
    def __init__(self, db: VocabBuilderDB):
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
    w = SettingsDialog(get_prod_vocab_builder_db())
    w.show()
    sys.exit(app.exec_())