import unittest
import sqlite3
import locale
from database.db import DatabaseInterface
from tests.test_config import DATABASE_FILE_PATH, DATABASE_SCHEMA_PATH, DATABASE_SEED_PATH


class TestDatabaseInterface(unittest.TestCase):
    def setUp(self):

        con = sqlite3.connect(DATABASE_FILE_PATH)
        con.execute("PRAGMA foreign_keys = ON")
        con.row_factory = sqlite3.Row

        sql_table_names = """
                SELECT tbl_name 
                FROM sqlite_master
                WHERE type = ?
            """

        result = con.execute(sql_table_names, ['table']).fetchall()

        if result:
            sql_drop = "DROP TABLE IF EXISTS "
            for row in result:
                sql_drop += row["tbl_name"] + ";"
            con.executescript(sql_drop)

        with open(DATABASE_SCHEMA_PATH, encoding=locale.getencoding()) as file:
            sql_schema = file.read()
        con.executescript(sql_schema)

        with open(DATABASE_SEED_PATH, encoding=locale.getencoding()) as file:
            sql_seed = file.read()
        con.executescript(sql_seed)

        self.test_db = DatabaseInterface(DATABASE_FILE_PATH)

    def test_query_returns_list(self):
        sql = "SELECT id, username FROM Users WHERE username = ?"
        result = self.test_db.query(sql, ["Aava"])

        self.assertEqual(type(result), type(list()))
