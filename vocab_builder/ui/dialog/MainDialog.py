import sys
from pathlib import Path

from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QPushButton, QApplication, QHBoxLayout, QVBoxLayout, QLabel, QDialog, QFileDialog,
                             QListWidgetItem, QSizePolicy)

from vocab_builder.anki.IAnkiService import IAnkiService
from vocab_builder.anki.MockedAnkiService import MockedAnkiService
from vocab_builder.domain.document.Document import Document
from vocab_builder.domain.document.DocumentService import DocumentService
from vocab_builder.domain.document.analyzer.DefaultDocumentAnalyzer import DefaultDocumentAnalyzer
from vocab_builder.domain.utils import init_database
from vocab_builder.infrastructure import VocabBuilderDB
from vocab_builder.ui.dialog.document.DocumentWindow import DocumentWindow
from vocab_builder.ui.dialog.context.list.ClickableListWidget import ClickableListWidget
from vocab_builder.ui.dialog.settings.SettingsDialog import SettingsDialog
from vocab_builder.ui.util.DatabaseUtils import get_prod_vocab_builder_db
from vocab_builder.ui.util.FileUtils import get_base_name_without_ext


# TODO Give the user an option to delete a document
class MainDialog(QDialog):

    def __init__(self, db: VocabBuilderDB, anki_service: IAnkiService):
        super().__init__()
        self.__db = db
        self.__anki_service = anki_service
        self.__document_service = DocumentService(self.__db)
        self.__init_ui()

    def __init_ui(self):
        vbox = QVBoxLayout()
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
        settings_dialog = SettingsDialog(self.__db)
        settings_dialog.exec_()

    def __get_import_new_document_button(self) -> QPushButton:
        btn = QPushButton("Add")
        btn.clicked.connect(self.__open_import_new_document_dialog)
        return btn

    def __open_import_new_document_dialog(self):
        # TODO Limit extensions
        document_file_path, file_filters = QFileDialog.getOpenFileName(self, 'Select document', '', '')
        if len(document_file_path) == 0:
            # The user didn't select any file
            return
        doc_name = get_base_name_without_ext(document_file_path)
        doc_contents = Path(document_file_path).read_text()

        default_document_analyzer = DefaultDocumentAnalyzer(self.__db)
        doc = self.__document_service.import_document(doc_name, doc_contents, default_document_analyzer)
        self.__list_widget.addItem(self.__to_list_item((doc.document_id, doc.name)))
        self.__list_widget.show()
        self.__no_document_label.hide()
        self.__anki_service.show_info_dialog("Importing is done")

    def __add_document_list(self, parent: QVBoxLayout) -> None:
        self.__no_document_label = QLabel("No document is available, click the \"Add\" button below to start importing.")
        self.__no_document_label.setStyleSheet("QLabel { background-color : white; }")
        self.__no_document_label.setSizePolicy(QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding))
        self.__no_document_label.setMinimumHeight(200)
        self.__no_document_label.setContentsMargins(20, 20, 20, 20)
        self.__no_document_label.setAlignment(Qt.AlignCenter)
        self.__list_widget = ClickableListWidget()
        self.__list_widget.itemClicked.connect(self.on_list_item_clicked)
        parent.addWidget(self.__no_document_label)
        parent.addWidget(self.__list_widget)

        doc_id_and_name_list = self.__document_service.get_document_id_and_name_list()
        if len(doc_id_and_name_list) == 0:
            self.__list_widget.hide()
        else:
            self.__no_document_label.hide()
            for doc_id_and_name in doc_id_and_name_list:
                self.__list_widget.addItem(self.__to_list_item(doc_id_and_name))

    def __to_list_item(self, doc_id_and_name: (int, str)) -> QListWidgetItem:
        res = QListWidgetItem()
        res.setText(doc_id_and_name[1])
        res.setData(QtCore.Qt.UserRole, doc_id_and_name[0])
        return res

    def on_list_item_clicked(self, item: QListWidgetItem) -> None:
        doc_id = item.data(QtCore.Qt.UserRole)
        self.__open_document_dialog(doc_id)

    def __open_document_dialog(self, doc_id: int):
        doc = self.__document_service.get_doc_by_id(doc_id)
        doc_dialog = DocumentWindow(doc, self.__db, self.__anki_service)
        doc_dialog.show()
        self.close()

    def __convert_doc_to_hbox(self, doc: Document) -> QHBoxLayout:
        hbox = QHBoxLayout()
        doc_btn = QPushButton(doc.name)
        hbox.addWidget(doc_btn, 0, Qt.AlignLeft)
        doc_btn.clicked.connect(lambda: self.__open_document_dialog(doc.document_id))
        return hbox


if __name__ == '__main__':
    app = QApplication(sys.argv)
    db = get_prod_vocab_builder_db()

    init_database(db)
    db.execute("delete from documents")
    db.execute("delete from words")
    db.execute("delete from global_word_status")

    ex = MainDialog(db, MockedAnkiService())
    ex.show()
    sys.exit(app.exec_())
