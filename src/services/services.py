from services.user_service import UserService

class Services:
    """Kokoaa palvelut yhteen.
    
        Attribuutit:
             _repos: tietokantatoiminnoista vastaava olio
             _exceptions: virhetapaukset
    """

    def __init__(self, repositories, exceptions):
        """Alusta palvelut.
        
            Muuttujat:
                repositories: tietokantatoiminnoista vastaava olio
                exceptions: virhetapaukset
        """
        self._repos = repositories
        self._exceptions = exceptions

    def get_user_service(self):
        """Luo käyttäjätoiminnoista vastaavan olion.
        
            Palauttaa:
                UserService: käyttäjäpalveluista vastaava olio
        """
        return UserService(self._repos.get_user_repository(), self._exceptions)
