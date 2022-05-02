import sys
from pathlib import Path

from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QPushButton, QApplication, QHBoxLayout, QVBoxLayout, QLabel, QDialog, QFileDialog,
                             QListWidgetItem, QSizePolicy)

from vocab_builder.anki.IAnkiService import IAnkiService
from vocab_builder.domain.document.Document import Document
from vocab_builder.domain.document.DocumentService import DocumentService
from vocab_builder.domain.document.analyzer.DefaultDocumentAnalyzer import DefaultDocumentAnalyzer
from vocab_builder.infrastructure import VocabBuilderDB
from vocab_builder.ui.dialog.DocumentWindow import DocumentWindow
from vocab_builder.ui.dialog.context.list.ClickableListWidget import ClickableListWidget
from vocab_builder.ui.dialog.settings.SettingsDialog import SettingsDialog
from vocab_builder.ui.util.DatabaseUtils import get_prod_vocab_builder_db
from vocab_builder.ui.util.FileUtils import get_base_name_without_ext


class MainDialog(QDialog):

    def __init__(self, db: VocabBuilderDB, anki_service: IAnkiService):
        super().__init__()
        self.__db = db
        self.__anki_service = anki_service
        self.__init_ui()

    def __init_ui(self):
        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addLayout(self.__get_top_bar())
        self.__add_document_list(vbox)
        vbox.addWidget(self.__get_import_new_document_button())

        self.setLayout(vbox)
        self.setWindowTitle("Vocab Builder")

    def __get_top_bar(self) -> QHBoxLayout:
        hbox = QHBoxLayout()
        hbox.addWidget(QLabel("Documents"))
        hbox.addWidget(self.__get_settings_btn())
        return hbox

    def __get_settings_btn(self) -> QPushButton:
        btn = QPushButton("Settings")
        btn.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred))
        btn.clicked.connect(self.__open_settings_dialog)
        return btn

    def __open_settings_dialog(self):
        settings_dialog = SettingsDialog()
        settings_dialog.exec_()

    def __get_import_new_document_button(self) -> QPushButton:
        btn = QPushButton("Add")
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
        self.__list_widget.addItem(self.__to_list_item(doc))
        self.__list_widget.show()
        self.__no_document_label.hide()
        self.__anki_service.show_tooltip("Importing is done")

    def __add_document_list(self, parent: QVBoxLayout) -> None:
        self.__no_document_label = QLabel("No document is available.")
        self.__list_widget = ClickableListWidget()
        self.__list_widget.itemClicked.connect(self.on_list_item_clicked)
        parent.addWidget(self.__no_document_label)
        parent.addWidget(self.__list_widget)

        document_service = DocumentService(get_prod_vocab_builder_db())
        # Store the contents of all the documents may not be a good idea
        documents = document_service.get_document_list()
        if len(documents) == 0:
            self.__list_widget.hide()
        else:
            self.__no_document_label.hide()
            for doc in documents:
                self.__list_widget.addItem(self.__to_list_item(doc))

    def __to_list_item(self, doc: Document) -> QListWidgetItem:
        res = QListWidgetItem()
        res.setText(doc.name)
        res.setData(QtCore.Qt.UserRole, doc)
        return res

    def on_list_item_clicked(self, item: QListWidgetItem) -> None:
        doc: Document = item.data(QtCore.Qt.UserRole)
        self.__open_document_dialog(doc)

    def __open_document_dialog(self, doc: Document):
        doc_dialog = DocumentWindow(doc, self.__db, self.__anki_service.show_add_card_dialog)
        doc_dialog.show()
        self.close()

    def __convert_doc_to_hbox(self, doc: Document) -> QHBoxLayout:
        hbox = QHBoxLayout()
        doc_btn = QPushButton(doc.name)
        hbox.addWidget(doc_btn, 0, Qt.AlignLeft)
        doc_btn.clicked.connect(lambda: self.__open_document_dialog(doc))
        return hbox


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainDialog(get_prod_vocab_builder_db())
    ex.show()
    sys.exit(app.exec_())
