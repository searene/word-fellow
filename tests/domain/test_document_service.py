import unittest

from tests.utils import get_test_vocab_builder_db
from vocab_builder.domain.document.DocumentService import DocumentService


class DocumentServiceTestCase(unittest.TestCase):

    def setUp(self) -> None:
        db = get_test_vocab_builder_db()
        self.__document_service = DocumentService(db)
        self.__doc1 = self.__document_service.create_new_document("test name1", "test contents1")
        self.__doc2 = self.__document_service.create_new_document("test name2", "test contents2")

    def test_get_document_id_and_name_list(self):
        doc_id_and_name_list = self.__document_service.get_document_id_and_name_list()
        self.assertEqual(len(doc_id_and_name_list), 2)
        self.assertTrue((self.__doc1.document_id, self.__doc1.name) in doc_id_and_name_list)
        self.assertTrue((self.__doc2.document_id, self.__doc2.name) in doc_id_and_name_list)
