import unittest
import sqlite3
import locale
from bcrypt import gensalt, hashpw, checkpw
from tests.test_config import TEST_DATABASE_FILE_PATH, TEST_DATABASE_SCHEMA_PATH, TEST_DATABASE_SEED_PATH
from database.db import DatabaseInterface
from exceptions import (user_exceptions as exceptions)
from repositories.user_repository import UserRepository
from services.user_service import UserService
from services.password_service import PasswordService


class TestUserService(unittest.TestCase):
    def setUp(self):
        self.db = DatabaseInterface(TEST_DATABASE_FILE_PATH)
        self.u_repo = UserRepository(self.db)
        self.pw_service = PasswordService(6)
        self.u_service = UserService(
            repository=self.u_repo,
            exceptions=exceptions,
            password_service=self.pw_service
        )

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
        con.executescript(sql_seed)

        con.commit()
        con.close()

    def test_create_user_creates_user_into_database(self):

        created_user = self.u_service.create_user(
            "Sampo",
            "Taivaanlaki",
            "Taivaanlaki"
        )

        con = sqlite3.connect(TEST_DATABASE_FILE_PATH)
        con.execute("PRAGMA foreign_keys = ON")
        con.row_factory = sqlite3.Row

        sql_found_project = """SELECT Users.id,
                                    Users.username,
                                    Users.password_hash
                            FROM Users
                            WHERE Users.id = ?
                        """

        result = con.execute(
            sql_found_project,
            [str(created_user.u_id)]
        ).fetchall()[0]

        con.close()

        self.assertEqual(result["id"], created_user.u_id)
        self.assertEqual(result["username"], created_user.username)
        self.assertEqual(result["password_hash"], created_user.password)

    def test_create_user_raises_user_already_exists_exception(self):
        self.u_service.create_user(
            "Sampo",
            "Taivaanlaki",
            "Taivaanlaki"
        )

        exc = None

        try:
            self.u_service.create_user(
                "Sampo",
                "Taivaanlaki",
                "Taivaanlaki"
            )
        except Exception as e:
            exc = e

        self.assertEqual(
            type(exc),
            self.u_service.get_exceptions().UserAlreadyExists
        )

    def test_create_user_raises_pssword_too_short_exception(self):

        exc = None

        try:
            self.u_service.create_user(
                "Sampo",
                "Moi",
                "Moi"
            )
        except Exception as e:
            exc = e

        self.assertEqual(
            type(exc),
            self.u_service.get_exceptions().PasswordTooShort
        )

    def test_create_user_raises_psswords_do_not_macth_exception(self):

        exc = None

        try:
            self.u_service.create_user(
                "Sampo",
                "Taivaanlaki",
                "Moi"
            )
        except Exception as e:
            exc = e

        self.assertEqual(
            type(exc),
            self.u_service.get_exceptions().PasswordsDoNotMatch
        )

    def test_create_user_raises_username_too_short_exception(self):

        exc = None

        try:
            self.u_service.create_user(
                "",
                "Taivaanlaki",
                "Taivaanlaki"
            )
        except Exception as e:
            exc = e

        self.assertEqual(
            type(exc),
            self.u_service.get_exceptions().UsernameTooShort
        )

    def test_login_returns_user_as_object_on_succsessful_login(self):
        password = "Taivaanlaki"
        salt = gensalt()
        password_bytes = password.encode('utf-8')
        pw_hash = hashpw(password_bytes, salt).decode('utf-8')

        con = sqlite3.connect(TEST_DATABASE_FILE_PATH)
        con.execute("PRAGMA foreign_keys = ON")
        con.row_factory = sqlite3.Row

        sql_set = """INSERT INTO Users (username, password_hash) 
                        VALUES (?, ?)"""
        con.execute(sql_set, ["Sampo", pw_hash])
        con.commit()

        sql_get = "SELECT id, username, password_hash FROM Users WHERE username = ?"
        result_get = con.execute(sql_get, ["Sampo"]).fetchall()[0]
        con.close()

        logged_in_user = self.u_service.login("Sampo", password)

        self.assertEqual(logged_in_user.u_id, result_get["id"])
        self.assertEqual(logged_in_user.username, "Sampo")
        self.assertEqual(logged_in_user.password, result_get["password_hash"])
