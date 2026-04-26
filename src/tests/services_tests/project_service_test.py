import unittest
import sqlite3
import locale
from tests.test_config import TEST_DATABASE_FILE_PATH, TEST_DATABASE_SCHEMA_PATH, TEST_DATABASE_SEED_PATH
from database.db import DatabaseInterface
from exceptions import (project_exceptions as exceptions)
from repositories.project_repository import ProjectRepository
from entities.project import Project
from services.project_service import ProjectService
from entities.user import User
from entities.type_class import TypeClass


class TestProjectService(unittest.TestCase):
    def setUp(self):
        self.db = DatabaseInterface(TEST_DATABASE_FILE_PATH)
        self.p_repo = ProjectRepository(self.db)
        self.p_service = ProjectService(
            repository=self.p_repo, exceptions=exceptions)

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

        sql_user = """SELECT Users.id,
                            Users.username,
                            Users.password_hash
                        FROM Users
                    """

        self.user_result = con.execute(sql_user).fetchall()

        self.user = User(
            u_id=self.user_result[0]["id"],
            username=self.user_result[0]["username"],
            password=self.user_result[0]["password_hash"]
        )

        sql_class = """SELECT id, title, value FROM Classes
                        WHERE title = ?
                        ORDER BY id
                    """
        self.class_result = con.execute(sql_class, ["Hanke"]).fetchall()

        self.p_type = TypeClass(
            t_id=self.class_result[0]["id"],
            title=self.class_result[0]["title"],
            value=self.class_result[0]["value"]
        )

        self.project = Project({
            "id": None,
            "title": "Maailma_testi",
            "type": self.p_type,
            "description": "kuvaus",
            "owner": self.user
        })

        sql = """INSERT INTO Projects (title, type, description, owner) 
                    VALUES (?, ?, ?, ?)"""

        con = sqlite3.connect(TEST_DATABASE_FILE_PATH)
        con.execute("PRAGMA foreign_keys = ON")
        con.row_factory = sqlite3.Row

        self.result = con.execute(
            sql,
            [self.project.title,
             self.project.p_type.t_id,
             self.project.description,
             self.project.owner.u_id]
        )

        con.commit()
        con.close()

        self.p_type_mod = TypeClass(
            t_id=self.class_result[2]["id"],
            title=self.class_result[2]["title"],
            value=self.class_result[2]["value"]
        )

        self.user_mod = User(
            u_id=self.user_result[2]["id"],
            username=self.user_result[2]["username"],
            password=self.user_result[2]["password_hash"]
        )

    def test_get_project_classes_gets_project_classes_from_database(self):
        con = sqlite3.connect(TEST_DATABASE_FILE_PATH)
        con.execute("PRAGMA foreign_keys = ON")
        con.row_factory = sqlite3.Row

        sql_classes = """
                SELECT value 
                FROM Classes
                WHERE title = ?
            """

        result = con.execute(sql_classes, ['Hanke']).fetchall()
        con.close()

        db_classes = self.p_service.get_project_classes()

        i = 0
        for type_class in db_classes:
            self.assertEqual(type_class.title, "Hanke")
            self.assertEqual(type_class.value, result[i]["value"])
            i += 1

    def test_save_project_modifies_project_in_database(self):

        project_mod = Project({
            "id": self.result.lastrowid,
            "title": "Maailman tallennus",
            "type": self.p_type_mod,
            "description": "Heippa!",
            "owner": self.user_mod
        })

        self.assertEqual(self.p_service.save_project(project_mod), project_mod)

    def test_save_project_raises_project_has_no_title_exception(self):

        project_mod = Project({
            "id": self.result.lastrowid,
            "title": "",
            "type": self.p_type_mod,
            "description": "Heippa!",
            "owner": self.user_mod
        })

        exc = None

        try:
            self.p_service.save_project(project_mod)
        except Exception as e:
            exc = e

        self.assertEqual(type(exc), exceptions.ProjectHasNoTitle)

    def test_save_project_raises_project_has_no_type_exception(self):

        project_mod = Project({
            "id": self.result.lastrowid,
            "title": "Maailma",
            "type": None,
            "description": "Heippa!",
            "owner": self.user_mod
        })

        exc = None

        try:
            self.p_service.save_project(project_mod)
        except Exception as e:
            exc = e

        self.assertEqual(type(exc), exceptions.ProjectHasNoType)

    def test_save_project_raises_project_has_no_owner_exception(self):
        project_mod = Project({
            "id": self.result.lastrowid,
            "title": "Maailma",
            "type": self.p_type_mod,
            "description": "Heippa!",
            "owner": None
        })

        exc = None

        try:
            self.p_service.save_project(project_mod)
        except Exception as e:
            exc = e

        self.assertEqual(type(exc), exceptions.ProjectHasNoOwner)

    def test_create_project_creates_project_into_database(self):

        created_project = self.p_service.create_project(
            "Maailman luonti",
            self.p_type_mod,
            "luonnin kuvaus",
            self.user_mod
        )

        con = sqlite3.connect(TEST_DATABASE_FILE_PATH)
        con.execute("PRAGMA foreign_keys = ON")
        con.row_factory = sqlite3.Row

        sql_found_project = """SELECT Projects.id,
                                    Projects.title,
                                    Projects.type,
                                    Projects.description,
                                    Projects.owner
                            FROM Projects
                            WHERE Projects.id = ?
                        """

        result = con.execute(
            sql_found_project,
            [str(created_project.p_id)]
        ).fetchall()[0]

        con.close()

        self.assertEqual(result["id"], created_project.p_id)
        self.assertEqual(result["title"], created_project.title)
        self.assertEqual(result["type"], created_project.p_type.t_id)
        self.assertEqual(result["description"], created_project.description)
        self.assertEqual(result["owner"], created_project.owner.u_id)

    def test_create_project_raises_project_has_no_title_exception(self):

        exc = None

        try:
            self.p_service.create_project(
                "",
                self.p_type_mod,
                "luonnin kuvaus",
                self.user_mod
            )
        except Exception as e:
            exc = e

        self.assertEqual(type(exc), exceptions.ProjectHasNoTitle)

    def test_save_project_raises_project_has_no_type_exception(self):

        exc = None

        try:
            self.p_service.create_project(
                "Maailman luonti",
                None,
                "luonnin kuvaus",
                self.user_mod
            )
        except Exception as e:
            exc = e

        self.assertEqual(type(exc), exceptions.ProjectHasNoType)

    def test_save_project_raises_project_has_no_owner_exception(self):

        exc = None

        try:
            self.p_service.create_project(
                "Maailman luonti",
                self.p_type_mod,
                "luonnin kuvaus",
                None
            )
        except Exception as e:
            exc = e

        self.assertEqual(type(exc), exceptions.ProjectHasNoOwner)
