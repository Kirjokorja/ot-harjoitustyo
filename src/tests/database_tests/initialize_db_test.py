import unittest
import sqlite3
import locale
import re
from database.db import DatabaseInterface
from database.initialize_db import DatabaseInitializer
from tests.test_config import DATABASE_FILE_PATH, DATABASE_SCHEMA_PATH, DATABASE_SEED_PATH

class TestDatabaseInitializer(unittest.TestCase):
    def setUp(self):
        self.test_db = DatabaseInterface(DATABASE_FILE_PATH)
        self.initializer = DatabaseInitializer(self.test_db, DATABASE_SCHEMA_PATH, DATABASE_SEED_PATH)

    def test_initialize_database_creates_tables_from_schema(self):
        self.initializer.initialize_database()
        con = sqlite3.connect(DATABASE_FILE_PATH)
        con.execute("PRAGMA foreign_keys = ON")
        con.row_factory = sqlite3.Row

        sql_table_names = """
                SELECT tbl_name 
                FROM sqlite_master
                WHERE type = ?
            """
        table_names = con.execute(sql_table_names, ['table']).fetchall()

        with open(DATABASE_SCHEMA_PATH, encoding=locale.getencoding()) as file:
            sql_schema = file.read()
        
        tables = list()

        regex = re.compile('(?<= TABLE )[a-zA-Z]+')

        for table in regex.finditer(sql_schema):
            tables.append(sql_schema[table.start():table.end()])
        i = 0
        for row in table_names:
            self.assertEqual(row['tbl_name'], tables[i])
            i += 1
