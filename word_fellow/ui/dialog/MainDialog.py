import os
import sys
from pathlib import Path

from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QPushButton, QApplication, QHBoxLayout, QVBoxLayout, QLabel, QDialog, QFileDialog,
                             QListWidgetItem, QSizePolicy, QListWidget, QScrollBar, QMenu)

from word_fellow.anki.IAnkiService import IAnkiService
from word_fellow.anki.MockedAnkiService import MockedAnkiService
from word_fellow.domain.document.Document import Document
from word_fellow.domain.document.DocumentService import DocumentService
from word_fellow.domain.document.analyzer.DefaultDocumentAnalyzer import DefaultDocumentAnalyzer
from word_fellow.domain.utils import init_database
from word_fellow.ui.util.DatabaseUtils import get_test_word_fellow_db
from word_fellow.infrastructure import WordFellowDB
from word_fellow.ui.dialog.document.DocumentDetailDialog import DocumentDetailDialog
from word_fellow.ui.dialog.context.list.ClickableListWidget import ClickableListWidget
from word_fellow.ui.dialog.settings.SettingsDialog import SettingsDialog
from word_fellow.ui.util.FileUtils import get_base_name_without_ext


class MainDialog(QDialog):

    def __init__(self, db: WordFellowDB, anki_service: IAnkiService, show_dialog=True):
        super().__init__()
        self.__db = db
        self.__anki_service = anki_service
        self.__document_service = DocumentService(self.__db)
        self.__show_dialog = show_dialog
        self.__init_ui(self.__document_service, self.__db, self.__show_dialog)

    def __init_ui(self, document_service: DocumentService, db: WordFellowDB, show_dialog: bool):
        vbox = QVBoxLayout()
        vbox.addLayout(self.__get_top_bar())
        self.__add_document_list(vbox, document_service, db, show_dialog)
        vbox.addWidget(self.__get_import_new_document_button())
        self.setLayout(vbox)
        self.setWindowTitle("WordFellow")

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

        menu = QMenu()
        self._import_by_file_action = menu.addAction("Import File (txt)")
        self._import_by_file_action.triggered.connect(lambda action: self.__open_import_file_dialog())

        btn.setMenu(menu)
        return btn

    def __open_import_file_dialog(self):
        document_file_path, file_filters = QFileDialog.getOpenFileName(self, 'Select document', '', 'Text Files (*.txt)')
        if len(document_file_path) == 0:
            # The user didn't select any file
            return
        doc_name = get_base_name_without_ext(document_file_path)
        doc_contents = Path(document_file_path).read_text()

        default_document_analyzer = DefaultDocumentAnalyzer(self.__db)
        doc = self.__document_service.import_document(doc_name, doc_contents, default_document_analyzer)
        self._list_widget.addItem(self.__to_list_item((doc.document_id, doc.name)))
        self._list_widget.show()
        self.__no_document_label.hide()

        # TODO After clicking on OK, the dialog hides behind Anki, need to fix it
        self.__anki_service.show_info_dialog("Importing is done")

    def __add_document_list(self, parent: QVBoxLayout, document_service: DocumentService, db: WordFellowDB, show_dialog: bool) -> None:
        self.__no_document_label = QLabel("No document is available, click the \"Add\" button below to start importing.")
        self.__no_document_label.setStyleSheet("QLabel { background-color : white; }")
        self.__no_document_label.setSizePolicy(QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding))
        self.__no_document_label.setMinimumHeight(200)
        self.__no_document_label.setContentsMargins(20, 20, 20, 20)
        self.__no_document_label.setAlignment(Qt.AlignCenter)
        scroll_bar = QScrollBar()
        self._list_widget = ClickableListWidget()
        self._list_widget.setVerticalScrollBar(scroll_bar)
        self._list_widget.itemClicked.connect(lambda item: self.on_list_item_clicked(item, document_service, db,
                                                                                     self._list_widget, show_dialog))
        parent.addWidget(self.__no_document_label)
        parent.addWidget(self._list_widget)

        doc_id_and_name_list = self.__document_service.get_document_id_and_name_list()
        if len(doc_id_and_name_list) == 0:
            self._list_widget.hide()
        else:
            self.__no_document_label.hide()
            for doc_id_and_name in doc_id_and_name_list:
                self._list_widget.addItem(self.__to_list_item(doc_id_and_name))

    def __to_list_item(self, doc_id_and_name: (int, str)) -> QListWidgetItem:
        res = QListWidgetItem()
        res.setText(doc_id_and_name[1])
        res.setData(QtCore.Qt.UserRole, doc_id_and_name[0])
        return res

    def on_list_item_clicked(self, item: QListWidgetItem, document_service: DocumentService, db: WordFellowDB,
                             doc_list: QListWidget, show_dialog: bool) -> None:
        doc_id = item.data(QtCore.Qt.UserRole)
        self.__open_document_dialog(doc_id, document_service, db, doc_list, show_dialog)

    def __open_document_dialog(self, doc_id: int, document_service: DocumentService, db: WordFellowDB,
                               doc_list: QListWidget, show_dialog: bool) -> None:
        doc = self.__document_service.get_doc_by_id(doc_id)
        self._doc_detail_dialog = DocumentDetailDialog(self, doc, db, document_service, self.__anki_service,
                                                       lambda: self.__delete_doc_from_list(doc_id, self._list_widget),
                                                       show_dialog)
        if show_dialog:
            self._doc_detail_dialog.show()

    def __delete_doc_from_list(self, doc_id: int, doc_list: QListWidget) -> None:
        for i in range(doc_list.count()):
            item = doc_list.item(i)
            if item.data(QtCore.Qt.UserRole) == doc_id:
                doc_list.takeItem(i)
                return


if __name__ == '__main__':
    app = QApplication(sys.argv)
    db = get_test_word_fellow_db()

    init_database(db)
    document_service = DocumentService(db)
    document_service.create_new_document("test name1", "test content")
    document_service.create_new_document("test name2", "test content")
    document_service.create_new_document("test name3", "test content")
    document_service.create_new_document("test name4", "test content")
    document_service.create_new_document("test name5", "test content")
    document_service.create_new_document("test name6", "test content")
    document_service.create_new_document("test name7", "test content")
    document_service.create_new_document("test name8", "test content")
    document_service.create_new_document("test name9", "test content")
    document_service.create_new_document("test name10", "test content")

    # db.execute("delete from documents")
    # db.execute("delete from words")
    # db.execute("delete from global_word_status")

    ex = MainDialog(db, MockedAnkiService(app))
    ex.show()
    app.exec_()
    os.remove(db.db_path)