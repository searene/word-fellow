import os
import shutil

from ...infrastructure import WordFellowDB


class ExportService:
    def __init__(self, db: WordFellowDB):
        self.__db = db

    def export(self, export_path: str):
        shutil.copyfile(self.__db.db_path, export_path)

    def is_export_file_valid(self, export_file_path: str) -> (bool, str):
        if not export_file_path:
            return False, "Export file cannot be empty!"
        if not export_file_path.endswith(".db"):
            return False, "Export file must end with .db!"
        return True, ""
