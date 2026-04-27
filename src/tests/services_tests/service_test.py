import unittest
from tests.test_config import TEST_DATABASE_FILE_PATH
from database.db import DatabaseInterface
from exceptions import (project_exceptions as exceptions)
from repositories.repository import RepositoryBase
from services.service import ServiceBase


class TestProjectService(unittest.TestCase):
    def setUp(self):
        self.db = DatabaseInterface(TEST_DATABASE_FILE_PATH)
        self.repo = RepositoryBase(self.db)
        self.service = ServiceBase(
            repository=self.repo, exceptions=exceptions)

    def test_get_exceptions_returns_exceptions(self):
        self.assertEqual(self.service.get_exceptions(), exceptions)
