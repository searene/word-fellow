from sqlite3 import Cursor
from typing import Any, List, Tuple, Optional
from sqlite3 import dbapi2 as sqlite


# TODO should I call close manually?
# TODO should I call commit manually?
class VocabBuilderDB:
    def __init__(self, db_path: str):
        self.db = sqlite.connect(db_path)

    def execute(self, sql: str, *params: Tuple) -> Cursor:
        return self.db.execute(sql, *params)

    def execute_script(self, script: str) -> Cursor:
        return self.db.executescript(script)

    def insert(self, sql: str, *params: Tuple) -> int:
        """Insert a record, return its id"""
        cursor = self.db.execute(sql, *params)
        return cursor.lastrowid

    def first(self, sql: str) -> Any:
        c = self.db.execute(sql)
        res = c.fetchone()
        return res

    def commit(self) -> None:
        return self.db.commit()

    def fetch_one(self, sql: str, *params: Tuple) -> Optional[Tuple]:
        c = self.execute(sql, *params)
        return c.fetchone()

    def fetch_all(self, sql: str, *params: Tuple) -> List[Tuple]:
        c = self.execute(sql, *params)
        return c.fetchall()
