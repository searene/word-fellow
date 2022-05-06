import unittest

from base.BaseTestCase import BaseTestCase
from word_fellow.domain.document.DocumentService import DocumentService
from word_fellow.domain.document.analyzer.DefaultDocumentAnalyzer import DefaultDocumentAnalyzer


class DefaultDocumentAnalyzerTest(BaseTestCase):

    def test_analyze(self):
        document_service = DocumentService(self.db)
        test_doc = document_service.create_new_document("test_name", "test contents")

        analyzer = DefaultDocumentAnalyzer(self.db)
        words = analyzer.import_words(test_doc)

        self.assertEqual(len(words), 2)

        self.assertTrue(words[0].word_id is not None)
        self.assertEqual(words[0].text, "test")
        self.assertEqual(words[0].document_id, 1)
        self.assertEqual(words[0].word_to_start_pos_dict, {"test": [0]})

        self.assertTrue(words[1].word_id is not None)
        self.assertEqual(words[1].text, "contents")
        self.assertEqual(words[1].document_id, 1)
        self.assertEqual(words[1].word_to_start_pos_dict, {"contents": [5]})

    def test_analyze_for_duplicated_words(self):
        """
        Test analyze a document with duplicated words.
        """
        document_service = DocumentService(self.db)
        test_doc = document_service.create_new_document("test_name", "test contents test")

        analyzer = DefaultDocumentAnalyzer(self.db)
        words = analyzer.import_words(test_doc)

        self.assertEqual(len(words), 2)

        self.assertTrue(words[0].word_id is not None)
        self.assertEqual(words[0].text, "test")
        self.assertEqual(words[0].document_id, 1)
        self.assertEqual(words[0].word_to_start_pos_dict, {"test": [0, 14]})

        self.assertTrue(words[1].word_id is not None)
        self.assertEqual(words[1].text, "contents")
        self.assertEqual(words[1].document_id, 1)
        self.assertEqual(words[1].word_to_start_pos_dict, {"contents": [5]})
