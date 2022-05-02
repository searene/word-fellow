import unittest

from tests.utils import get_test_vocab_builder_db
from vocab_builder.domain.document.Document import Document
from vocab_builder.domain.document.DocumentService import DocumentService
from vocab_builder.domain.document.analyzer.DefaultDocumentAnalyzer import DefaultDocumentAnalyzer


class DocumentServiceTestCase(unittest.TestCase):

    def test_should_get_imported_document(self):
        db = get_test_vocab_builder_db()
        document_service = DocumentService(db)

        document_name = "test document"
        document_contents = "test contents"
        document_service.import_document(document_name, document_contents, DefaultDocumentAnalyzer(db))

        documents = document_service.get_document_list()
        self.assertEqual(len(documents), 1)
        self.assertEqual(documents[0].name, document_name)
        self.assertEqual(documents[0].contents, document_contents)

    def test_should_get_documents_after_creating_them(self):
        db = get_test_vocab_builder_db()
        document_service = DocumentService(db)

        document1 = document_service.create_new_document("test_document_name_1", "test_document_contents_1")
        document2 = document_service.create_new_document("test_document_name_2", "test_document_contents_2")

        document_list = document_service.get_document_list()

        self.assertEqual(len(document_list), 2)
        self.assertEqual(document_list[0], document1)
        self.assertEqual(document_list[1], document2)

    def test_should_remove_all_documents(self):

        # prepare
        db = get_test_vocab_builder_db()
        document_service = DocumentService(db)
        document1 = document_service.create_new_document("test_document_name_1", "test_document_contents_1")
        document2 = document_service.create_new_document("test_document_name_2", "test_document_contents_2")

        # invoke
        document_service.remove_all()

        # check
        document_list = document_service.get_document_list()
        self.assertEqual(len(document_list), 0)


if __name__ == '__main__':
    unittest.main()
