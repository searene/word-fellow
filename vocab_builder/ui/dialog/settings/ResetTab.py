from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel


class ResetTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.__setup_ui()

    def __setup_ui(self) -> None:
        vbox = QVBoxLayout()
        self.__add_caution_label(vbox)
        self.__add_reset_btn(vbox)
        self.setLayout(vbox)

    def __add_reset_btn(self, vbox: QVBoxLayout) -> None:
        self._reset_btn = QPushButton("Reset")
        vbox.addWidget(self._reset_btn)

    def __add_caution_label(self, vbox: QVBoxLayout) -> None:
        label = QLabel("You will lose all your data in anki-vocab-builder, including imported documents, marked words, and so on. Be careful!\n\nAnki decks, cards, notes and everything belonging to Anki won't be deleted.")
        label.setWordWrap(True)
        label.setMaximumWidth(300)
        vbox.addWidget(label)
