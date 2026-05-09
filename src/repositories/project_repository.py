from repositories.repository import RepositoryBase
from database.db import (database as default_db)
from entities.project import Project
from entities.user import User
from entities.type_class import TypeClass


class ProjectRepository(RepositoryBase):
    """Luokka vastaa hankkeiden tietokantatoiminnoista.

        Attributes:
            _db (DatabaseInterface): tietokannan käyttöliittymäolio
    """

    def __init__(self, db=default_db):
        super().__init__(db)

    def _get_project_from_row(self, row):
        class_type = TypeClass(
            t_id=row["class_id"], title=row["class_title"], value=row["class_value"])
        owner = User(u_id=row["owner_id"], username=row["owner_name"])
        params = {
            "id": row["id"],
            "title": row["title"],
            "type": class_type,
            "description": row["description"],
            "owner": owner
        }
        return Project(params=params)

    def _get_projects_from_rows(self, rows):
        return list(map(self._get_project_from_row, rows))

    def add_project(self, project):
        """Lisää uuden hankkeen tietokantaan.

            Args:
                project (Project): hankeolio

            Returns:
                project (Project): hankeolio
        """
        sql = """INSERT INTO Projects (title, type, description, owner)
                    VALUES (?, ?, ?, ?)"""

        project.p_id = self._db.execute(
            sql,
            [project.title, project.p_type.t_id,
                project.description, project.owner.u_id]
        )
        return project

    def edit_project(self, project):
        """Muokkaa hanketta tietokannassa.

            Args:
                project (Project): hankeolio

            Returns:
                project (Project): hankeolio
        """
        sql = """UPDATE Projects
                    SET title = ?,
                        type = ?,
                        description = ?
                    WHERE id = ?
            """
        self._db.execute(
            sql,
            [project.title, project.p_type.t_id,
                project.description, project.p_id]
        )
        return project

    def delete_project(self, project_id):
        """Poistaa hankkeen tietokannasta.

            Args:
                project_id (int): poistettavan hankkeen tunnusluku
        """
        sql = "DELETE FROM Projects WHERE id = ?"
        self._db.execute(sql, [project_id])

    def count_results(self, query):
        """Pyytää tietokannasta hankehaun tulosten lukumäärän.

            Args:
                query (String): hakusana

            Returns:
                int: hakutulosten lukumäärä
        """
        sql = """SELECT
                    (SELECT COUNT(*) 
                        FROM Projects
                        WHERE (Projects.title LIKE ? 
                        OR Projects.description LIKE ?)
                    )
             """

        like = "%" + query + "%"
        return self._db.query(sql, [like, like])[0][0]

    def find_projects_by_page(self, query, page, page_size):
        """Kyselee tietokannasta hankkeita hakusanalla niiden otsikoista ja kuvauksista.

            Args:
                query (String): hakusana
                page (String): näytettävän sivun numero koko hausta
                page_size (String): näytettävän sivun koko

            Returns:
                List: lista löytyneistä hankeolioista
        """
        sql = """SELECT Projects.id id,
                        Projects.title title,
                        Classes.id class_id,
                        Classes.title class_title,
                        Classes.value class_value,
                        Projects.description,
                        Users.id owner_id,
                        Users.username owner_name
                FROM Projects, Classes, Users
                WHERE (Projects.title LIKE ? OR Projects.description LIKE ?)
                AND Users.id = Projects.owner
                AND Projects.type = Classes.id
                ORDER BY title ASC
                LIMIT ? OFFSET ?
             """
        like = "%" + query + "%"
        limit = page_size
        offset = page_size * (page - 1)
        result = self._db.query(sql, [like, like, limit, offset])
        return self._get_projects_from_rows(result)

    def get_project(self, project_id):
        """Kyselee hanketta tunnusluvulla tietokannalta.

            Args:
                project_id (int): hankkeen tunnusluku
        """
        sql = """SELECT Projects.id,
                        Projects.title,
                        Classes.id class_id,
                        Classes.title class_title,
                        Classes.value class_value,
                        Projects.description,
                        Users.id owner_id,
                        Users.username owner_name
                FROM Projects, Users, Classes
                WHERE Users.id = Projects.owner 
                AND Projects.id = ?
                AND Classes.id = Projects.type
            """
        result = self._db.query(sql, [project_id])
        return self._get_project_from_row(result[0])

    def get_projects_owner(self, project_id):
        """Kyselee tietokannalta hankkeen haltijaa.

            Args:
                project_id (int): hankkeen tunnusluku

            Returns:
                User: hankkeen haltijan käyttäjäolio
        """
        sql = """SELECT Users.id,
                        Users.username
                FROM Users, Projects
                WHERE Users.id = Projects.owner
                AND Projects.id = ?
              """
        result = self._db.query(sql, [project_id])[0]
        return User(u_id=result["id"], username=result["username"])


default_project_repository = ProjectRepository()
