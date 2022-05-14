from typing import Optional

from PyQt5.QtCore import QThread, QTimer
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QWidget


class BackingUpDialog(QDialog):

    def __init__(self, parent: Optional[QWidget], backup_thread: QThread):
        super(BackingUpDialog, self).__init__(parent)
        self.__backup_thread = backup_thread
        self.setWindowTitle("Backing Up...")
        self.__init_ui()

    def exec(self) -> None:
        is_finished = self.__check_if_thread_finished(self.__backup_thread)
        if not is_finished:
            super(BackingUpDialog, self).exec()

    def __check_if_thread_finished(self, backup_thread: QThread) -> bool:
        if backup_thread.isFinished():
            backup_thread.deleteLater()
            self.close()
            return True
        else:
            QTimer.singleShot(1000, lambda: self.__check_if_thread_finished(backup_thread))
            return False

    def __init_ui(self):
        vbox = QVBoxLayout()

        desc_label = QLabel("It won't take more than 10 seconds, please wait for a while...")
        vbox.addWidget(desc_label)

        self.setLayout(vbox)