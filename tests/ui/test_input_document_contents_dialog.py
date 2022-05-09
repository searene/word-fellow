import sys
import unittest

from PyQt5.QtCore import Qt
from PyQt5.QtTest import QTest
from PyQt5.QtWidgets import QApplication

from tests.base.BaseTestCase import BaseTestCase
from word_fellow.anki.MockedAnkiService import MockedAnkiService
from word_fellow.domain.document.DocumentService import DocumentService
from word_fellow.domain.document.analyzer.DefaultDocumentAnalyzer import DefaultDocumentAnalyzer
from word_fellow.ui.dialog.document.DocumentDetailDialog import DocumentDetailDialog
from word_fellow.ui.dialog.document.InputDocumentContentsDialog import InputDocumentContentsDialog


class InputDocumentContentsDialogTestCase(BaseTestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.__app = QApplication(sys.argv)

    def setUp(self) -> None:
        super().setUp()
        self.__document_service = DocumentService(self.db)
        analyzer = DefaultDocumentAnalyzer(self.db)
        self.__doc1 = self.__document_service.import_document("test name1", "test contents1", analyzer)
        self.__form = InputDocumentContentsDialog(self.__document_service, DefaultDocumentAnalyzer(self.db), show_ui=False)

    def test_should_import_document_when_clicking_on_ok(self):
        QTest.keyClicks(self.__form._name_line_edit, "test name2")
        QTest.keyClicks(self.__form._contents_text_edit, "test contents2")
        QTest.mouseClick(self.__form._ok_btn, Qt.LeftButton)

        doc_list = self.__document_service.get_document_list()
        self.assertEqual(len(doc_list), 2)
        self.assertEqual(doc_list[1].name, "test name2")
        self.assertEqual(doc_list[1].contents, "test contents2")

    def test_do_not_import_when_name_is_empty(self):
        QTest.keyClicks(self.__form._contents_text_edit, "test contents2")
        QTest.mouseClick(self.__form._ok_btn, Qt.LeftButton)

        doc_list = self.__document_service.get_document_list()
        self.assertEqual(len(doc_list), 1)

    def test_do_not_import_when_contents_is_empty(self):
        QTest.keyClicks(self.__form._name_line_edit, "test name2")
        QTest.mouseClick(self.__form._ok_btn, Qt.LeftButton)

        doc_list = self.__document_service.get_document_list()
        self.assertEqual(len(doc_list), 1)


if __name__ == '__main__':
    unittest.main()
