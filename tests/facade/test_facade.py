import unittest

from sqlalchemy import create_engine

from facade.Facade import Facade


class FacadeTestCase(unittest.TestCase):

    engine = create_engine('sqlite:///:memory:', echo=True)

    # def test_get_next_word(self):
    #     document_facade = DocumentFacade()
    #     document_id = 1
    #     next_word = "test"
    #     context = WordContext("Fake test contents", 5, 8)
    #
    #     document_word: DocumentWord = document_facade.get_next_unknown_word(document_id)
    #
    #     self.assertEqual(document_word.word, next_word)
    #     self.assertEqual(len(document_word.contexts), 1)
    #     self.assertEqual(document_word.contexts[0], context)

    def test_should_get_created_documents(self):
        facade = Facade(sql_engine=FacadeTestCase.engine)
        document = facade.create_new_document("test document")
        documents = facade.get_document_list()
        self.assertEqual(len(documents), 1)
        self.assertEqual(documents[0], document)


if __name__ == '__main__':
    unittest.main()
