import unittest
import sqlite3
import locale
import re
import os
from database.db import DatabaseInterface
from database.initialize_db import DatabaseInitializer
from tests.test_config import TEST_DATABASE_FILE_PATH, TEST_DATABASE_SCHEMA_PATH, TEST_DATABASE_SEED_PATH


class TestDatabaseInitializer(unittest.TestCase):
    def setUp(self):
        if os.path.exists(TEST_DATABASE_FILE_PATH):
            os.remove(TEST_DATABASE_FILE_PATH)
        self.test_db = DatabaseInterface(TEST_DATABASE_FILE_PATH)

        print(TEST_DATABASE_FILE_PATH)
        print(TEST_DATABASE_SCHEMA_PATH)
        print(TEST_DATABASE_SEED_PATH)

    def test_initialize_database_creates_tables_from_schema(self):
        initializer = DatabaseInitializer(
            self.test_db, TEST_DATABASE_SCHEMA_PATH, TEST_DATABASE_SEED_PATH)
        initializer.initialize_database()

        con = sqlite3.connect(TEST_DATABASE_FILE_PATH)
        con.execute("PRAGMA foreign_keys = ON")
        con.row_factory = sqlite3.Row

        sql_table_names = """
                SELECT tbl_name 
                FROM sqlite_master
                WHERE type = ?
            """
        table_names = con.execute(sql_table_names, ['table']).fetchall()
        con.close()

        with open(TEST_DATABASE_SCHEMA_PATH, encoding=locale.getencoding()) as file:
            sql_schema = file.read()

        tables = list()

        regex = re.compile('(?<= TABLE )[a-zA-Z]+')

        for table in regex.finditer(sql_schema):
            tables.append(sql_schema[table.start():table.end()])
        i = 0
        for row in table_names:
            self.assertEqual(row['tbl_name'], tables[i])
            i += 1

    def test_initialize_databse_creates_content_from_seed(self):
        con = sqlite3.connect(TEST_DATABASE_FILE_PATH)
        con.execute("PRAGMA foreign_keys = ON")
        con.row_factory = sqlite3.Row

        con.executescript("""CREATE TABLE Users (
                            id INTEGER PRIMARY KEY,
                            username TEXT UNIQUE,
                            password_hash TEXT
                        );

                        CREATE TABLE Projects (
                            id INTEGER PRIMARY KEY,
                            title TEXT, 
                            type INTEGER REFERENCES Classes ON DELETE SET NULL,
                            description TEXT,
                            owner INTEGER REFERENCES Users ON DELETE SET NULL
                        );

                        CREATE TABLE Classes (
                            id INTEGER PRIMARY KEY,
                            title TEXT,
                            value TEXT
                        );"""
                          )
        con.commit()
        con.close()

        initializer = DatabaseInitializer(
            self.test_db, TEST_DATABASE_SCHEMA_PATH, TEST_DATABASE_SEED_PATH)
        initializer.initialize_database()

        con = sqlite3.connect(TEST_DATABASE_FILE_PATH)
        con.execute("PRAGMA foreign_keys = ON")
        con.row_factory = sqlite3.Row

        sql_content = "SELECT username FROM Users ORDER BY username"
        db_users = con.execute(sql_content).fetchall()
        con.close()

        with open(TEST_DATABASE_SEED_PATH, encoding=locale.getencoding()) as file:
            sql_seed = file.read()

        print(sql_seed)

        users = list()

        regex = re.compile('(?<= password_hash\\) VALUES \\(\')[a-zA-Z0-9]+')

        print("regex:")
        for user in regex.finditer(sql_seed):
            users.append(sql_seed[user.start():user.end()])
        users.sort()
        for x in users:
            print(x)
        i = 0
        print("Kysely:")
        for row in db_users:
            print(row['username'])
            self.assertEqual(row['username'], users[i])
            i += 1

    def test_initialize_database_creates_no_content_if_no_seed(self):
        initializer = DatabaseInitializer(
            self.test_db, TEST_DATABASE_SCHEMA_PATH, None)
        initializer.initialize_database()

        con = sqlite3.connect(TEST_DATABASE_FILE_PATH)
        con.execute("PRAGMA foreign_keys = ON")
        con.row_factory = sqlite3.Row

        sql_content = "SELECT username FROM Users"
        db_users = con.execute(sql_content).fetchall()

        con.close()

        self.assertEqual(len(db_users), 0)
