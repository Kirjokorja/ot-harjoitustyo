from services.user_service import UserService

class Services:
    """Kokoaa palvelut yhteen.
    
        Attribuutit:
             _repos: tietokantatoiminnoista vastaava olio
    """

    def __init__(self, repositories):
        """Alusta palvelut.
        
            Muuttujat:
                tietokantatoiminnoista vastaava olio
        """
        self._repos = repositories

    def get_user_service(self):
        """Luo käyttäjätoiminnoista vastaavan olion.
        
            Palauttaa:
                UserService: käyttäjäpalveluista vastaava olio
        """
        return UserService(self._repos.get_user_repository())
