from typing import Optional

import word_fellow.domain.word.Word
import word_fellow.domain.word.WordService
from word_fellow.domain.word.Word import Word
from word_fellow.domain.word.WordStatus import WordStatus
from word_fellow.infrastructure import WordFellowDB


def __get_next_unreviewed_word(doc_id: int, offset: int, db: WordFellowDB) -> Optional[Word]:
    word_query_res = db.fetch_one(f"""
    select w.* from words w
    left join global_word_status g on w.text = g.word
    where g.word is null
        and w.document_id = {doc_id}
    limit {offset}, 1
    """)
    if word_query_res is None:
        return None
    return word_fellow.domain.word.WordService.convert_word_data_object_to_word(word_query_res)


def __get_next_global_word(doc_id: int, offset: int, word_status: WordStatus, db: WordFellowDB) -> Optional[Word]:
    word_query_res = db.fetch_one(f"""
    select w.* from words w
    join global_word_status g on w.text = g.word
    where g.status = ?
        and w.document_id = {doc_id}
    limit {offset}, 1
    """, (word_status.name, ))
    if word_query_res is None:
        return None
    return word_fellow.domain.word.WordService.convert_word_data_object_to_word(word_query_res)


def __get_next_ignored_word(doc_id: int, offset: int, db: WordFellowDB) -> Optional[Word]:
    word_query_res = db.fetch_one(f"""
    select w.* from words w
    join global_word_status g on w.text = g.word
    where g.status = 'IGNORED'
        and w.document_id = {doc_id}
    limit {offset}, 1
    """)
    if word_query_res is None:
        return None
    return word_fellow.domain.word.WordService.convert_word_data_object_to_word(word_query_res)


def get_next_word(doc_id: int, offset: int, word_status: WordStatus, db: WordFellowDB) -> Optional[Word]:
    if word_status == WordStatus.UNREVIEWED:
        return __get_next_unreviewed_word(doc_id, offset, db)
    elif word_status in (WordStatus.KNOWN, WordStatus.STUDYING, WordStatus.IGNORED, WordStatus.STUDY_LATER):
        return __get_next_global_word(doc_id, offset, word_status, db)
    else:
        raise ValueError("Unknown word status: " + word_status.name)


def get_word_count(doc_id: int, word_status: WordStatus, db: WordFellowDB) -> int:
    if word_status == WordStatus.UNREVIEWED:
        return db.fetch_one(f"""
        select count(*)
        from words w
          left join global_word_status g on w.text = g.word
        where g.word is null
          and w.document_id = {doc_id}
        """)[0]
    return db.fetch_one(f"""
    select count(*) as cnt
    from words w
      join global_word_status g on w.text = g.word
    where g.status = ?
        and w.document_id = ?
    """, (word_status.name, doc_id))[0]