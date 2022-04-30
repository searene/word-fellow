import unittest
from typing import Optional

from PyQt5.QtCore import Qt
from PyQt5.QtTest import QSignalSpy, QTest
from aqt import AnkiApp

from tests.anki_testing import anki_running
from tests.utils import get_test_vocab_builder_db
from tests.utils.UiUtils import get_visible_item_widget
from vocab_builder.domain.document.DocumentService import DocumentService
from vocab_builder.domain.document.analyzer.DefaultDocumentAnalyzer import DefaultDocumentAnalyzer
from vocab_builder.domain.status import GlobalWordStatus
from vocab_builder.domain.status.GlobalWordStatus import Status
from vocab_builder.domain.word.WordStatus import WordStatus
from vocab_builder.ui.dialog.DocumentWindow import DocumentWindow


class DocumentWindowTestCase(unittest.TestCase):

    def setUp(self):
        self.anki_app: Optional[AnkiApp] = anki_running()
        self.anki_app.__enter__()
        self.__db = get_test_vocab_builder_db()
        document_service = DocumentService(self.__db)
        self.__doc = document_service.import_document("test doc", "this is this", DefaultDocumentAnalyzer(self.__db))
        self.form = DocumentWindow(self.__doc, self.__db)

    def tearDown(self):
        self.anki_app.__exit__(None, None, None)

    def test_should_give_the_same_contexts_when_switching_status_back(self):
        """Situation: Change the status from unknown to ignored, then to unknown again.
           Expected: The number of contexts in both unknown statuses is the same"""
        short_html1 = self.__get_widget_list_htmls()
        self.form._status_combo_box.currentTextChanged.emit(WordStatus.IGNORED.name)
        self.form._status_combo_box.currentTextChanged.emit(WordStatus.UNKNOWN.name)
        short_html2 = self.__get_widget_list_htmls()
        self.assertEqual(short_html1, short_html2)

    def test_should_go_to_next_page_when_clicking_on_ignore(self):
        QTest.mouseClick(self.form._ignore_bnt, Qt.LeftButton)
        short_htmls = self.__get_widget_list_htmls()
        self.assertEqual(short_htmls, ["this <b>is</b> this"])

    def test_should_show_ignored_contexts_when_a_word_is_ignored(self):
        QTest.mouseClick(self.form._ignore_bnt, Qt.LeftButton)
        self.form._status_combo_box.currentTextChanged.emit(WordStatus.IGNORED.name)
        short_htmls = self.__get_widget_list_htmls()
        self.assertEqual(short_htmls, ["<b>this</b> is this", "this is <b>this</b>"])

    def test_should_go_to_next_page_when_clicking_on_study_later(self):
        QTest.mouseClick(self.form._study_later_btn, Qt.LeftButton)
        short_htmls = self.__get_widget_list_htmls()
        self.assertEqual(short_htmls, ["this <b>is</b> this"])

    def test_should_show_study_later_contexts_contexts_when_a_word_is_set_study_later(self):
        QTest.mouseClick(self.form._study_later_btn, Qt.LeftButton)
        self.form._status_combo_box.currentTextChanged.emit(WordStatus.STUDY_LATER.name)
        short_htmls = self.__get_widget_list_htmls()
        self.assertEqual(short_htmls, ["<b>this</b> is this", "this is <b>this</b>"])

    def test_should_go_to_next_page_when_clicking_on_know_it(self):
        QTest.mouseClick(self.form._know_btn, Qt.LeftButton)
        short_htmls = self.__get_widget_list_htmls()
        self.assertEqual(short_htmls, ["this <b>is</b> this"])

    def test_should_show_known_contexts_when_a_word_is_set_known(self):
        QTest.mouseClick(self.form._know_btn, Qt.LeftButton)
        self.form._status_combo_box.currentTextChanged.emit(WordStatus.KNOWN.name)
        short_htmls = self.__get_widget_list_htmls()
        self.assertEqual(short_htmls, ["<b>this</b> is this", "this is <b>this</b>"])

    def test_click_on_next_page(self):
        QTest.mouseClick(self.form._next_page_btn, Qt.LeftButton)
        short_htmls = self.__get_widget_list_htmls()
        self.assertEqual(short_htmls, ["this <b>is</b> this"])

    def test_click_on_prev_page(self):
        QTest.mouseClick(self.form._next_page_btn, Qt.LeftButton)
        QTest.mouseClick(self.form._prev_page_btn, Qt.LeftButton)
        short_htmls = self.__get_widget_list_htmls()
        self.assertEqual(short_htmls, ["<b>this</b> is this", "this is <b>this</b>"])

    def test_should_disable_prev_btn_if_its_first_page(self):
        self.assertFalse(self.form._prev_page_btn.isEnabled())

    def test_should_disable_next_btn_if_no_word_is_available_in_the_beginning(self):
        document_service = DocumentService(self.__db)
        document_service.remove_all()
        doc = document_service.import_document("test doc", "this is this", DefaultDocumentAnalyzer(self.__db))
        GlobalWordStatus.upsert_word_status("this", Status.STUDYING, self.__db)
        GlobalWordStatus.upsert_word_status("is", Status.STUDYING, self.__db)
        form = DocumentWindow(doc, self.__db)
        self.assertFalse(form._next_page_btn.isEnabled())

    def test_should_disable_next_btn_if_no_word_is_available_after_changing_status(self):
        for status in [WordStatus.STUDYING, WordStatus.IGNORED, WordStatus.KNOWN]:
            with self.subTest():
                self.form._status_combo_box.currentTextChanged.emit(status.name)
                self.assertFalse(self.form._next_page_btn.isEnabled())

    def test_should_disable_prev_btn_if_at_first_page_after_changing_status(self):
        QTest.mouseClick(self.form._next_page_btn, Qt.LeftButton)
        for status in [WordStatus.KNOWN, WordStatus.IGNORED, WordStatus.STUDYING]:
            with self.subTest():
                self.form._status_combo_box.currentTextChanged.emit(status.name)
                self.assertFalse(self.form._prev_page_btn.isEnabled())

    def __get_widget_list_htmls(self):
        return [item.short_html for item in get_visible_item_widget(self.form._context_list._list_widget)]
