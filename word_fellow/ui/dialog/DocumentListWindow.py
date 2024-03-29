import os
import sys
from pathlib import Path

from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import (QPushButton, QApplication, QHBoxLayout, QVBoxLayout, QLabel, QFileDialog,
                             QListWidgetItem, QSizePolicy, QListWidget, QScrollBar, QMenu, QWidget)

from ...anki.IAnkiService import IAnkiService
from ...anki.MockedAnkiService import MockedAnkiService
from ...domain.document.Document import Document
from ...domain.document.DocumentService import DocumentService
from ...domain.document.analyzer import IDocumentAnalyzer
from ...domain.document.analyzer.DefaultDocumentAnalyzer import DefaultDocumentAnalyzer
from ...domain.utils import init_database
from ...infrastructure import WordFellowDB
from ...ui.dialog.backup.BackingUpDialog import BackingUpDialog
from ...ui.dialog.backup.BackupWorker import BackupWorker
from ...ui.dialog.context.list.ClickableListWidget import ClickableListWidget
from ...ui.dialog.document.DocumentDetailWindow import DocumentDetailWindow
from ...ui.dialog.document.InputDocumentContentsWindow import InputDocumentContentsWindow
from ...ui.dialog.settings.SettingsWindow import SettingsWindow
from ...ui.util import MsgUtils
from ...ui.util.DatabaseUtils import get_test_word_fellow_db
from ...ui.util.FileUtils import get_base_name_without_ext


class DocumentListWindow(QWidget):

    def __init__(self, db: WordFellowDB, anki_service: IAnkiService, document_analyzer: IDocumentAnalyzer,
                 show_window=True):
        super().__init__()
        self.__db = db
        self.__anki_service = anki_service
        self.__document_service = DocumentService(self.__db)
        self.__show_window = show_window
        self.__init_ui(self.__document_service, self.__db, self.__show_window, document_analyzer, show_window)
        self.__run_backup()

    def closeEvent(self, event: QtGui.QCloseEvent) -> None:
        event.ignore()
        backing_up_dialog = BackingUpDialog(self, self.__backup_thread)
        if self.__show_window:
            backing_up_dialog.exec()

        event.accept()

    def __run_backup(self):
        self.__backup_thread = QThread()

        self.__backup_worker = BackupWorker(self.__db.db_path)
        self.__backup_worker.moveToThread(self.__backup_thread)

        self.__backup_thread.started.connect(self.__backup_worker.run)
        self.__backup_thread.start()

    def __init_ui(self, document_service: DocumentService, db: WordFellowDB, show_dialog: bool, document_analyzer: IDocumentAnalyzer, show_ui: bool):
        vbox = QVBoxLayout()
        vbox.addLayout(self.__get_top_bar())
        self.__add_document_list(vbox, document_service, db, show_dialog)
        vbox.addWidget(self.__get_import_new_document_button(document_service, document_analyzer, show_ui))
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
        self._settings_win = SettingsWindow(self.__db)
        self._settings_win.show()

    def __get_import_new_document_button(self, document_service: DocumentService, document_analyzer: IDocumentAnalyzer, show_ui: bool) -> QPushButton:
        btn = QPushButton(self)
        btn.setText("Add")

        menu = QMenu(self)
        self._import_by_file_action = menu.addAction("Import File (txt)")
        self._import_by_file_action.triggered.connect(lambda action: self.__open_import_file_dialog(show_ui))
        self._import_by_text_action = menu.addAction("Input documents contents manually")
        self._import_by_text_action.triggered.connect(lambda action: self.__open_input_document_contents_dialog(document_service, document_analyzer, show_ui))

        btn.setMenu(menu)
        return btn

    def __open_input_document_contents_dialog(self, document_service: DocumentService, document_analyzer: IDocumentAnalyzer, show_ui: bool):
        self._input_documents_contents_dialog = InputDocumentContentsWindow(document_service, document_analyzer,
                                                                            lambda doc: self.__add_doc_to_list(doc), show_ui)
        if show_ui:
            self._input_documents_contents_dialog.show()

    def __open_import_file_dialog(self, show_ui: bool):
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

        MsgUtils.show_warning_with_ok_btn(self, "Done", "Importing is done", show_ui)

    def __add_document_list(self, parent: QVBoxLayout, document_service: DocumentService, db: WordFellowDB, show_dialog: bool) -> None:
        scroll_bar = QScrollBar()
        self._list_widget = ClickableListWidget()
        self._list_widget.setVerticalScrollBar(scroll_bar)
        self._list_widget.itemClicked.connect(lambda item: self.on_list_item_clicked(item, document_service, db,
                                                                                     show_dialog))
        parent.addWidget(self._list_widget)

        doc_id_and_name_list = self.__document_service.get_document_id_and_name_list()
        for doc_id_and_name in doc_id_and_name_list:
            self._list_widget.addItem(self.__to_list_item(doc_id_and_name))

    def __to_list_item(self, doc_id_and_name: (int, str)) -> QListWidgetItem:
        res = QListWidgetItem()
        res.setText(doc_id_and_name[1])
        res.setData(QtCore.Qt.UserRole, doc_id_and_name[0])
        return res

    def on_list_item_clicked(self, item: QListWidgetItem, document_service: DocumentService, db: WordFellowDB, show_dialog: bool) -> None:
        doc_id = item.data(QtCore.Qt.UserRole)
        self.__open_document_window(doc_id, document_service, db, show_dialog)

    def __open_document_window(self, doc_id: int, document_service: DocumentService, db: WordFellowDB, show_dialog: bool) -> None:
        doc = self.__document_service.get_doc_by_id(doc_id)
        self._doc_detail_window = DocumentDetailWindow(doc, db, document_service, self.__anki_service,
                                                       lambda: self.__delete_doc_from_list(doc_id, self._list_widget),
                                                       show_dialog)
        if show_dialog:
            self._doc_detail_window.show()

    def __add_doc_to_list(self, doc: Document) -> None:
        self._list_widget.addItem(self.__to_list_item((doc.document_id, doc.name)))

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

    ex = DocumentListWindow(db, MockedAnkiService(app), DefaultDocumentAnalyzer(db))
    ex.show()
    app.exec_()
    db.destroy()