import unittest

from tests.utils import get_test_sqlite_url
from vocab_builder.domain.document.Document import Document
from vocab_builder.domain.document.DocumentService import DocumentService
from vocab_builder.infrastructure.VocabBuilderDB import VocabBuilderDB


class DocumentTestCase(unittest.TestCase):

    def test_should_create_document(self):
        sqlite_url = get_test_sqlite_url()
        db = VocabBuilderDB(sqlite_url)

        DocumentService(db).init_database()

        cnt = db.first("select count(*) from documents")
        self.assertEqual(cnt, (0,))