from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QMessageBox, QApplication

from ....ui.util.DatabaseUtils import get_test_word_fellow_db
from ....domain.reset.ResetService import ResetService


class ResetTab(QWidget):
    def __init__(self, parent, reset_service: ResetService):
        super().__init__(parent)
        self.__parent = parent
        self.__reset_service = reset_service
        self.__setup_ui()

    def __setup_ui(self) -> None:
        vbox = QVBoxLayout()
        self.__add_caution_label(vbox)
        self.__add_reset_btn(vbox)
        self.setLayout(vbox)

    def __add_reset_btn(self, vbox: QVBoxLayout) -> None:
        self._reset_btn = QPushButton("Reset")
        self._reset_btn.clicked.connect(self.__show_warning_dialog)
        vbox.addWidget(self._reset_btn)

    def __show_warning_dialog(self) -> None:
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setText("This will remove all your WordFellow's data, are you sure you want to continue?")
        msg.setWindowTitle("Warning")
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        msg.buttonClicked.connect(lambda btn: self.__warning_dialog_btn_handler(btn, msg))
        msg.exec_()

    def __warning_dialog_btn_handler(self, button: QMessageBox.StandardButton, msg_box: QMessageBox) -> None:
        btn_code = msg_box.standardButton(button)
        if btn_code == QMessageBox.Ok:
            self.__reset_service.reset()
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("Reset is finished. Please close all of WordFellow's windows and restart it again to take effect.")
            msg.setWindowTitle("Finished")
            msg.buttonClicked.connect(self.__close_parent)
            msg.exec_()

    def __close_parent(self):
        self.__parent.close()

    def __add_caution_label(self, vbox: QVBoxLayout) -> None:
        label = QLabel("You will lose all your data in WordFellow, including imported documents, marked words, and so on. Be careful!\n\nAnki decks, cards, notes and everything belonging to Anki won't be deleted.")
        label.setWordWrap(True)
        vbox.addWidget(label)


if __name__ == "__main__":
    db = get_test_word_fellow_db()
    reset_service = ResetService(db)
    app = QApplication([])
    reset_tab = ResetTab(None, reset_service)
    reset_tab.show()
    app.exec_()