import unittest
from unittest.mock import Mock, call, patch

from vocab_builder.domain.word.WordService import batch_insert
from vocab_builder.domain.word.WordValueObject import WordValueObject


class WordTestCase(unittest.TestCase):
    def test_batch_insert(self):
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
               'N');
INSERT INTO words (text, document_id, positions, skipped) VALUES
              ('word2',
               1,
               '{"word2": [6, 15]}',
               'N');
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
               'N');
COMMIT;""", ))
        self.assertEqual(args2, ("""BEGIN TRANSACTION;
INSERT INTO words (text, document_id, positions, skipped) VALUES
              ('word2',
               1,
               '{"word2": [6, 15]}',
               'N');
COMMIT;""", ))
