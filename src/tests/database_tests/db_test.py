import unittest
import sqlite3
from database.db import DatabaseInterface
from tests.test_config import TEST_DATABASE_FILE_PATH


class TestDatabaseInterface(unittest.TestCase):
    def setUp(self):

        con = sqlite3.connect(TEST_DATABASE_FILE_PATH)
        con.execute("PRAGMA foreign_keys = ON")
        con.row_factory = sqlite3.Row

        sql_table_names = """
                SELECT tbl_name 
                FROM sqlite_master
                WHERE type = ?
            """

        result = con.execute(sql_table_names, ['table']).fetchall()

        statement = "DROP TABLE IF EXISTS "

        if result:
            sql_drop = ""
            for table in result:
                sql_drop += statement + table['tbl_name'] + ";"
            con.executescript(sql_drop)

        sql_schema = """CREATE TABLE Users (
                        id INTEGER PRIMARY KEY,
                        username TEXT UNIQUE,
                        password_hash TEXT
                    );"""
        con.executescript(sql_schema)
        con.commit()
        con.close()

        self.test_db = DatabaseInterface(TEST_DATABASE_FILE_PATH)

    def test_query_returns_list(self):
        con = sqlite3.connect(TEST_DATABASE_FILE_PATH)
        con.execute("PRAGMA foreign_keys = ON")
        con.row_factory = sqlite3.Row

        sql_seed = """INSERT INTO Users (username, password_hash) 
                            VALUES ('Pekka', 'testi1');
                    """
        con.executescript(sql_seed)
        con.commit()
        con.close()

        sql = "SELECT id, username FROM Users WHERE username = ?"
        result = self.test_db.query(sql, ["Pekka"])

        self.assertEqual(type(result), type(list()))

    def test_query_list_contains_sqlite_rows(self):
        con = sqlite3.connect(TEST_DATABASE_FILE_PATH)
        con.execute("PRAGMA foreign_keys = ON")
        con.row_factory = sqlite3.Row

        sql_seed = """INSERT INTO Users (username, password_hash) 
                            VALUES ('Aava', 'testi2');
                    """
        con.executescript(sql_seed)
        con.commit()
        con.close()

        sql = "SELECT id, username FROM Users WHERE username = ?"
        result = self.test_db.query(sql, ["Aava"])

        self.assertEqual(type(result[0]), sqlite3.Row)

    def test_execute_returns_last_inserted_row_id(self):
        sql = """INSERT INTO Users (username, password_hash) 
                            VALUES (?, ?);
                """

        row_id = self.test_db.execute(sql, ['Louhi', 'testi3'])

        self.assertEqual(row_id, 1)
