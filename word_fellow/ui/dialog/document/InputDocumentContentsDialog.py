import os
import sys

from PyQt5.QtWidgets import QDialog, QVBoxLayout, QFormLayout, QLineEdit, QTextEdit, QHBoxLayout, QPushButton, \
    QApplication

from word_fellow.domain.document.DocumentService import DocumentService
from word_fellow.ui.util.DatabaseUtils import get_test_word_fellow_db


class InputDocumentContentsDialog(QDialog):

    def __init__(self, document_service: DocumentService):
        super(InputDocumentContentsDialog, self).__init__()
        self.__document_service = document_service
        self.__setup_ui()

    def __setup_ui(self):
        vbox = QVBoxLayout()

        self.__add_form(vbox)
        self.__add_bottom_buttons(vbox)

        self.setLayout(vbox)

    def __add_form(self, vbox: QVBoxLayout):
        form = QFormLayout()
        self._name_line_edit = QLineEdit()
        self._contents_text_edit = QTextEdit()
        form.addRow("Name", self._name_line_edit)
        form.addRow("Contents", self._contents_text_edit)
        vbox.addLayout(form)

    def __add_bottom_buttons(self, vbox: QVBoxLayout):
        hbox = QHBoxLayout()
        self._cancel_btn = QPushButton("Cancel")
        self._ok_btn = QPushButton("OK")
        self._ok_btn.setDefault(True)
        hbox.addWidget(self._cancel_btn)
        hbox.addWidget(self._ok_btn)
        vbox.addLayout(hbox)


if __name__ == "__main__":

    app = QApplication(sys.argv)
    db = get_test_word_fellow_db()
    document_service = DocumentService(db)
    dialog = InputDocumentContentsDialog(document_service)
    dialog.show()
    code = app.exec_()
    os.remove(db.db_path)
    sys.exit(code)
