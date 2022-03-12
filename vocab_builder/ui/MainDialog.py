import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QPushButton, QApplication, QHBoxLayout, QVBoxLayout, QLabel, QDialog)

from vocab_builder.domain.document.DocumentFactory import DocumentFactory
from vocab_builder.ui import prod_vocab_builder_db
from vocab_builder.ui.PyQtUtils import get_horizontal_line


class MainDialog(QDialog):

    def __init__(self):
        super().__init__()
        self.__init_ui()

    def __get_top_bar(self) -> QHBoxLayout:
        hbox = QHBoxLayout()
        hbox.addWidget(QLabel("Documents"))
        hbox.addWidget(QPushButton("Import New Document"))
        return hbox

    def __get_document_list(self) -> QVBoxLayout:
        vbox = QVBoxLayout()

        document_factory = DocumentFactory(prod_vocab_builder_db)
        documents = document_factory.get_document_list()
        for doc in documents:
            hbox = QHBoxLayout()
            hbox.addWidget(QLabel(doc.name), 0, Qt.AlignLeft)
            vbox.addLayout(hbox)
        return vbox

    def __init_ui(self):
        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addLayout(self.__get_top_bar())
        vbox.addWidget(get_horizontal_line())
        vbox.addLayout(self.__get_document_list())

        self.setLayout(vbox)
        self.setWindowTitle("Vocab Builder")

    def show_dialog(self):
        self.show()
        self.exec_()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainDialog()
    sys.exit(app.exec_())
