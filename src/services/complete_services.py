from services.user_service import default_user_service
from services.project_service import default_project_service


class Services:
    """Kokoaa palvelut yhteen.

        Attribuutit:
             _user_service (UserService): salasanankäsittelypalvelu
             _project_service (ProjectService): hankkeiden käsittelypalvelu
    """

    def __init__(
        self,
        user_service=default_user_service,
        project_service=default_project_service
    ):
        """Alusta palvelut.

            Muuttujat:
                user_service (UserService): salasanankäsittelypalvelu
                project_service (ProjectService): hankkeiden käsittelypalvelu

        """
        self._user_service = user_service
        self._project_service = project_service

    def get_user_service(self):
        """Antaa käyttäjätoiminnoista vastaavan olion.

            Palauttaa:
                UserService: käyttäjäpalveluista vastaava olio
        """
        return self._user_service

    def get_project_service(self):
        """Antaa hanketoiminnoista vastaavan olion.

            Palauttaa:
                ProjectService: hankepalveluista vastaava olio
        """
        return self._project_service


default_services = Services()
