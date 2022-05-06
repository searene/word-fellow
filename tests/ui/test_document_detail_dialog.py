import sys

from PyQt5.QtCore import Qt
from PyQt5.QtTest import QTest
from PyQt5.QtWidgets import QMessageBox, QApplication

from base.BaseTestCase import BaseTestCase
from word_fellow.anki.MockedAnkiService import MockedAnkiService
from word_fellow.domain.document.DocumentService import DocumentService
from word_fellow.domain.document.analyzer.DefaultDocumentAnalyzer import DefaultDocumentAnalyzer
from word_fellow.ui.dialog.document.DocumentDetailDialog import DocumentDetailDialog


class DocumentDetailDialogTestCase(BaseTestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.__app = QApplication(sys.argv)

    def setUp(self) -> None:
        super().setUp()
        self.__document_service = DocumentService(self.db)
        analyzer = DefaultDocumentAnalyzer(self.db)
        self.__doc1 = self.__document_service.import_document("test name1", "test contents1", analyzer)
        self.__doc2 = self.__document_service.import_document("test name2", "test contents2", analyzer)
        self.__form = DocumentDetailDialog(None, self.__doc1, self.db, self.__document_service, MockedAnkiService(), show_msg_box=False)

    def test_should_delete_document_when_clicking_on_delete(self):
        QTest.mouseClick(self.__form._deleteBtn, Qt.LeftButton)
        QTest.mouseClick(self.__form._delete_warning_msg_box.button(QMessageBox.Ok), Qt.LeftButton)

        docs = self.__document_service.get_document_list()
        self.assertEqual(docs, [self.__doc2])

    def test_should_not_delete_document_when_clicking_on_cancel(self):
        QTest.mouseClick(self.__form._deleteBtn, Qt.LeftButton)
        QTest.mouseClick(self.__form._delete_warning_msg_box.button(QMessageBox.Cancel), Qt.LeftButton)

        docs = self.__document_service.get_document_list()
        self.assertEqual(docs, [self.__doc1, self.__doc2])
