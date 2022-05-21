import sys
import tempfile

from PyQt5.QtCore import Qt
from PyQt5.QtTest import QTest
from PyQt5.QtWidgets import QApplication, QMessageBox

from tests.base.BaseTestCase import BaseTestCase
from word_fellow.domain.document.DocumentService import DocumentService
from word_fellow.domain.utils import FileUtils
from word_fellow.infrastructure import WordFellowDB
from word_fellow.ui.dialog.settings.backup.ExportImportTab import ExportImportTab


class ExportImportTabTestCase(BaseTestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.__app = QApplication(sys.argv)

    def setUp(self) -> None:
        super(ExportImportTabTestCase, self).setUp()
        self.__form = ExportImportTab(None, self.db, show_ui=False)

    def test_can_export_and_import(self):
        # initialize the database
        doc_service = DocumentService(self.db)
        doc1 = doc_service.create_new_document("test name", "test content")

        # export
        export_file_path = FileUtils.generate_non_existent_temp_file_path() + ".db"
        self.__form._export_line_edit.setText(export_file_path)
        QTest.mouseClick(self.__form._export_btn, Qt.LeftButton)
        QTest.mouseClick(self.__form._export_success_msg_box.button(QMessageBox.Ok), Qt.LeftButton)

        # make some changes
        doc2 = doc_service.create_new_document("test name 2", "test content 2")

        # import
        self.__form._import_line_edit.setText(export_file_path)
        QTest.mouseClick(self.__form._import_btn, Qt.LeftButton)
        QTest.mouseClick(self.__form._import_warning_msg_box.button(QMessageBox.Ok), Qt.LeftButton)
        QTest.mouseClick(self.__form._import_success_msg_box.button(QMessageBox.Ok), Qt.LeftButton)

        # verify
        docs = DocumentService(WordFellowDB(self.db.db_path)).get_document_list()
        self.assertEqual(docs, [doc1])
