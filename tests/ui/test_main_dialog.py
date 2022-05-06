import sys
import time

from PyQt5.QtCore import Qt
from PyQt5.QtTest import QTest
from PyQt5.QtWidgets import QApplication, QListWidgetItem, QMessageBox

from tests.base.BaseTestCase import BaseTestCase
from tests.utils.UiUtils import get_visible_items
from word_fellow.anki.MockedAnkiService import MockedAnkiService
from word_fellow.domain.document.DocumentService import DocumentService
from word_fellow.domain.document.analyzer.DefaultDocumentAnalyzer import DefaultDocumentAnalyzer
from word_fellow.ui.dialog.MainDialog import MainDialog


class MainDialogTestCase(BaseTestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.__app = QApplication(sys.argv)

    def setUp(self) -> None:
        super().setUp()

        self.__document_service = DocumentService(self.db)
        analyzer = DefaultDocumentAnalyzer(self.db)
        self.__doc1 = self.__document_service.import_document("test name1", "this is this this", analyzer)
        self.__doc2 = self.__document_service.import_document("test name2", "skip\nto skip\nthis", analyzer)

        self.__form = MainDialog(self.db, MockedAnkiService(), show_dialog=False)

    def test_should_remove_deleted_document_from_list(self):
        item1 = list(filter(lambda item: item.text() == self.__doc1.name, get_visible_items(self.__form._list_widget)))[0]
        self.__form._list_widget.itemClicked.emit(item1)
        QTest.mouseClick(self.__form._doc_detail_dialog._delete_btn, Qt.LeftButton)
        QTest.mouseClick(self.__form._doc_detail_dialog._delete_warning_msg_box.button(QMessageBox.Ok), Qt.LeftButton)

        items = get_visible_items(self.__form._list_widget)
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0].text(), self.__doc2.name)