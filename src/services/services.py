from services.user_service import (user_service as default_user_service)


class Services:
    """Kokoaa palvelut yhteen.

        Attribuutit:
             _user_service: salasanankäsittelypalvelu
    """

    def __init__(self, user_service=default_user_service):
        """Alusta palvelut.

            Muuttujat:
                user_service: salasanankäsittelypalvelu

        """
        self._user_service = user_service

    def get_user_service(self):
        """Luo käyttäjätoiminnoista vastaavan olion.

            Palauttaa:
                UserService: käyttäjäpalveluista vastaava olio
        """
        return self._user_service


services = Services()
