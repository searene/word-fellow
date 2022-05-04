from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QApplication

from tests.utils import get_test_vocab_builder_db
from vocab_builder.domain.backup.BackupService import BackupService
from vocab_builder.domain.settings.SettingsService import SettingsService
from vocab_builder.infrastructure import get_db_path


class BackupDialog(QDialog):
    def __init__(self, backup_service: BackupService, db_path: str):
        super().__init__()
        self.__init_ui()
        backup_service.run_backup()

    def __init_ui(self):
        self.__layout_vbox = QVBoxLayout()
        self.setLayout(self.__layout_vbox)

        self.__add_description_label(self.__layout_vbox)

    def __add_description_label(self, vbox: QVBoxLayout):
        self._desc_label = QLabel("We have backed up your data for you.\n\n(Go to settings if you want to change the behavior.)")
        vbox.addWidget(self._desc_label)

        self._ok_btn = QPushButton("OK")
        vbox.addWidget(self._ok_btn)

    def __close(self):
        self.close()

    def __add_ok_button(self, vbox: QVBoxLayout):
        self._ok_btn = QPushButton("OK")
        self._ok_btn.clicked.connect(self.__close)
        vbox.addWidget(self._ok_btn)


if __name__ == "__main__":
    app = QApplication([])
    db = get_test_vocab_builder_db()
    settings_service = SettingsService(db)
    backup_service = BackupService(settings_service, get_db_path())
    dialog = BackupDialog(backup_service)
    dialog.show()
    app.exec_()