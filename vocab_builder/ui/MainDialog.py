import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QPushButton, QApplication, QHBoxLayout, QVBoxLayout, QLabel, QDialog, QFileDialog)
from aqt.utils import showInfo

from vocab_builder.domain.document.Document import Document
from vocab_builder.domain.document.DocumentFactory import DocumentFactory
from vocab_builder.domain.document.analyzer.DefaultDocumentAnalyzer import DefaultDocumentAnalyzer
from vocab_builder.ui import prod_vocab_builder_db
from vocab_builder.ui.DocumentDialog import DocumentDialog
from vocab_builder.ui.FileUtils import get_base_name_without_ext
from vocab_builder.ui.PyQtUtils import get_horizontal_line
from pathlib import Path


class MainDialog(QDialog):

    def __init__(self):
        super().__init__()
        self.__doc_list_vbox = self.__get_document_list()
        self.__init_ui()

    def show_dialog(self):
        self.show()
        self.exec_()

    def __init_ui(self):
        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addLayout(self.__get_top_bar())
        vbox.addWidget(get_horizontal_line())
        vbox.addLayout(self.__doc_list_vbox)

        self.setLayout(vbox)
        self.setWindowTitle("Vocab Builder")

    def __get_top_bar(self) -> QHBoxLayout:
        hbox = QHBoxLayout()
        hbox.addWidget(QLabel("Documents"))
        hbox.addWidget(self.__get_import_new_document_button())
        return hbox

    def __get_import_new_document_button(self) -> QPushButton:
        btn = QPushButton("Import New Document")
        btn.clicked.connect(self.__open_import_new_document_dialog)
        return btn

    def __open_import_new_document_dialog(self):
        document_file_path, file_filters = QFileDialog.getOpenFileName(self, 'Select document', '', '')
        if len(document_file_path) == 0:
            # The user didn't select any file
            return
        doc_name = get_base_name_without_ext(document_file_path)
        doc_contents = Path(document_file_path).read_text()

        document_factory = DocumentFactory(prod_vocab_builder_db)
        default_document_analyzer = DefaultDocumentAnalyzer(prod_vocab_builder_db)
        doc = document_factory.import_document(doc_name, doc_contents, default_document_analyzer)
        self.__doc_list_vbox.addLayout(MainDialog.__convert_doc_to_hbox(doc))
        showInfo("Importing is done.")

    def __get_document_list(self) -> QVBoxLayout:
        vbox = QVBoxLayout()

        document_factory = DocumentFactory(prod_vocab_builder_db)
        documents = document_factory.get_document_list()
        for doc in documents:
            vbox.addLayout(self.__convert_doc_to_hbox(doc))
        return vbox

    def __open_document_dialog(self, document_id: int, document_name: str):
        doc_dialog = DocumentDialog(document_id, document_name)
        doc_dialog.show_dialog()
        self.close()

    def __convert_doc_to_hbox(self, doc: Document) -> QHBoxLayout:
        hbox = QHBoxLayout()
        doc_btn = QPushButton(doc.name)
        hbox.addWidget(doc_btn, 0, Qt.AlignLeft)
        doc_btn.clicked.connect(lambda: self.__open_document_dialog(doc.document_id, doc.name))
        return hbox


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainDialog()
    sys.exit(app.exec_())
