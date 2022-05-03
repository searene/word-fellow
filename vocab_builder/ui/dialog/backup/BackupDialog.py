from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QApplication

from tests.utils import get_test_vocab_builder_db
from vocab_builder.domain.backup.BackupService import BackupService
from vocab_builder.domain.settings.SettingsService import SettingsService
from vocab_builder.infrastructure import get_db_path


class Backup(QDialog):
    def __init__(self, backup_service: BackupService, db_path: str):
        super().__init__()
        self.__init_ui()
        self.__start_backup(backup_service, db_path)

    def __init_ui(self):
        self.__layout_vbox = QVBoxLayout()
        self.setLayout(self.__layout_vbox)

        self.__add_description_label(self.__layout_vbox)

    def __add_description_label(self, vbox: QVBoxLayout):
        self._desc_label = QLabel("Backing up...")
        vbox.addWidget(self._desc_label)

    def __add_bottom_buttons(self, vbox: QVBoxLayout):
        self._ok_btn = QPushButton("OK")
        vbox.addWidget(self._ok_btn)

    def __start_backup(self, backup_service: BackupService, db_path: str):
        backup_service.run_backup(db_path)
        self._desc_label.setText("We have backed up your data for you.\n\n(Go to settings if you want to change the behavior.)")
        self.__add_ok_button(self.__layout_vbox)

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
    backup_service = BackupService(settings_service)
    db_path = get_db_path()
    dialog = Backup(backup_service, db_path)
    dialog.show()
    app.exec_()