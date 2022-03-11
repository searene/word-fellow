from sqlite3 import Cursor
from typing import Any, List

from anki.db import DB

class VocabBuilderDB:
    def __init__(self, db_path: str):
        self.db = DB(db_path)

    def execute(self, sql: str) -> Cursor:
        return self.db.execute(sql)

    def first(self, sql: str) -> Any:
        return self.db.first(sql)

    def all(self, sql: str) -> List:
        return self.db.all(sql)
