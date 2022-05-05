import unittest
from typing import Tuple

from base.BaseTestCase import BaseTestCase


class VocabBuilderDBTestCase(BaseTestCase):

    def test_execute_script_without_params(self):
        self.db.execute_script("""
            BEGIN TRANSACTION;
            CREATE TABLE IF NOT EXISTS test_table (
                id INTEGER PRIMARY KEY,
                name TEXT
            );
            INSERT INTO test_table (name) VALUES ('name1');
            INSERT INTO test_table (name) VALUES ('name2');
            COMMIT;
        """)

        records = self.db.fetch_all("""
        SELECT * FROM test_table
        """)
        self.assertEqual(len(records), 2)
        self.assertTrue(self.__contains_record_with_name(records, "name1"))
        self.assertTrue(self.__contains_record_with_name(records, "name2"))

    @staticmethod
    def __contains_record_with_name(records: Tuple, name: str):
        # The first element of each tuple is the name
        return len([record for record in records if record[1] == name]) >= 1
