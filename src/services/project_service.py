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

    def save_project(self, user, project):
        """Muokkaa hanketta.

            Args:
                project (Project): hankeolio
                user (User): käyttäjäolio

            Raises:
                UserNotOwnerOfProject: virhe, 
                    joka syntyy, kun hanketta käsittelevä kyttäjä ei ole hankkeen haltia
                ProjectHasNoTitle: virhe, joka syntyy hankkeen nimikkeen puuttuessa
                ProjectHasNoType: virhe, joka syntyy hankkeen luokan puuttuessa
                ProjectHasNoOwner: virhe, joka syntyy hankkeen haltijan puuttuessa

            Returns:
                project (Project): hankeolio
        """
        db_user = self._repository.get_projects_owner(project.p_id)
        if user.u_id is not db_user.u_id:
            raise self._exceptions.UserNotOwnerOfProject(
                "Käyttäjä ei ole hankkeen haltija.")
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

    def remove_project(self, user, project):
        """Poistaa hankeen.

            Args:
                user (User): käyttäjäolio
                project (Project): poistettava hankeolio

            Raises:
                UserNotOwnerOfProject: virhe, joka syntyy, 
                    kun hanketta yrittää poistaa joku muu kuin hankkeen haltija
        """
        db_user = self._repository.get_projects_owner(project.p_id)
        if user.u_id is not db_user.u_id:
            raise self._exceptions.UserNotOwnerOfProject(
                "Käyttäjä ei ole hankkeen haltija.")
        self._repository.delete_project(project.p_id)

    def count_projects(self, query):
        """Antaa hankehaun tulosten lukumäärän.

            Args:
                query (String): hakusana

            Returns:
                int: hakutulosten lukumäärä
        """
        return self._repository.count_results(query=query)

    def search_projects(self, query, page, page_size):
        """Etsii hankkeita hakusanalla.

            Args:
                query (String): hakusana
                page (String): näytettävän sivun numero koko hausta
                page_size (String): näytettävän sivun koko

            Returns:
                List<Project>: lista löytyneitä hankeolioita   
        """
        return self._repository.find_projects_by_page(query, page, page_size)

    def get_project(self, project_id):
        """Hakee hankkeen tunnusluvulla.

            Args:
                project_id (int): hankkeen tunnusluku

            Returns:
                Project: hankeolio
        """
        return self._repository.get_project(project_id)


default_project_service = ProjectService()
