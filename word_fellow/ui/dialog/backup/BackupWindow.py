import os

from PyQt5.QtWidgets import QVBoxLayout, QLabel, QPushButton, QApplication, QWidget

from word_fellow.domain.backup.BackupService import BackupService
from word_fellow.domain.settings.SettingsService import SettingsService
from word_fellow.infrastructure import get_prod_db_path
from word_fellow.ui.util.DatabaseUtils import get_test_word_fellow_db


class BackupWindow(QWidget):
    def __init__(self, backup_service: BackupService):
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
    db = get_test_word_fellow_db()
    settings_service = SettingsService(db)
    backup_service = BackupService(settings_service, get_prod_db_path())
    win = BackupWindow(backup_service)
    win.show()
    app.exec_()
    os.remove(db.db_path)