import unittest
import sqlite3
import locale
import re
from tests.test_config import TEST_DATABASE_FILE_PATH, TEST_DATABASE_SCHEMA_PATH, TEST_DATABASE_SEED_PATH
from database.db import DatabaseInterface
from repositories.repository import RepositoryBase


class TestRepository(unittest.TestCase):
    def setUp(self):
        self.db = DatabaseInterface(TEST_DATABASE_FILE_PATH)
        self.repo = RepositoryBase(self.db)

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
            con.commit()

        with open(TEST_DATABASE_SCHEMA_PATH, encoding=locale.getencoding()) as file:
            sql_schema = file.read()
        con.executescript(sql_schema)
        con.commit()

        with open(TEST_DATABASE_SEED_PATH, encoding=locale.getencoding()) as file:
            sql_seed = file.read()
        print(sql_seed)
        con.executescript(sql_seed)
        con.commit()
        con.close()

    def test_get_classes_returns_classes_by_title_from_database(self):
        con = sqlite3.connect(TEST_DATABASE_FILE_PATH)
        con.execute("PRAGMA foreign_keys = ON")
        con.row_factory = sqlite3.Row

        sql_classes = """
                SELECT value 
                FROM Classes
                WHERE title = ?
            """

        result = con.execute(sql_classes, ['Luokka']).fetchall()

        con.close()

        db_classes = self.repo.get_classes("Luokka")

        i = 0
        for type_class in db_classes:
            self.assertEqual(type_class.title, "Luokka")
            self.assertEqual(type_class.value, result[i]["value"])
            i += 1

