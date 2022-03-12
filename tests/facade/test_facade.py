import unittest
import json

from sqlalchemy import create_engine

from vocab_builder.domain.word.Word import WordStatus
from vocab_builder.domain.document.analyzer.en.TraceOriginDocumentAnalyzer import TraceOriginDocumentAnalyzer
from vocab_builder.facade.Facade import Facade


class FacadeTestCase(unittest.TestCase):

    __engine = create_engine('sqlite:///:memory:', echo=True)
    __facade = Facade(sql_engine=__engine)


    def test_should_get_words_after_importing_document(self):
        facade = FacadeTestCase.__facade
        self.__import_test_document("known")
        document_name = "test document"
        document_contents = "test contents tests known"
        document = facade.import_document(document_name, document_contents, TraceOriginDocumentAnalyzer())

        word = facade.get_next_unknown_word(document)

        self.assertEqual(word.text, "test")
        self.assertEqual(word.document_id, document.id)
        self.assertEqual(word.positions, json.dumps([{"key": "test", "positions": [0, 14]}]))
        self.assertEqual(word.status, WordStatus.UNKNOWN)

    def __import_test_document(self, contents: str):
        FacadeTestCase.__facade.import_document("test document", contents, TraceOriginDocumentAnalyzer())


if __name__ == '__main__':
    unittest.main()
