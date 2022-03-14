import json
from typing import List

from vocab_builder.domain.word.Word import Word
from vocab_builder.domain.word.WordValueObject import WordValueObject
from vocab_builder.infrastructure import VocabBuilderDB
from vocab_builder.infrastructure.utils import DBUtils


# TODO remove it
def save_words(words: [Word]):
    pass


def batch_insert(words: List[WordValueObject], db: VocabBuilderDB, max_insert_allowed_in_one_batch=500) -> None:
    pos = 0

    while True:
        script = __get_insert_script(words, pos, pos + max_insert_allowed_in_one_batch)
        db.execute_script(script)

        # next starting pos
        pos = pos + max_insert_allowed_in_one_batch

        if pos >= len(words):
            break


def __get_insert_sql(word: WordValueObject) -> str:
    return f"""INSERT INTO words (text, document_id, positions, skipped) VALUES
              ('{DBUtils.escape_for_sql_statement(word.text)}',
               {word.document_id},
               '{DBUtils.escape_for_sql_statement(json.dumps(word.word_to_start_pos_dict))}',
               {1 if word.skipped else 0});"""


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
