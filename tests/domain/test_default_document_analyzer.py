import unittest

from tests.utils import get_test_vocab_builder_db
from vocab_builder.domain.document.Document import Document
from vocab_builder.domain.document.DocumentService import DocumentService
from vocab_builder.domain.document.analyzer.DefaultDocumentAnalyzer import DefaultDocumentAnalyzer


class DefaultDocumentAnalyzerTest(unittest.TestCase):

    def test_analyze(self):
        db = get_test_vocab_builder_db()
        document_service = DocumentService(db)
        test_doc = document_service.create_new_document("test_name", "test contents")

        analyzer = DefaultDocumentAnalyzer(db)
        words = analyzer.import_words(test_doc)

        self.assertEqual(len(words), 2)

        self.assertTrue(words[0].word_id is not None)
        self.assertEqual(words[0].text, "test")
        self.assertEqual(words[0].document_id, 1)
        self.assertEqual(words[0].word_to_start_pos_dict, {"test": [0]})
        self.assertEqual(words[0].skipped, False)

        self.assertTrue(words[1].word_id is not None)
        self.assertEqual(words[1].text, "contents")
        self.assertEqual(words[1].document_id, 1)
        self.assertEqual(words[1].word_to_start_pos_dict, {"contents": [5]})
        self.assertEqual(words[1].skipped, False)

    def test_analyze_for_duplicated_words(self):
        """
        Test analyze a document with duplicated words.
        """
        db = get_test_vocab_builder_db()
        document_service = DocumentService(db)
        test_doc = document_service.create_new_document("test_name", "test contents test")

        analyzer = DefaultDocumentAnalyzer(db)
        words = analyzer.import_words(test_doc)

        self.assertEqual(len(words), 2)

        self.assertTrue(words[0].word_id is not None)
        self.assertEqual(words[0].text, "test")
        self.assertEqual(words[0].document_id, 1)
        self.assertEqual(words[0].word_to_start_pos_dict, {"test": [0, 14]})
        self.assertEqual(words[0].skipped, False)

        self.assertTrue(words[1].word_id is not None)
        self.assertEqual(words[1].text, "contents")
        self.assertEqual(words[1].document_id, 1)
        self.assertEqual(words[1].word_to_start_pos_dict, {"contents": [5]})
        self.assertEqual(words[1].skipped, False)
