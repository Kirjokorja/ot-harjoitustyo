from services.service import ServiceBase
from exceptions import (project_exceptions as default_exceptions)
from repositories.project_repository import default_project_repository
from entities.project import Project


class ProjectService(ServiceBase):
    """Luokka vastaa hankkeisiin liittyvistä toiminnoista sovelluksessa.

        Attributes:
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

            Args:
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

    def get_project_classes(self):
        """Antaa hankkeiden luokat.

            Returns:
                list<TypeClass>: lista luokkaolioita
        """
        return self._repository.get_classes("Hanke")

    def save_project(self, project):
        """Muokkaa hanketta.

            Args:
                project (Project): hankeolio

            Raises:
                ProjectHasNoTitle: virhe, joka syntyy hankkeen nimikkeen puuttuessa
                ProjectHasNoType: virhe, joka syntyy hankkeen luokan puuttuessa
                ProjectHasNoOwner: virhe, joka syntyy hankkeen haltijan puuttuessa

            Returns:
                project (Project): hankeolio
        """
        self._project_acceptable(project.title, project.p_type, project.owner)
        project = self._repository.edit_project(project)
        return project

    def create_project(self, title, p_type, description, owner):
        """Luo uuden hankkeen.

            Args:
                title (str): hankkeen nimi
                p_type (TypeClass): hankkeen luokka
                description (str): hankkeen kuvaus
                owner (User): hankkeen haltija

            Raises:
                ProjectHasNoTitle: virhe, joka syntyy hankkeen nimikkeen puuttuessa
                ProjectHasNoType: virhe, joka syntyy hankkeen luokan puuttuessa
                ProjectHasNoOwner: virhe, joka syntyy hankkeen haltijan puuttuessa

            Returns:
                project (Project): hankeolio
        """

        project = Project({
            "id": None,
            "title": title,
            "type": p_type,
            "description": description,
            "owner": owner
        })
        self._project_acceptable(project.title, project.p_type, project.owner)
        project = self._repository.add_project(project)
        return project


default_project_service = ProjectService()
