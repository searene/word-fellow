from unittest.mock import Mock

from base.BaseTestCase import BaseTestCase
from vocab_builder.domain.document.Document import Document
from vocab_builder.domain.status import GlobalWordStatus
from vocab_builder.domain.status.GlobalWordStatus import Status
from vocab_builder.domain.word import WordService, WordFactory
from vocab_builder.domain.word.Word import get_words_by_document_id, Word
from vocab_builder.domain.word.WordService import batch_insert
from vocab_builder.domain.word.WordStatus import WordStatus
from vocab_builder.domain.word.WordValueObject import WordValueObject, WordContext, ShortAndLongContext


class WordTestCase(BaseTestCase):
    def test_batch_insert_with_one_batch(self):
        word_value_objects = [
            WordValueObject("word1", 1, {"word1": [0]}),
            WordValueObject("word2", 1, {"word2": [6, 15]}),
        ]
        db = Mock()

        batch_insert(word_value_objects, db)

        db.execute_script.assert_called_once_with("""BEGIN TRANSACTION;
INSERT INTO words (text, document_id, positions) VALUES
              ('word1',
               1,
               '{"word1": [0]}');
INSERT INTO words (text, document_id, positions) VALUES
              ('word2',
               1,
               '{"word2": [6, 15]}');
COMMIT;""")

    def test_batch_insert_with_two_batches(self):
        word_value_objects = [
            WordValueObject("word1", 1, {"word1": [0]}),
            WordValueObject("word2", 1, {"word2": [6, 15]}),
        ]
        db = Mock()

        batch_insert(word_value_objects, db, max_insert_allowed_in_one_batch=1)

        _, args1, _ = db.mock_calls[0]
        _, args2, _ = db.mock_calls[1]

        self.assertEqual(db.execute_script.call_count, 2)
        self.assertEqual(args1, ("""BEGIN TRANSACTION;
INSERT INTO words (text, document_id, positions) VALUES
              ('word1',
               1,
               '{"word1": [0]}');
COMMIT;""", ))
        self.assertEqual(args2, ("""BEGIN TRANSACTION;
INSERT INTO words (text, document_id, positions) VALUES
              ('word2',
               1,
               '{"word2": [6, 15]}');
COMMIT;""", ))

    def test_get_words_by_document_id(self):
        self.db.insert("""INSERT INTO words (id, text, document_id, positions) VALUES
                  (1, 'word1', 1, '{"word1": [0]}'),
                  (2, 'word2', 1, '{"word2": [6, 15]}')""")

        words = get_words_by_document_id(1, self.db)

        expected_word1 = Word(1, "word1", 1, {"word1": [0]})
        expected_word2 = Word(2, "word2", 1, {"word2": [6, 15]})
        self.assertEqual(words, [expected_word1, expected_word2])

    def test_get_next_unreviewed_word(self):
        # prepare test data
        word_value_object1 = WordValueObject("test1", 1, {"test1": [0]})
        word_value_object2 = WordValueObject("test2", 1, {"test2": [0]})
        WordService.batch_insert([word_value_object1, word_value_object2], self.db)

        # invoke the method
        unreviewed_word = WordFactory.get_next_word(doc_id=1, offset=0, word_status=WordStatus.UNREVIEWED, db=self.db)

        # check result
        self.assertTrue(unreviewed_word.has_same_values(word_value_object1))

    def test_get_next_known_word(self):
        # prepare test data
        word_value_object1 = WordValueObject("test1", 1, {"test1": [0]})
        word_value_object2 = WordValueObject("test2", 1, {"test2": [0]})
        WordService.batch_insert([word_value_object1, word_value_object2], self.db)

        GlobalWordStatus.insert_word_status("test2", Status.KNOWN, self.db)

        # invoke the method
        known_word = WordFactory.get_next_word(doc_id=1, offset=0, word_status=WordStatus.KNOWN, db=self.db)

        # check result
        self.assertTrue(known_word.has_same_values(word_value_object2))

    def test_upsert_word_status_when_we_should_update(self):
        # prepare test data
        word_value_object1 = WordValueObject("test1", 1, {"test1": [0]})
        word_value_object2 = WordValueObject("test2", 1, {"test2": [0]})
        WordService.batch_insert([word_value_object1, word_value_object2], self.db)

        GlobalWordStatus.insert_word_status("test2", Status.KNOWN, self.db)
        GlobalWordStatus.upsert_word_status("test2", Status.STUDYING, self.db)

        # invoke the method
        known_word = WordFactory.get_next_word(doc_id=1, offset=0, word_status=WordStatus.KNOWN, db=self.db)
        studying_word = WordFactory.get_next_word(doc_id=1, offset=0, word_status=WordStatus.STUDYING, db=self.db)

        # check result
        self.assertEqual(known_word, None)
        self.assertTrue(studying_word.has_same_values(word_value_object2))

    def test_upsert_word_status_when_we_should_insert(self):
        # prepare test data
        word_value_object1 = WordValueObject("test1", 1, {"test1": [0]})
        word_value_object2 = WordValueObject("test2", 1, {"test2": [0]})
        WordService.batch_insert([word_value_object1, word_value_object2], self.db)

        GlobalWordStatus.upsert_word_status("test2", Status.STUDYING, self.db)

        # invoke the method
        studying_word = WordFactory.get_next_word(doc_id=1, offset=0, word_status=WordStatus.STUDYING, db=self.db)

        # check result
        self.assertTrue(studying_word.has_same_values(word_value_object2))

    def test_get_next_ignored_word(self):
        # prepare test data
        word_value_object1 = WordValueObject("test1", 1, {"test1": [0]})
        word_value_object2 = WordValueObject("test2", 1, {"test2": [0]})
        WordService.batch_insert([word_value_object1, word_value_object2], self.db)

        GlobalWordStatus.insert_word_status("test1", Status.IGNORED, self.db)

        # invoke the method
        unreviewed_word = WordFactory.get_next_word(doc_id=1, offset=0, word_status=WordStatus.IGNORED, db=self.db)

        # check result
        self.assertTrue(unreviewed_word.has_same_values(word_value_object1))

    def test_get_context_without_exceeding_boundaries(self):
        doc = Document(1, "test doc", "This test is here.")
        word = Word(1, "test", 1, {"test": [5]})

        context = word._get_context(2, doc, "test", 5)

        expected_context = WordContext("test", "s test i", 2)
        self.assertEqual(context, expected_context)

    def test_get_context_with_exceeded_boundaries(self):
        doc = Document(1, "test doc", "This test is here.")
        word = Word(1, "test", 1, {"test": [5]})

        context = word._get_context(100, doc, "test", 5)

        expected_context = WordContext("test", "This test is here.", 5)
        self.assertEqual(context, expected_context)

    def test_get_short_contexts(self):
        doc = Document(1, "test doc", "This test is a test.")
        word = Word(1, "test", 1, {"test": [5, 15]})

        short_and_long_contexts = word.get_short_and_long_contexts(doc)

        expected_context1 = WordContext("test", "This test is a test.", 5)
        expected_context2 = WordContext("test", "This test is a test.", 15)
        expected_short_and_long_contexts1 = ShortAndLongContext(expected_context1, expected_context1)
        expected_short_and_long_contexts2 = ShortAndLongContext(expected_context2, expected_context2)
        self.assertEqual(short_and_long_contexts, [expected_short_and_long_contexts1, expected_short_and_long_contexts2])

    def test_to_html(self):
        word_context = WordContext("test", "abc\n< test \nxyz", 6)

        html = word_context.to_html(allow_multi_line=False)

        self.assertEqual(html, "abc &lt; <b><u>test</u></b>  xyz")