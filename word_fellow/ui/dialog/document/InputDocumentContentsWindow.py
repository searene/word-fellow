import os
import sys
from typing import Callable

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QFormLayout, QLineEdit, QTextEdit, QHBoxLayout, QPushButton, \
    QApplication, QWidget

from ....domain.document.Document import Document
from ....domain.document.DocumentService import DocumentService
from ....domain.document.analyzer import IDocumentAnalyzer
from ....domain.document.analyzer.DefaultDocumentAnalyzer import DefaultDocumentAnalyzer
from ....ui.util import MsgUtils
from ....ui.util.DatabaseUtils import get_test_word_fellow_db


class InputDocumentContentsWindow(QWidget):

    def __init__(self, document_service: DocumentService, document_analyzer: IDocumentAnalyzer,
                 add_doc_handler: Callable[[Document], None], show_ui=True):
        super(InputDocumentContentsWindow, self).__init__()
        self.__show_ui = show_ui
        self.__document_service = document_service
        self.__document_analyzer = document_analyzer
        self.__add_doc_handler = add_doc_handler
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
        self._contents_text_edit.setAcceptRichText(False)
        form.addRow("Name", self._name_line_edit)
        form.addRow("Contents", self._contents_text_edit)
        vbox.addLayout(form)

    def __add_bottom_buttons(self, vbox: QVBoxLayout):
        hbox = QHBoxLayout()
        self._cancel_btn = QPushButton("Cancel")
        self._cancel_btn.clicked.connect(self.__close)
        self._ok_btn = QPushButton("OK")
        self._ok_btn.setDefault(True)
        self._ok_btn.clicked.connect(self.__import_document)
        hbox.addWidget(self._cancel_btn)
        hbox.addWidget(self._ok_btn)
        vbox.addLayout(hbox)

    def __close(self):
        self.close()

    def __import_document(self):
        if self._name_line_edit.text() == "":
            MsgUtils.show_warning_with_ok_btn(self, "Warning", "Please input document name.", show_ui=self.__show_ui)
            return
        if self._contents_text_edit.toPlainText() == "":
            MsgUtils.show_warning_with_ok_btn(self, "Warning", "Please input document contents.", show_ui=self.__show_ui)
            return
        name = self._name_line_edit.text()
        contents = self._contents_text_edit.toPlainText()
        doc = self.__document_service.import_document(name, contents, self.__document_analyzer)
        self.__add_doc_handler(doc)
        self.close()


if __name__ == "__main__":

    app = QApplication(sys.argv)
    db = get_test_word_fellow_db()
    document_service = DocumentService(db)
    win = InputDocumentContentsWindow(document_service, DefaultDocumentAnalyzer(db), lambda _: None)
    win.show()
    code = app.exec_()
    db.destroy()
    sys.exit(code)
