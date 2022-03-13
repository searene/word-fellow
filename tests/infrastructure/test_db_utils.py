import unittest

from vocab_builder.infrastructure.utils import DBUtils


class DBUtilsTestCase(unittest.TestCase):

    def test_escape_for_sql_statement_without_single_quote(self):
        escaped = DBUtils.escape_for_sql_statement("abc")
        self.assertEqual(escaped, "abc")

    def test_escape_for_sql_statement_with_one_single_quote(self):
        escaped = DBUtils.escape_for_sql_statement("a'bc")
        self.assertEqual(escaped, "a''bc")

    def test_escape_for_sql_statement_with_multiple_single_quotes(self):
        escaped = DBUtils.escape_for_sql_statement("a'b'c")
        self.assertEqual(escaped, "a''b''c")
