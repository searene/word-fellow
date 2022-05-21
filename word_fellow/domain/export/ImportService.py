import os
import shutil

from word_fellow.domain.utils import FileUtils
from word_fellow.infrastructure import WordFellowDB


class ImportService:
    def __init__(self, db: WordFellowDB):
        self.__db = db

    def do_import(self, exported_file_path: str) -> None:
        if not os.path.exists(exported_file_path):
            raise FileExistsError(f"File does not exist: {exported_file_path}")
        os.remove(self.__db.db_path)
        shutil.move(exported_file_path, self.__db.db_path)
