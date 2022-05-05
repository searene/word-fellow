import unittest

from base.BaseTestCase import BaseTestCase
from vocab_builder.domain.document.DocumentService import DocumentService
from vocab_builder.domain.document.analyzer.DefaultDocumentAnalyzer import DefaultDocumentAnalyzer


class DocumentServiceTestCase(BaseTestCase):

    def test_should_get_imported_document(self):
        document_service = DocumentService(self.db)

        document_name = "test document"
        document_contents = "test contents"
        document_service.import_document(document_name, document_contents, DefaultDocumentAnalyzer(self.db))

        documents = document_service.get_document_list()
        self.assertEqual(len(documents), 1)
        self.assertEqual(documents[0].name, document_name)
        self.assertEqual(documents[0].contents, document_contents)

    def test_should_get_documents_after_creating_them(self):
        document_service = DocumentService(self.db)

        document1 = document_service.create_new_document("test_document_name_1", "test_document_contents_1")
        document2 = document_service.create_new_document("test_document_name_2", "test_document_contents_2")

        document_list = document_service.get_document_list()

        self.assertEqual(len(document_list), 2)
        self.assertEqual(document_list[0], document1)
        self.assertEqual(document_list[1], document2)

    def test_should_remove_all_documents(self):

        # prepare
        document_service = DocumentService(self.db)
        document1 = document_service.create_new_document("test_document_name_1", "test_document_contents_1")
        document2 = document_service.create_new_document("test_document_name_2", "test_document_contents_2")

        # invoke
        document_service.remove_all_documents_and_words()

        # check
        document_list = document_service.get_document_list()
        self.assertEqual(len(document_list), 0)


if __name__ == '__main__':
    unittest.main()
