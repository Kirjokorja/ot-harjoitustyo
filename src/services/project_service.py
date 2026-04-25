from services.service import ServiceBase
from exceptions import (project_exceptions as default_exceptions)
from repositories.project_repository import default_project_repository
from entities.project import Project


class ProjectService(ServiceBase):
    """Luokka vastaa hankkeisiin liittyvistä toiminnoista sovelluksessa.

        Attribuutit:
            _repository (ProjectRepository): 
                tietokantatoiminnoista vastaava olio
            _exceptions: virheluokat
    """

    def __init__(
        self,
        repository=default_project_repository,
        exceptions=default_exceptions,
    ):
        """Alusta hankepalvelut.

            Muuttujat:
                repository (ProjectRepository):
                    käyttäjien tietokantatoiminnoista vastaava olio
                exceptions: käyttäjävirheet
        """
        super().__init__(repository=repository, exceptions=exceptions)

    def _project_acceptable(self, title, p_type, owner):
        if len(title) < 1:
            raise self._exceptions.ProjectHasNoTitle(
                "Hankkeelta puuttuu nimi.")
        if not p_type:
            raise self._exceptions.ProjectHasNoType(
                "Hankkeelta puuttuu luokka.")
        if not owner:
            raise self._exceptions.ProjectHasNoOwner(
                "Hankkeelta puuttu haltija.")
        return True

    def get_project_classes(self, title):
        """Antaa hankkeiden luokat.

            Muuttujat:
                title (str):  

            Palauttaa:
                list<TypeClass>: lista luokkaolioita
        """
        return self._repository.get_classes(title)

    def save_project(self, project):
        """Muokkaa hanketta.

            Muuttujat:
                project (Project): hankeolio

            Palauttaa:
                project (Project): hankeolio
        """
        if self._project_acceptable(project.title, project.p_type, project.owner):
            project = self._repository.edit_project(project)
        return project

    def create_project(self, title, p_type, description, owner):
        """Luo uuden hankkeen.

            Muuttujat:
                title (str): hankkeen nimi
                p_type (TypeClass): hankkeen luokka
                description (str): hankkeen kuvaus
                owner (User): hankkeen haltija

            Palauttaa:
                project (Project): hankeolio
        """

        project = Project({
            "id": None,
            "title": title,
            "type": p_type,
            "description": description,
            "owner": owner
        })
        if self._project_acceptable(title, p_type, owner):
            project = self._repository.add_project(project)
        return project


default_project_service = ProjectService()
