import os

from vocab_builder.infrastructure import VocabBuilderDB


class ResetService:

    def __init__(self, db: VocabBuilderDB):
        self.__db = db

    def reset(self) -> None:
        self.__db.execute("delete from documents")
        self.__db.execute("delete from words")
        self.__db.execute("delete from global_word_status")
        self.__db.execute("delete from settings")
