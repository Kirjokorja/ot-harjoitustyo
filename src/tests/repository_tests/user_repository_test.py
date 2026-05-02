import unittest
import sqlite3
import locale
from tests.test_config import (TEST_DATABASE_FILE_PATH,
                               TEST_DATABASE_SCHEMA_PATH,
                               TEST_DATABASE_SEED_PATH)
from database.db import DatabaseInterface
from repositories.user_repository import UserRepository
from entities.user import User


class TestUserRepository(unittest.TestCase):
    def setUp(self):
        self.db = DatabaseInterface(TEST_DATABASE_FILE_PATH)
        self.user_repo = UserRepository(self.db)

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

    def test_find_user_by_name_returns_correct_user(self):
        user = self.user_repo.find_user_by_name("Aava")

        self.assertEqual(user.u_id, 4)

    def test_find_user_by_name_returns_none_when_username_is_not_in_database(self):
        user = self.user_repo.find_user_by_name("ei-tietokannassa")

        self.assertEqual(user, None)

    def test_add_user_adds_user_to_database(self):
        user = User(username="Pohjolan isäntä", password="moro!")

        added_user = self.user_repo.add_user(user=user)

        con = sqlite3.connect(TEST_DATABASE_FILE_PATH)
        con.execute("PRAGMA foreign_keys = ON")
        con.row_factory = sqlite3.Row

        sql_found_user = """SELECT Users.id,
                                    Users.username,
                                    Users.password_hash
                            FROM Users
                            WHERE Users.id = ?
                        """

        result = con.execute(
            sql_found_user, [str(added_user.u_id)]).fetchall()[0]

        con.close()

        self.assertEqual(result["id"], added_user.u_id)
        self.assertEqual(result["username"], user.username)
        self.assertEqual(result["password_hash"], user.password)
