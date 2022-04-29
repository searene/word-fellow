import unittest
from typing import Optional

from aqt import AnkiApp

from anki_testing import anki_running
from tests.utils import get_test_vocab_builder_db
from vocab_builder.domain.document.DocumentService import DocumentService
from vocab_builder.domain.document.analyzer.DefaultDocumentAnalyzer import DefaultDocumentAnalyzer
from vocab_builder.ui.dialog.DocumentWindow import DocumentWindow


class DocumentWindowTestCase(unittest.TestCase):

    def setUp(self):
        self.anki_app: Optional[AnkiApp] = anki_running()
        self.anki_app.__enter__()
        db = get_test_vocab_builder_db()
        document_service = DocumentService(db)
        doc = document_service.import_document("test doc", "This is a test doc", DefaultDocumentAnalyzer(db))
        self.form = DocumentWindow(doc, db)

    def tearDown(self):
        self.anki_app.__exit__(None, None, None)

    def test_ignore_and_change_status(self):
        self.assertEqual(self.form._status_combo_box.currentText(), "UNKNOWN")