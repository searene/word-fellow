import shutil

from word_fellow.infrastructure import WordFellowDB


class ExportService:
    def __init__(self, db: WordFellowDB):
        self.__db = db

    def export(self, export_path: str):
        shutil.copyfile(self.__db.db_path, export_path)

    def get_default_extension(self) -> str:
        return ".db"
