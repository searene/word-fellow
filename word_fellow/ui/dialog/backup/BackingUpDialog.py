from typing import Optional

from PyQt5.QtCore import QThread, QTimer, pyqtSignal
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QWidget

from word_fellow.ui.dialog.backup.BackupWorker import BackupWorker
from word_fellow.ui.util.DatabaseUtils import get_test_word_fellow_db


class BackingUpDialog(QDialog):

    def __init__(self, parent: Optional[QWidget], db_path: str):
        super(BackingUpDialog, self).__init__(parent)
        self.setWindowTitle("Backing Up...")
        self.__init_ui()
        self.backup_thread = self.__start_backup_thread(db_path)
        self.is_thread_finished = False
        self.__check_if_backup_finished()

    def __check_if_backup_finished(self):
        if self.is_thread_finished:
            self.close()
        else:
            QTimer.singleShot(1000, self.__check_if_backup_finished)

    def __start_backup_thread(self, db_path: str) -> QThread:
        res = QThread()

        self.__backup_worker = BackupWorker(db_path)
        self.__backup_worker.moveToThread(res)

        res.started.connect(self.__backup_worker.run)
        res.finished.connect(self.__on_thread_finished)
        res.start()
        return res

    def __on_thread_finished(self):
        self.backup_thread.deleteLater()
        self.is_thread_finished = True

    def __init_ui(self):
        vbox = QVBoxLayout()

        desc_label = QLabel("It won't take more than 10 seconds, please wait for a while...")
        vbox.addWidget(desc_label)

        self.setLayout(vbox)


if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    db = get_test_word_fellow_db()

    dlg = BackingUpDialog(None, db.db_path)
    dlg.show()

    sys.exit(app.exec_())
