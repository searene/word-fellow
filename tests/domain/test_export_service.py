import os
import tempfile

from tests.base.BaseTestCase import BaseTestCase
from word_fellow.domain.document.DocumentService import DocumentService
from word_fellow.domain.export.ExportService import ExportService
from word_fellow.domain.export.ImportService import ImportService
from word_fellow.infrastructure import WordFellowDB


class ExportServiceTestCase(BaseTestCase):

    def setUp(self) -> None:
        super().setUp()
        self.__export_service = ExportService(self.db)
        self.__import_service = ImportService(self.db)

    def test_export_and_import(self):
        # initialize the database
        doc_service = DocumentService(self.db)
        doc1 = doc_service.create_new_document("test name", "test content")

        # export
        tmp_dir = tempfile.mkdtemp()
        export_path = os.path.join(tmp_dir, "export.db")
        self.__export_service.export(export_path)

        # make some changes
        doc2 = doc_service.create_new_document("test name 2", "test content 2")

        # import
        self.__import_service.do_import(export_path)

        # verify
        new_doc_service = DocumentService(WordFellowDB(self.db.db_path))
        doc_list = new_doc_service.get_document_list()
        self.assertEqual([doc1], doc_list)
