import unittest
import sqlite3
import locale
from bcrypt import gensalt, hashpw
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
        self.pw_lenght = 6
        self.pw_service = PasswordService(self.pw_lenght)
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

        self.log_username = "Väinämöinen"
        self.log_pw = "OlisiPitänytNaidaNuorena."
        salt = gensalt()
        self.log_pw_bytes = self.log_pw.encode('utf-8')
        self.log_pw_hash = hashpw(self.log_pw_bytes, salt).decode('utf-8')

        sql_log_set = """INSERT INTO Users (username, password_hash) 
                        VALUES (?, ?)"""
        self.user_log_id = con.execute(
            sql_log_set,
            [self.log_username,
             self.log_pw_hash]
        ).lastrowid
        con.commit()

        sql_get = "SELECT id, username, password_hash FROM Users WHERE id = ?"
        self.result_get_log = con.execute(
            sql_get,
            [self.user_log_id]
        ).fetchall()[0]
        con.close()

        self.create_username = "Sampo"
        self.create_pw = "Taivaanlaki"

    def test_create_user_creates_user_into_database(self):

        created_user = self.u_service.create_user(
            self.create_username,
            self.create_pw,
            self.create_pw
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
            self.create_username,
            self.create_pw,
            self.create_pw
        )

        exc = None

        try:
            self.u_service.create_user(
                self.create_username,
                self.create_pw,
                self.create_pw
            )
        except Exception as e:
            exc = e

        self.assertEqual(type(exc), exceptions.UserAlreadyExists)

    def test_create_user_raises_pssword_too_short_exception(self):

        exc = None

        try:
            self.u_service.create_user(
                "Joukahainen",
                "Moi",
                "Moi"
            )
        except Exception as e:
            exc = e

        self.assertEqual(type(exc), exceptions.PasswordTooShort)

    def test_create_user_raises_psswords_do_not_macth_exception(self):
        exc = None
        try:
            self.u_service.create_user(
                "Joukahainen",
                self.log_pw,
                self.create_pw
            )
        except Exception as e:
            exc = e

        self.assertEqual(type(exc), exceptions.PasswordsDoNotMatch)

    def test_create_user_raises_username_too_short_exception(self):

        exc = None

        try:
            self.u_service.create_user(
                "",
                self.create_pw,
                self.create_pw
            )
        except Exception as e:
            exc = e

        self.assertEqual(type(exc), exceptions.UsernameTooShort)

    def test_login_returns_user_as_object_on_succsessful_login(self):
        logged_in_user = self.u_service.login(self.log_username, self.log_pw)

        self.assertEqual(logged_in_user.u_id, self.result_get_log["id"])
        self.assertEqual(logged_in_user.username,
                         self.result_get_log["username"])
        self.assertEqual(logged_in_user.password,
                         self.result_get_log["password_hash"])

    def test_login_raises_session_already_exists_exception_if_a_user_is_logged_in(self):
        con = sqlite3.connect(TEST_DATABASE_FILE_PATH)
        con.execute("PRAGMA foreign_keys = ON")
        con.row_factory = sqlite3.Row

        salt = gensalt()
        pw_bytes = self.create_pw.encode('utf-8')
        pw_hash = hashpw(pw_bytes, salt).decode('utf-8')

        sql_log_set = """INSERT INTO Users (username, password_hash) 
                        VALUES (?, ?)"""
        con.execute(sql_log_set, [self.create_username, pw_hash]).lastrowid
        con.commit()

        self.u_service.login(self.create_username, self.create_pw)
        exc = None
        try:
            self.u_service.login(self.log_username, self.log_pw)
        except Exception as e:
            exc = e
        self.assertEqual(type(exc), exceptions.ASessionAlreadyExists)

    def test_login_raises_invalid_credentials_exception_if_user_is_not_in_database(self):
        exc = None
        try:
            self.u_service.login(self.create_username, self.create_pw)
        except Exception as e:
            exc = e
        self.assertEqual(type(exc), exceptions.InvalidCredentials)

    def test_login_raises_invalid_credentials_exception_if_password_is_incorrect(self):
        exc = None
        try:
            self.u_service.login(self.log_username, self.create_pw)
        except Exception as e:
            exc = e
        self.assertEqual(type(exc), exceptions.InvalidCredentials)

    def test_get_current_user_gets_logged_in_user(self):
        logged_in_user = self.u_service.login(self.log_username, self.log_pw)

        self.assertEqual(self.u_service.get_current_user(), logged_in_user)

    def test_get_current_user_raises_session_not_found_if_user_is_not_logged_in(self):
        exc = None
        try:
            self.u_service.get_current_user()
        except Exception as e:
            exc = e

        self.assertEqual(type(exc), exceptions.SessionNotFound)

    def test_logout_logs_out_user(self):
        self.u_service.login(self.log_username, self.log_pw)
        self.u_service.logout()

        exc = None
        try:
            self.u_service.get_current_user()
        except Exception as e:
            exc = e

        self.assertEqual(type(exc), exceptions.SessionNotFound)

    def test_get_min_password_lenght_returns_password_lenght(self):
        self.assertEqual(
            self.u_service.get_min_password_lenght(), self.pw_lenght)
