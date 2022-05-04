from sqlite3 import connect
from typing import Any, List, Tuple, Optional
from contextlib import closing


class VocabBuilderDB:
    def __init__(self, db_path: str):
        self.__conn = connect(db_path)
        self.db_path = db_path

    def execute(self, sql: str, *params: Tuple) -> None:
        with self.__conn:  # auto-commits
            with closing(self.__conn.cursor()) as cursor:  # auto-closes
                cursor.execute(sql, *params)

    def execute_script(self, script: str) -> None:
        with self.__conn:  # auto-commits
            with closing(self.__conn.cursor()) as cursor:  # auto-closes
                cursor.executescript(script)

    def insert(self, sql: str, *params: Tuple) -> int:
        """Insert a record, return its id"""
        with self.__conn:  # auto-commits
            with closing(self.__conn.cursor()) as cursor:  # auto-closes
                return cursor.execute(sql, *params).lastrowid

    def first(self, sql: str) -> Any:
        with self.__conn:  # auto-commits
            with closing(self.__conn.cursor()) as cursor:  # auto-closes
                return cursor.execute(sql).fetchone()

    def fetch_one(self, sql: str, *params: Tuple) -> Optional[Tuple]:
        with self.__conn:  # auto-commits
            with closing(self.__conn.cursor()) as cursor:  # auto-closes
                return cursor.execute(sql, *params).fetchone()

    def fetch_all(self, sql: str, *params: Tuple) -> List[Tuple]:
        with self.__conn:  # auto-commits
            with closing(self.__conn.cursor()) as cursor:  # auto-closes
                return cursor.execute(sql, *params).fetchall()
