import unittest
from typing import Optional

from PyQt5.QtTest import QSignalSpy
from aqt import AnkiApp

from anki_testing import anki_running
from tests.utils import get_test_vocab_builder_db
from tests.utils.UiUtils import get_visible_item_widget
from vocab_builder.domain.document.DocumentService import DocumentService
from vocab_builder.domain.document.analyzer.DefaultDocumentAnalyzer import DefaultDocumentAnalyzer
from vocab_builder.domain.word.WordStatus import WordStatus
from vocab_builder.ui.dialog.DocumentWindow import DocumentWindow


class DocumentWindowTestCase(unittest.TestCase):

    def setUp(self):
        self.anki_app: Optional[AnkiApp] = anki_running()
        self.anki_app.__enter__()
        db = get_test_vocab_builder_db()
        document_service = DocumentService(db)
        doc = document_service.import_document("test doc", "this is this this", DefaultDocumentAnalyzer(db))
        self.form = DocumentWindow(doc, db)

    def tearDown(self):
        self.anki_app.__exit__(None, None, None)

    def test_should_give_the_same_contexts_when_switching_status_back(self):
        """Situation: Change the status from unknown to ignored, then to unknown again.
           Expected: The number of contexts in both unknown statuses is the same"""
        short_html1 = [item.short_html for item in get_visible_item_widget(self.form._context_list._list_widget)]
        self.form._status_combo_box.currentTextChanged.emit(WordStatus.IGNORED.name)
        self.form._status_combo_box.currentTextChanged.emit(WordStatus.UNKNOWN.name)
        short_html2 = [item.short_html for item in get_visible_item_widget(self.form._context_list._list_widget)]
        self.assertEqual(short_html1, short_html2)
