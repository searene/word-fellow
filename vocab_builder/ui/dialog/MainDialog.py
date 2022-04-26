import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QPushButton, QApplication, QHBoxLayout, QVBoxLayout, QLabel, QDialog, QFileDialog, QWidget)
from aqt.utils import showInfo

from vocab_builder.domain.document.Document import Document
from vocab_builder.domain.document.DocumentService import DocumentService
from vocab_builder.domain.document.analyzer.DefaultDocumentAnalyzer import DefaultDocumentAnalyzer
from vocab_builder.infrastructure import VocabBuilderDB
from vocab_builder.ui import prod_vocab_builder_db
from vocab_builder.ui.dialog.DocumentWindow import DocumentWindow
from vocab_builder.ui.util.FileUtils import get_base_name_without_ext
from vocab_builder.ui.util.PyQtUtils import get_horizontal_line
from pathlib import Path


class MainDialog(QDialog):

    def __init__(self, db: VocabBuilderDB):
        super().__init__()
        self.__db = db
        self.__doc_list_vbox = self.__get_document_list()
        self.__init_ui()

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

        document_service = DocumentService(self.__db)
        default_document_analyzer = DefaultDocumentAnalyzer(self.__db)
        doc = document_service.import_document(doc_name, doc_contents, default_document_analyzer)
        # TODO hide the "no documents available" label
        self.__doc_list_vbox.addLayout(self.__convert_doc_to_hbox(doc))
        showInfo("Importing is done.")

    def __get_document_list(self) -> QVBoxLayout:
        vbox = QVBoxLayout()
        self.__no_document_label = QLabel("No document is available.")
        vbox.addWidget(self.__no_document_label)

        document_service = DocumentService(prod_vocab_builder_db)
        documents = document_service.get_document_list()
        if len(documents) == 0:
            self.__no_document_label.show()
        else:
            self.__no_document_label.hide()
            for doc in documents:
                vbox.addLayout(self.__convert_doc_to_hbox(doc))
        return vbox

    def __open_document_dialog(self, doc: Document):
        doc_dialog = DocumentWindow(doc, self.__db)
        doc_dialog.show()
        # TODO How to close the current dialog before showing the document dialog
        self.close()

    def __convert_doc_to_hbox(self, doc: Document) -> QHBoxLayout:
        hbox = QHBoxLayout()
        doc_btn = QPushButton(doc.name)
        hbox.addWidget(doc_btn, 0, Qt.AlignLeft)
        doc_btn.clicked.connect(lambda: self.__open_document_dialog(doc))
        return hbox


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainDialog(prod_vocab_builder_db)
    sys.exit(app.exec_())
