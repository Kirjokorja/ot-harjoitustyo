import unittest
import sqlite3
import locale
import os
from tests.test_config import (TEST_DATABASE_FILE_PATH,
                               TEST_DATABASE_SCHEMA_PATH,
                               TEST_DATABASE_SEED_PATH)
from database.db import DatabaseInterface
from repositories.project_repository import ProjectRepository
from entities.project import Project
from entities.user import User
from entities.type_class import TypeClass


class TestProjectRepository(unittest.TestCase):
    def setUp(self):
        self.db = DatabaseInterface(TEST_DATABASE_FILE_PATH)
        self.project_repo = ProjectRepository(self.db)

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
        con.close()

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

    def tearDown(self):
        os.remove(TEST_DATABASE_FILE_PATH)

    def test_add_project_adds_project_to_database(self):
        added_project = self.project_repo.add_project(self.project)

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
            [str(added_project.p_id)]
        ).fetchall()[0]

        con.close()

        self.assertEqual(result["id"], added_project.p_id)
        self.assertEqual(result["title"], self.project.title)
        self.assertEqual(result["type"], self.project.p_type.t_id)
        self.assertEqual(result["description"], self.project.description)
        self.assertEqual(result["owner"], self.project.owner.u_id)

    def test_edit_project_modifies_project_in_database(self):
        p_type = TypeClass(
            t_id=self.class_result[1]["id"],
            title=self.class_result[1]["title"],
            value=self.class_result[1]["value"]
        )

        user = User(
            u_id=self.user_result[1]["id"],
            username=self.user_result[1]["username"],
            password=self.user_result[1]["password_hash"]
        )

        sql = """INSERT INTO Projects (title, type, description, owner) 
                    VALUES (?, ?, ?, ?)"""

        con = sqlite3.connect(TEST_DATABASE_FILE_PATH)
        con.execute("PRAGMA foreign_keys = ON")
        con.row_factory = sqlite3.Row

        result = con.execute(
            sql,
            [self.project.title,
             self.project.p_type.t_id,
             self.project.description,
             self.project.owner.u_id]
        )

        con.commit()
        con.close()

        project_mod = Project({
            "id": result.lastrowid,
            "title": "Maailma_muokkaus",
            "type": p_type,
            "description": "muokattu kuvaus",
            "owner": user
        })

        self.assertEqual(self.project_repo.edit_project(
            project_mod), project_mod)

    def test_delete_project_deletes_project_from_database(self):
        sql = """INSERT INTO Projects (title, type, description, owner) 
                    VALUES (?, ?, ?, ?)"""

        con = sqlite3.connect(TEST_DATABASE_FILE_PATH)
        con.execute("PRAGMA foreign_keys = ON")
        con.row_factory = sqlite3.Row

        result_id = con.execute(
            sql,
            [self.project.title,
             self.project.p_type.t_id,
             self.project.description,
             self.project.owner.u_id]
        ).lastrowid

        con.commit()

        self.project_repo.delete_project(result_id)

        sql_query = """SELECT id, title 
                        FROM Projects
                        WHERE id = ?"""
        query_result = con.execute(sql_query, [result_id]).fetchall()
        con.close()

        self.assertEqual(len(query_result), 0)
