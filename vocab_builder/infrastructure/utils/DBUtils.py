def escape_for_sql_statement(s: str):
    return s.replace("'", "''")