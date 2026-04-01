from services.user_service import UserService
from services.password_service import (password_service as default_pw_service)
from repositories.repositories import (repository as default_repository)
from exceptions import (exceptions as default_exceptions)


class Services:
    """Kokoaa palvelut yhteen.

        Attribuutit:
             _repos: tietokantatoiminnoista vastaava olio
             _exceptions: virhetapaukset
             _password_service: salasanankäsittelypalvelu
    """

    def __init__(self, repositories=default_repository,
                 exceptions=default_exceptions,
                 pasword_service=default_pw_service
                 ):
        """Alusta palvelut.

            Muuttujat:
                repositories: tietokantatoiminnoista vastaava olio
                exceptions: virhetapaukset
                password_service: salasanankäsittelypalvelu
        """
        self._repos = repositories
        self._exceptions = exceptions
        self._password_service = pasword_service

    def get_user_service(self):
        """Luo käyttäjätoiminnoista vastaavan olion.

            Palauttaa:
                UserService: käyttäjäpalveluista vastaava olio
        """
        return UserService(self._repos.get_user_repository(),
                           self._exceptions,
                           self._password_service
                           )


services = Services()
