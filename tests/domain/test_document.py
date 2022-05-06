from tests.base.BaseTestCase import BaseTestCase
from word_fellow.domain.document.DocumentService import DocumentService


class DocumentTestCase(BaseTestCase):

    def test_should_create_document(self):
        DocumentService(self.db).init_database()

        cnt = self.db.first("select count(*) from documents")
        self.assertEqual(cnt, (0,))