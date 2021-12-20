import unittest

from tests.utils import get_test_session
from vocab_builder.domain.document.DocumentFactory import DocumentFactory


class DocumentFactoryTestCase(unittest.TestCase):

    def test_should_get_documents_after_creating_them(self):
        session = get_test_session()
        document_factory = DocumentFactory(session)
        document1 = document_factory.create_new_document("test_document_name_1", "test_document_contents_1")
        document2 = document_factory.create_new_document("test_document_name_2", "test_document_contents_2")

        document_list = document_factory.get_document_list()

        self.assertEqual(len(document_list), 2)
        self.assertEqual(document_list[0], document1)
        self.assertEqual(document_list[1], document2)


if __name__ == '__main__':
    unittest.main()
