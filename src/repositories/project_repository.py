from repositories.repository import RepositoryBase
from database.db import (database as default_db)


class ProjectRepository(RepositoryBase):
    """Luokka vastaa hankkeiden tietokantatoiminnoista.

        Attribuutit:
            _db (DatabaseInterface): tietokannan käyttöliittymäolio
    """

    def __init__(self, db=default_db):
        super().__init__(db)

    def add_project(self, project):
        """Lisää uuden hankkeen tietokantaan.

            Muuttujat:
                project (Project): hankeolio

            Palauttaa:
                project (Project): hankeolio
        """
        sql = """INSERT INTO Projects (title, type, description, owner)
                    VALUES (?, ?, ?, ?)"""

        project.id = self._db.execute(
            sql,
            [project.title, project.p_type.t_id,
                project.description, project.owner.u_id]
        )
        return project


default_project_repository = ProjectRepository()
