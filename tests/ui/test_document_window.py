import sys

from PyQt5.QtCore import Qt
from PyQt5.QtTest import QTest
from PyQt5.QtWidgets import QApplication

from tests.base.BaseTestCase import BaseTestCase
from tests.utils.UiUtils import get_visible_item_widgets
from word_fellow.anki.MockedAnkiService import MockedAnkiService
from word_fellow.domain.document.DocumentService import DocumentService
from word_fellow.domain.document.analyzer.DefaultDocumentAnalyzer import DefaultDocumentAnalyzer
from word_fellow.domain.status import GlobalWordStatus
from word_fellow.domain.status.GlobalWordStatus import Status
from word_fellow.domain.word.WordStatus import WordStatus
from word_fellow.ui.dialog.document.DocumentWindow import DocumentWindow


class DocumentWindowTestCase(BaseTestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.__app = QApplication(sys.argv)

    def setUp(self):
        super(DocumentWindowTestCase, self).setUp()
        self.__document_service = DocumentService(self.db)
        self.doc = self.__document_service.import_document("test doc", "this is this", DefaultDocumentAnalyzer(self.db))
        self.form = DocumentWindow(self.doc, self.db, MockedAnkiService(self.__app))

    def test_should_give_the_same_contexts_when_switching_status_back(self):
        """Situation: Change the status from unreviewed to ignored, then to unreviewed again.
           Expected: The number of contexts in both unreviewed statuses is the same"""
        short_html1 = self.__get_widget_list_htmls()
        self.__change_status(WordStatus.IGNORED)
        self.__change_status(WordStatus.UNREVIEWED)
        short_html2 = self.__get_widget_list_htmls()
        self.assertEqual(short_html1, short_html2)

    def test_should_disable_all_operate_buttons_when_no_word_is_available_at_first(self):
        self.__use_form_with_all_words_studying()

        self.assertFalse(self.form._ignore_btn.isEnabled())
        self.assertFalse(self.form._add_to_anki_btn.isEnabled())
        self.assertFalse(self.form._know_btn.isEnabled())
        self.assertFalse(self.form._study_later_btn.isEnabled())

    def test_should_disable_all_operate_buttons_when_no_word_is_available_after_changing_status(self):
        self.__change_status(WordStatus.IGNORED)
        self.assertFalse(self.form._ignore_btn.isEnabled())
        self.assertFalse(self.form._add_to_anki_btn.isEnabled())
        self.assertFalse(self.form._know_btn.isEnabled())
        self.assertFalse(self.form._study_later_btn.isEnabled())

    def test_should_go_to_next_page_when_clicking_on_ignore(self):
        QTest.mouseClick(self.form._ignore_btn, Qt.LeftButton)
        short_htmls = self.__get_widget_list_htmls()
        self.assertEqual(short_htmls, ["this <b><u>is</u></b> this"])

    def test_should_show_ignored_contexts_when_a_word_is_ignored(self):
        QTest.mouseClick(self.form._ignore_btn, Qt.LeftButton)
        self.__change_status(WordStatus.IGNORED)
        short_htmls = self.__get_widget_list_htmls()
        self.assertEqual(short_htmls, ["<b><u>this</u></b> is this", "this is <b><u>this</u></b>"])

    def test_should_go_to_next_page_when_clicking_on_study_later(self):
        QTest.mouseClick(self.form._study_later_btn, Qt.LeftButton)
        short_htmls = self.__get_widget_list_htmls()
        self.assertEqual(short_htmls, ["this <b><u>is</u></b> this"])

    def test_should_show_study_later_contexts_contexts_when_a_word_is_set_study_later(self):
        QTest.mouseClick(self.form._study_later_btn, Qt.LeftButton)
        self.__change_status(WordStatus.STUDY_LATER)
        short_htmls = self.__get_widget_list_htmls()
        self.assertEqual(short_htmls, ["<b><u>this</u></b> is this", "this is <b><u>this</u></b>"])

    def test_should_go_to_next_page_when_clicking_on_know_it(self):
        QTest.mouseClick(self.form._know_btn, Qt.LeftButton)
        short_htmls = self.__get_widget_list_htmls()
        self.assertEqual(short_htmls, ["this <b><u>is</u></b> this"])

    def test_should_show_known_contexts_when_a_word_is_set_known(self):
        QTest.mouseClick(self.form._know_btn, Qt.LeftButton)
        self.__change_status(WordStatus.KNOWN)
        short_htmls = self.__get_widget_list_htmls()
        self.assertEqual(short_htmls, ["<b><u>this</u></b> is this", "this is <b><u>this</u></b>"])

    def test_click_on_next_page(self):
        QTest.mouseClick(self.form._next_page_btn, Qt.LeftButton)
        short_htmls = self.__get_widget_list_htmls()
        self.assertEqual(short_htmls, ["this <b><u>is</u></b> this"])

    def test_click_on_prev_page(self):
        QTest.mouseClick(self.form._next_page_btn, Qt.LeftButton)
        QTest.mouseClick(self.form._prev_page_btn, Qt.LeftButton)
        short_htmls = self.__get_widget_list_htmls()
        self.assertEqual(short_htmls, ["<b><u>this</u></b> is this", "this is <b><u>this</u></b>"])

    def test_should_disable_prev_btn_if_its_first_page(self):
        self.assertFalse(self.form._prev_page_btn.isEnabled())

    def test_should_disable_next_btn_if_no_word_is_available_in_the_beginning(self):
        self.__use_form_with_all_words_studying()
        self.assertFalse(self.form._next_page_btn.isEnabled())

    def test_should_enable_next_btn_if_there_is_next_page_at_first(self):
        self.assertTrue(self.form._next_page_btn.isEnabled())

    def test_should_enable_next_btn_if_there_is_next_page_after_changing_status(self):
        self.__change_status(WordStatus.IGNORED)
        self.__change_status(WordStatus.UNREVIEWED)
        self.assertTrue(self.form._next_page_btn.isEnabled())

    def test_should_disable_next_btn_if_no_word_is_available_after_changing_status(self):
        for status in [WordStatus.STUDYING, WordStatus.IGNORED, WordStatus.KNOWN]:
            with self.subTest():
                self.__change_status(status)
                self.assertFalse(self.form._next_page_btn.isEnabled())

    def test_should_disable_prev_btn_if_at_first_page_after_changing_status(self):
        QTest.mouseClick(self.form._next_page_btn, Qt.LeftButton)
        for status in [WordStatus.KNOWN, WordStatus.IGNORED, WordStatus.STUDYING]:
            with self.subTest():
                self.__change_status(status)
                self.assertFalse(self.form._prev_page_btn.isEnabled())

    def test_should_disable_next_btn_if_no_word_is_available_after_going_to_next_page(self):
        QTest.mouseClick(self.form._next_page_btn, Qt.LeftButton)
        QTest.mouseClick(self.form._next_page_btn, Qt.LeftButton)
        self.assertFalse(self.form._next_page_btn.isEnabled())

    def test_should_disable_prev_btn_if_at_first_page_after_going_to_prev_page(self):
        QTest.mouseClick(self.form._next_page_btn, Qt.LeftButton)
        QTest.mouseClick(self.form._prev_page_btn, Qt.LeftButton)
        self.assertFalse(self.form._prev_page_btn.isEnabled())

    def test_should_disable_add_to_anki_button_when_current_status_is_studying(self):
        self.__change_status(WordStatus.STUDYING)
        self.assertFalse(self.form._add_to_anki_btn.isEnabled())

    def test_should_disable_ignore_button_when_current_status_is_ignore(self):
        self.__change_status(WordStatus.IGNORED)
        self.assertFalse(self.form._ignore_btn.isEnabled())

    def test_should_disable_study_later_button_when_current_status_is_study_later(self):
        self.__change_status(WordStatus.STUDY_LATER)
        self.assertFalse(self.form._study_later_btn.isEnabled())

    def test_should_disable_know_button_when_current_status_is_known(self):
        self.__change_status(WordStatus.KNOWN)
        self.assertFalse(self.form._know_btn.isEnabled())

    def test_should_display_correct_page_info_when_starting_up(self):
        self.assertEqual(self.form._page_info_label.text(), "1 / 2")

    def test_should_display_empty_page_info_when_there_is_no_word_when_starting_up(self):
        self.__use_form_with_all_words_studying()
        self.assertEqual(self.form._page_info_label.text(), "- / -")

    def test_should_display_correct_page_info_after_changing_status(self):
        self.__change_status(WordStatus.STUDYING)
        self.assertEqual(self.form._page_info_label.text(), "- / -")

    def test_should_display_correct_page_info_after_going_to_next_page(self):
        QTest.mouseClick(self.form._next_page_btn, Qt.LeftButton)
        self.assertEqual(self.form._page_info_label.text(), "2 / 2")

    def test_should_display_correct_page_info_when_clicking_on_add_to_anki_btn(self):
        QTest.mouseClick(self.form._add_to_anki_btn, Qt.LeftButton)
        self.assertEqual(self.form._page_info_label.text(), "1 / 1")

    def test_should_display_correct_page_info_when_clicking_on_ignore_btn(self):
        QTest.mouseClick(self.form._ignore_btn, Qt.LeftButton)
        self.assertEqual(self.form._page_info_label.text(), "1 / 1")

    def test_should_display_correct_page_info_when_clicking_on_know_btn(self):
        QTest.mouseClick(self.form._know_btn, Qt.LeftButton)
        self.assertEqual(self.form._page_info_label.text(), "1 / 1")

    def test_should_display_correct_page_info_when_clicking_on_study_later_btn(self):
        QTest.mouseClick(self.form._study_later_btn, Qt.LeftButton)
        self.assertEqual(self.form._page_info_label.text(), "1 / 1")

    def test_should_disable_next_page_btn_when_we_are_at_last_page(self):
        QTest.mouseClick(self.form._next_page_btn, Qt.LeftButton)
        self.assertFalse(self.form._next_page_btn.isEnabled())

    def test_should_show_correct_word_label_when_starting_up(self):
        self.assertEqual(self.form._word_label.text(), "this")

    def test_should_show_dashes_when_there_are_no_words(self):
        self.__change_status(WordStatus.STUDYING)
        self.assertEqual(self.form._word_label.text(), "--")

    def test_should_change_word_label_when_clicking_on_next_page(self):
        QTest.mouseClick(self.form._next_page_btn, Qt.LeftButton)
        self.assertEqual(self.form._word_label.text(), "is")

    def test_should_go_to_last_page_if_there_is_no_word_at_current_page_after_clicking_on_operating_buttons(self):
        QTest.mouseClick(self.form._next_page_btn, Qt.LeftButton)
        QTest.mouseClick(self.form._ignore_btn, Qt.LeftButton)
        self.assertEqual(self.form._word_label.text(), "this")

    def test_should_undo_ignored_word_when_clicking_on_undo_btn(self):
        QTest.mouseClick(self.form._ignore_btn, Qt.LeftButton)
        self.form._undo_action.trigger()
        self.assertEqual(self.form._word_label.text(), "this")

        # Change to the ignored section
        self.__change_status(WordStatus.IGNORED)
        # There should be no word
        self.assertEqual(self.form._word_label.text(), "--")

    def test_should_undo_known_word_when_clicking_on_undo_btn(self):
        QTest.mouseClick(self.form._know_btn, Qt.LeftButton)
        self.form._undo_action.trigger()
        self.assertEqual(self.form._word_label.text(), "this")

        # Change to the ignored section
        self.__change_status(WordStatus.KNOWN)
        # There should be no word
        self.assertEqual(self.form._word_label.text(), "--")

    def test_should_undo_study_later_word_when_clicking_on_undo_btn(self):
        QTest.mouseClick(self.form._study_later_btn, Qt.LeftButton)
        self.form._undo_action.trigger()
        self.assertEqual(self.form._word_label.text(), "this")
        self.__change_status(WordStatus.STUDY_LATER)
        self.assertEqual(self.form._word_label.text(), "--")

    def test_should_undo_added_to_anki_when_clicking_on_undo_btn(self):
        QTest.mouseClick(self.form._add_to_anki_btn, Qt.LeftButton)
        self.form._undo_action.trigger()
        self.assertEqual(self.form._word_label.text(), "this")
        self.__change_status(WordStatus.STUDYING)
        self.assertEqual(self.form._word_label.text(), "--")

    def test_should_undo_known_when_clicking_on_undo_btn_and_current_status_is_ignored(self):

        # Ignore the word
        QTest.mouseClick(self.form._ignore_btn, Qt.LeftButton)

        # Set the word as known
        self.__change_status(WordStatus.IGNORED)
        QTest.mouseClick(self.form._know_btn, Qt.LeftButton)

        self.form._undo_action.trigger()

        self.assertEqual(self.form._word_label.text(), "this")

        self.__change_status(WordStatus.KNOWN)
        self.assertEqual(self.form._word_label.text(), "--")

    # def test_should_update_everything_when_reopening(self):
    #
    #     # Make some changes
    #     QTest.mouseClick(self.form._ignore_btn, Qt.LeftButton)
    #     QTest.mouseClick(self.form._ignore_btn, Qt.LeftButton)
    #     self.__change_status(WordStatus.IGNORED)
    #
    #     # Reopen
    #     doc = self.__document_service.import_document("test doc2", "another test doc", DefaultDocumentAnalyzer(self.db))
    #     self.form.reopen(None, doc, self.db, MockedAnkiService(self.__app))
    #
    #     # Verify
    #     self.assertEqual(self.form._word_label.text(), "another")
    #
    #     self.assertEqual(self.form._status_combo_box.currentText(), WordStatus.UNREVIEWED.value)
    #
    #     self.assertTrue(self.form._ignore_btn.isEnabled())
    #     self.assertTrue(self.form._know_btn.isEnabled())
    #     self.assertTrue(self.form._study_later_btn.isEnabled())
    #     self.assertTrue(self.form._add_to_anki_btn.isEnabled())
    #
    #     self.assertFalse(self.form._prev_page_btn.isEnabled())
    #     self.assertTrue(self.form._next_page_btn.isEnabled())
    #     self.assertEqual(self.form._page_info_label.text(), "1 / 3")
    #
    #     self.assertEqual(self.form._context_list.get_item_htmls(), [
    #         "<b><u>another</u></b> test doc"
    #     ])

    def __get_widget_list_htmls(self):
        return [item.short_html for item in get_visible_item_widgets(self.form._context_list._list_widget)]

    def __change_status(self, status: WordStatus) -> None:
        self.form._status_combo_box.currentTextChanged.emit(status.value)

    def __use_form_with_all_words_studying(self) -> None:
        document_service = DocumentService(self.db)
        document_service.remove_all_documents_and_words()
        self.doc = document_service.import_document("test doc", "this is this", DefaultDocumentAnalyzer(self.db))
        GlobalWordStatus.upsert_word_status("this", Status.STUDYING, self.db)
        GlobalWordStatus.upsert_word_status("is", Status.STUDYING, self.db)
        self.form = DocumentWindow(self.doc, self.db, MockedAnkiService(self.__app))
