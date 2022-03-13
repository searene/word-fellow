import unittest

from tests.utils import get_test_vocab_builder_db
from vocab_builder.domain.document.Document import Document
from vocab_builder.domain.document.analyzer.DefaultDocumentAnalyzer import DefaultDocumentAnalyzer


class DefaultDocumentAnalyzerTest(unittest.TestCase):

    def test_analyze(self):
        test_document = Document(1, "test doc", "test contents")

        analyzer = DefaultDocumentAnalyzer(get_test_vocab_builder_db())
        words = analyzer.analyze(test_document)

        self.assertEqual(len(words), 3)

        self.assertEqual(words[0].text, "test")
        self.assertEqual(words[0].document_id, 1)
        self.assertEqual(words[0].word_to_start_pos_dict, {"test": 0})
        self.assertEqual(words[0].skipped, False)

        self.assertEqual(words[1].text, "contents")
        self.assertEqual(words[1].document_id, 1)
        self.assertEqual(words[1].word_to_start_pos_dict, {"contents": 5})
        self.assertEqual(words[1].skipped, False)

    def test_analyze_for_duplicated_words(self):
        """
        Test analyze a document with duplicated words.
        # TODO
        """
        pass