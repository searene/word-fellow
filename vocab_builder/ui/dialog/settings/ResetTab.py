from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QMessageBox

from vocab_builder.domain.reset.ResetService import ResetService


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
        msg.setText("This will remove all your anki-vocab-builder's data, are you sure you want to continue?")
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
            msg.setText("Reset is finished. Please close all of anki-vocab-builder's windows and restart it again to take effect.")
            msg.setWindowTitle("Finished")
            # TODO should init database when clicking on the addon's menu item, instead of when Anki starts
            msg.buttonClicked.connect(self.__close_parent)
            msg.exec_()

    def __close_parent(self):
        self.__parent.close()

    def __add_caution_label(self, vbox: QVBoxLayout) -> None:
        label = QLabel("You will lose all your data in anki-vocab-builder, including imported documents, marked words, and so on. Be careful!\n\nAnki decks, cards, notes and everything belonging to Anki won't be deleted.")
        label.setWordWrap(True)
        label.setMaximumWidth(300)
        vbox.addWidget(label)