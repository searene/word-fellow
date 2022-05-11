import os
from typing import Optional

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QWidget, QVBoxLayout, QLabel, QHBoxLayout, QPushButton, QApplication, QMessageBox

from word_fellow.ui.util.DatabaseUtils import get_test_word_fellow_db
from word_fellow.domain.backup.Backup import Backup
from word_fellow.domain.backup.BackupService import BackupService
from word_fellow.domain.settings.SettingsService import SettingsService


class BackupDetailDialog(QDialog):

    def __init__(self, parent: Optional[QWidget], backup: Backup, backup_service: BackupService, show_restore_finished_dialog=True):
        self.__parent = parent
        self.__show_restore_finished_dialog = show_restore_finished_dialog
        super(BackupDetailDialog, self).__init__(parent)
        self.__setup_ui(backup, backup_service)
        self.setWindowFlags(self.windowFlags() | Qt.Popup)

    def __setup_ui(self, backup: Backup, backup_service: BackupService):
        vbox = QVBoxLayout()
        self.__add_backup_time_label(vbox, backup)
        self.__add_desc_label(vbox)
        vbox.addStretch()
        self.__add_bottom_buttons(vbox, backup, backup_service)
        self.setLayout(vbox)

    def __add_backup_time_label(self, vbox: QVBoxLayout, backup: Backup):
        # backup time in string
        backup_time = backup.get_backup_time().strftime("%Y-%m-%d %H:%M:%S")
        label = QLabel(f"Backup time: {backup_time}")
        label.setStyleSheet("QLabel { margin-top: 20; }")
        vbox.addWidget(label)

    def __add_desc_label(self, vbox: QVBoxLayout):
        label = QLabel("After restoration, WordFellow's data will be replaced by the restored one,  Anki's data (including decks, added words, etc) will not be affected, are you sure you want to restore?")
        label.setWordWrap(True)
        label.setStyleSheet("QLabel { margin-top: 20; }")
        vbox.addWidget(label)

    def __add_bottom_buttons(self, vbox: QVBoxLayout, backup: Backup, backup_service: BackupService):
        hbox = QHBoxLayout()
        hbox.addStretch()
        self.__add_restore_button(hbox, backup, backup_service)
        self.__add_cancel_button(hbox)
        vbox.addLayout(hbox)

    def __add_restore_button(self, hbox: QHBoxLayout, backup: Backup, backup_service: BackupService):
        self._restore_button = QPushButton("Yes, restore it")
        self._restore_button.clicked.connect(lambda: self.__start_restore(backup, backup_service))
        hbox.addWidget(self._restore_button)

    def __start_restore(self, backup: Backup, backup_service: BackupService):
        backup_service.restore(backup)
        if self.__show_restore_finished_dialog:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("Restoration finished! Please close all WordFellow's windows and start it again to take effect.")
            msg.setWindowTitle("Restoration finished!")
            msg.buttonClicked.connect(self.__close)
            msg.exec_()

    def __add_cancel_button(self, hbox: QHBoxLayout):
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.__close)
        hbox.addWidget(cancel_button)

    def __close(self):
        self.close()


if __name__ == "__main__":
    backup = Backup(f"/tmp/{Backup.name_prefix}20220501110000.db")
    db = get_test_word_fellow_db()
    settings_service = SettingsService(db)
    backup_service = BackupService(settings_service)

    app = QApplication([])
    dialog = BackupDetailDialog(None, backup, backup_service)
    dialog.exec()
    app.exec_()
    os.remove(db.db_path)