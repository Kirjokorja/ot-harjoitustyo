import unittest
import sqlite3
import locale
from bcrypt import gensalt, hashpw
from tests.test_config import TEST_DATABASE_FILE_PATH, TEST_DATABASE_SCHEMA_PATH, TEST_DATABASE_SEED_PATH
from database.db import DatabaseInterface
from exceptions import (user_exceptions as exceptions)
from repositories.user_repository import UserRepository
from repositories.project_repository import ProjectRepository
from services.project_service import ProjectService
from services.user_service import UserService
from services.password_service import PasswordService
from services.complete_services import Services


class TestUserService(unittest.TestCase):
    def setUp(self):
        self.db = DatabaseInterface(TEST_DATABASE_FILE_PATH)
        self.u_repo = UserRepository(self.db)
        self.p_repo = ProjectRepository(self.db)
        self.pw_lenght = 6
        self.pw_service = PasswordService(self.pw_lenght)
        self.u_service = UserService(
            repository=self.u_repo,
            exceptions=exceptions,
            password_service=self.pw_service
        )
        self.p_service = ProjectService(
            repository=self.p_repo,
            exceptions=exceptions
        )
        self.all_services = Services(
            user_service=self.u_service,
            project_service=self.p_service
        )

    def test_get_user_service_returns_user_service(self):
        self.assertEqual(self.all_services.get_user_service(), self.u_service)

    def test_get_project_service_returns_project_service(self):
        self.assertEqual(
            self.all_services.get_project_service(),
            self.p_service
        )
