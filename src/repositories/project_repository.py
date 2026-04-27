from repositories.repository import RepositoryBase
from database.db import (database as default_db)


class ProjectRepository(RepositoryBase):
    """Luokka vastaa hankkeiden tietokantatoiminnoista.

        Attributes:
            _db (DatabaseInterface): tietokannan käyttöliittymäolio
    """

    def __init__(self, db=default_db):
        super().__init__(db)

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
        sql = """UPDATE Projects SET title = ?,
                            type = ?,
                            description = ?
                            WHERE id = ?"""

        project.p_id = self._db.execute(
            sql,
            [project.title, project.p_type.t_id,
                project.description, project.p_id]
        )
        return project

    def delete_project(self, project):
        """Poistaa hankkeen tietokannasta.

            Args:
                project (Project): hankeolio
        """
        sql = "DELETE FROM Projects WHERE id = ?"
        self._db.execute(sql, [project.p_id])


default_project_repository = ProjectRepository()
