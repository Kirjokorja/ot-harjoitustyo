import unittest
import sqlite3
import locale
from tests.test_config import TEST_DATABASE_FILE_PATH, TEST_DATABASE_SCHEMA_PATH, TEST_DATABASE_SEED_PATH
from database.db import DatabaseInterface
from repositories.project_repository import ProjectRepository
from entities.project import Project
from entities.user import User
from entities.type_class import TypeClass


class TestProjectRepository(unittest.TestCase):
    def setUp(self):
        self.db = DatabaseInterface(TEST_DATABASE_FILE_PATH)
        self.projectRepo = ProjectRepository(self.db)

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

    def test_add_project_adds_project_to_database(self):
        con = sqlite3.connect(TEST_DATABASE_FILE_PATH)
        con.execute("PRAGMA foreign_keys = ON")
        con.row_factory = sqlite3.Row

        sql_user = """SELECT Users.id,
                            Users.username,
                            Users.password_hash
                        FROM Users
                    """

        user_result = con.execute(sql_user).fetchall()[0]
        user = User(u_id=user_result["id"], username=user_result["username"],
                    password=user_result["password_hash"])

        sql_class = """SELECT id, title, value FROM Classes
                        WHERE title = ?
                        ORDER BY id
                    """
        class_result = con.execute(sql_class, ["Hanke"]).fetchall()[0]
        p_type = TypeClass(
            t_id=class_result["id"], title=class_result["title"], value=class_result["value"])

        project = Project({
            "id": None,
            "title": "Maailma_testi",
            "type": p_type,
            "description": "kuvaus",
            "owner": user
        })

        added_project = self.projectRepo.add_project(project=project)

        sql_found_project = """SELECT Projects.id,
                                    Projects.title,
                                    Projects.type,
                                    Projects.description,
                                    Projects.owner
                            FROM Projects
                            WHERE Projects.id = ?
                        """

        result = con.execute(sql_found_project, [
                             str(added_project.p_id)]).fetchall()[0]

        con.close()

        self.assertEqual(result["id"], added_project.p_id)
        self.assertEqual(result["title"], project.title)
        self.assertEqual(result["type"], project.p_type.t_id)
        self.assertEqual(result["description"], project.description)
        self.assertEqual(result["owner"], project.owner.u_id)
