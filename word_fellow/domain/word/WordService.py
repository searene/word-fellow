import json
from typing import List, Tuple

from word_fellow.domain.word.Word import Word
from word_fellow.domain.word.WordValueObject import WordValueObject
from word_fellow.infrastructure import WordFellowDB
from word_fellow.infrastructure.utils import DBUtils


def batch_insert(words: List[WordValueObject], db: WordFellowDB, max_insert_allowed_in_one_batch=500) -> None:
    pos = 0

    while True:
        script = __get_insert_script(words, pos, pos + max_insert_allowed_in_one_batch)
        db.execute_script(script)

        # next starting pos
        pos = pos + max_insert_allowed_in_one_batch

        if pos >= len(words):
            break


def __get_insert_sql(word: WordValueObject) -> str:
    return f"""INSERT INTO words (text, document_id, positions) VALUES
              ('{DBUtils.escape_for_sql_statement(word.text)}',
               {word.document_id},
               '{DBUtils.escape_for_sql_statement(json.dumps(word.word_to_start_pos_dict))}');"""


def __get_insert_script(words: [WordValueObject], start: int, end: int) -> str:
    script = "BEGIN TRANSACTION;\n"
    pos = start
    while pos < len(words) and pos < end:
        sql = __get_insert_sql(words[pos])
        script += sql
        script += "\n"
        pos += 1
    script += "COMMIT;"
    return script


def init_database(db: WordFellowDB):
    db.execute("""
    CREATE TABLE IF NOT EXISTS words (
        id INTEGER PRIMARY KEY,
        text TEXT NOT NULL,
        document_id INTEGER NOT NULL,
        positions TEXT NOT NULL
    )
    """)


def get_words_by_document_id(document_id, db: WordFellowDB) -> [Word]:
    words_data_objects = db.fetch_all("""SELECT * from words WHERE document_id = ?""", (document_id,))
    return convert_word_data_objects_to_words(words_data_objects)


def convert_word_data_objects_to_words(word_data_objects: List[Tuple]) -> List[Word]:
    return [convert_word_data_object_to_word(word_data_object)
            for word_data_object in word_data_objects]


def convert_word_data_object_to_word(word_data_object: Tuple) -> Word:
    word_id = word_data_object[0]
    text = word_data_object[1]
    document_id = word_data_object[2]
    word_to_start_pos_dict = json.loads(word_data_object[3])
    return Word(word_id, text, document_id, word_to_start_pos_dict)
