import os

from word_fellow.infrastructure import WordFellowDB


class ResetService:

    def __init__(self, db: WordFellowDB):
        self.__db = db

    def reset(self) -> None:
        self.__db.destroy()
