import os

from vocab_builder.infrastructure import VocabBuilderDB


class ResetService:

    def __init__(self, db: VocabBuilderDB):
        self.__db = db

    def reset(self) -> None:
        os.remove(self.__db.db_path)
