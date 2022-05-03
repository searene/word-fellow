from PyQt5.QtWidgets import QDialog, QVBoxLayout, QTabWidget, QWidget

from tests.utils import get_test_vocab_builder_db
from vocab_builder.domain.backup.BackupService import BackupService
from vocab_builder.domain.settings.SettingsService import SettingsService
from vocab_builder.infrastructure import VocabBuilderDB
from vocab_builder.ui.dialog.settings.BackupTab import BackupTab
from vocab_builder.ui.dialog.settings.ResetTab import ResetTab


class SettingsDialog(QDialog):
    def __init__(self, db: VocabBuilderDB):
        super(SettingsDialog, self).__init__()
        self.__db = db
        self.__settings_service = SettingsService(self.__db)
        self.__backup_service = BackupService(self.__settings_service)
        self.__setup_ui()

    def __setup_ui(self) -> None:
        self.setWindowTitle("Settings")
        vbox = QVBoxLayout()
        tab_widget = QTabWidget()
        tab_widget.addTab(BackupTab(self.__backup_service), "Backup")
        tab_widget.addTab(ResetTab(), "Reset")
        vbox.addWidget(tab_widget)
        self.setLayout(vbox)


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    w = SettingsDialog(get_test_vocab_builder_db())
    w.show()
    sys.exit(app.exec_())