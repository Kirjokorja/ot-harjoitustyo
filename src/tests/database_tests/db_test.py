import unittest
import sqlite3
from database.db import DatabaseInterface
from tests.test_config import DATABASE_FILE_PATH, DATABASE_SCHEMA, DATABASE_CONTENT

class TestDatabaseInterface(unittest.TestCase):
    def setUp(self):
        self.test_db = DatabaseInterface(DATABASE_FILE_PATH)

        con = sqlite3.connect(DATABASE_FILE_PATH)
        con.execute("PRAGMA foreign_keys = ON")
        con.row_factory = sqlite3.Row

        sql_table_names = """
                SELECT tbl_name 
                FROM sqlite_master
                WHERE type = ?
            """

        result =  con.execute(sql_table_names, ['table']).fetchall()

        if result:
            sql_drop = "DROP TABLE IF EXISTS "
            for row in result:
                sql_drop += row["tbl_name"] + ";"
            con.executescript(sql_drop)
        
        con.executescript(DATABASE_SCHEMA)
        con.executescript(DATABASE_CONTENT)
        
    def test_query_palauttaa_listan(self):
        sql = "SELECT id, username FROM Users WHERE username = ?"
        result = self.test_db.query(sql, ["Aava"])

        self.assertEqual(type(result), type(list()))
