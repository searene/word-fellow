import unittest
from unittest.mock import Mock

from tests.utils import get_test_vocab_builder_db
from vocab_builder.domain.word import WordService, WordFactory
from vocab_builder.domain.word.Word import get_words_by_document_id, Word
from vocab_builder.domain.word.WordService import batch_insert
from vocab_builder.domain.word.WordStatus import WordStatus
from vocab_builder.domain.word.WordValueObject import WordValueObject


class WordTestCase(unittest.TestCase):
    def test_batch_insert_with_one_batch(self):
        word_value_objects = [
            WordValueObject("word1", 1, {"word1": [0]}, False),
            WordValueObject("word2", 1, {"word2": [6, 15]}, False),
        ]
        db = Mock()

        batch_insert(word_value_objects, db)

        db.execute_script.assert_called_once_with("""BEGIN TRANSACTION;
INSERT INTO words (text, document_id, positions, skipped) VALUES
              ('word1',
               1,
               '{"word1": [0]}',
               0);
INSERT INTO words (text, document_id, positions, skipped) VALUES
              ('word2',
               1,
               '{"word2": [6, 15]}',
               0);
COMMIT;""")

    def test_batch_insert_with_two_batches(self):
        word_value_objects = [
            WordValueObject("word1", 1, {"word1": [0]}, False),
            WordValueObject("word2", 1, {"word2": [6, 15]}, False),
        ]
        db = Mock()

        batch_insert(word_value_objects, db, max_insert_allowed_in_one_batch=1)

        _, args1, _ = db.mock_calls[0]
        _, args2, _ = db.mock_calls[1]

        self.assertEqual(db.execute_script.call_count, 2)
        self.assertEqual(args1, ("""BEGIN TRANSACTION;
INSERT INTO words (text, document_id, positions, skipped) VALUES
              ('word1',
               1,
               '{"word1": [0]}',
               0);
COMMIT;""", ))
        self.assertEqual(args2, ("""BEGIN TRANSACTION;
INSERT INTO words (text, document_id, positions, skipped) VALUES
              ('word2',
               1,
               '{"word2": [6, 15]}',
               0);
COMMIT;""", ))

    def test_get_words_by_document_id(self):
        db = get_test_vocab_builder_db()
        db.insert("""INSERT INTO words (id, text, document_id, positions, skipped) VALUES
                  (1, 'word1', 1, '{"word1": [0]}', 0),
                  (2, 'word2', 1, '{"word2": [6, 15]}', 1)""")

        words = get_words_by_document_id(1, db)

        expected_word1 = Word(1, "word1", 1, {"word1": [0]}, False)
        expected_word2 = Word(2, "word2", 1, {"word2": [6, 15]}, True)
        self.assertEqual(words, [expected_word1, expected_word2])

    def test_get_next_unknown_word(self):
        # prepare test data
        db = get_test_vocab_builder_db()
        word_value_object1 = WordValueObject("test1", 1, {"test1": [0]}, True)
        word_value_object2 = WordValueObject("test2", 1, {"test2": [0]}, False)
        WordService.batch_insert([word_value_object1, word_value_object2], db)

        # invoke the method
        unknown_word = WordFactory.get_next_word(doc_id=1, offset=0, word_status=WordStatus.UNKNOWN, db=db)

        # check result
        self.assertTrue(unknown_word.has_same_values(word_value_object2))