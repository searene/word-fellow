import unittest

from base.BaseTestCase import BaseTestCase
from vocab_builder.domain.document.DocumentService import DocumentService
from vocab_builder.domain.document.analyzer.DefaultDocumentAnalyzer import DefaultDocumentAnalyzer


class DocumentServiceTestCase(BaseTestCase):

    def setUp(self) -> None:
        super(DocumentServiceTestCase, self).setUp()
        self.__document_service = DocumentService(self.db)
        analyzer = DefaultDocumentAnalyzer(self.db)
        self.__doc1 = self.__document_service.import_document("test name1", "test contents1", analyzer)
        self.__doc2 = self.__document_service.import_document("test name2", "test contents2", analyzer)

    def test_get_document_id_and_name_list(self):
        doc_id_and_name_list = self.__document_service.get_document_id_and_name_list()
        self.assertEqual(len(doc_id_and_name_list), 2)
        self.assertTrue((self.__doc1.document_id, self.__doc1.name) in doc_id_and_name_list)
        self.assertTrue((self.__doc2.document_id, self.__doc2.name) in doc_id_and_name_list)

    def test_get_document_by_id(self):
        doc = self.__document_service.get_doc_by_id(self.__doc1.document_id)
        self.assertEqual(doc, self.__doc1)

    def test_delete_doc_and_words(self):
        self.__document_service.delete_doc_and_words(self.__doc1.document_id)

        documents = self.__document_service.get_document_list()
        self.assertEqual(documents, [self.__doc2])