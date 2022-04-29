import unittest
from typing import Optional

from PyQt5.QtTest import QSignalSpy
from aqt import AnkiApp

from anki_testing import anki_running
from tests.utils import get_test_vocab_builder_db
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

    def test_should_give_the_same_number_of_contexts_when_switching_back(self):
        """Situation: Change the status from unknown to ignored, then to unknown.
           Expected: The number of contexts in both unknown statuses is the same"""
        unknown_item_texts1 = self.form._context_list.get_item_htmls()
        self.form._status_combo_box.currentTextChanged.emit(WordStatus.IGNORED.name)
        self.form._status_combo_box.currentTextChanged.emit(WordStatus.UNKNOWN.name)
        unknown_item_texts2 = self.form._context_list.get_item_htmls()
        self.assertEqual(unknown_item_texts1, unknown_item_texts2)
