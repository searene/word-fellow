import unittest

from tests.utils import get_test_vocab_builder_db
from vocab_builder.domain.document.DocumentService import DocumentService


class DocumentTestCase(unittest.TestCase):

    def test_should_create_document(self):
        db = get_test_vocab_builder_db()

        DocumentService(db).init_database()

        cnt = db.first("select count(*) from documents")
        self.assertEqual(cnt, (0,))