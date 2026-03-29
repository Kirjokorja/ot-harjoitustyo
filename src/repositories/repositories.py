from repositories.user_repository import UserRepository

class Repositories:
    """Luokka kokoaa tietokantatoiminnot yhteen.
    
        Attribuutit:
            _db: tietokannasta vastaava olio 
    """

    def __init__(self, database):
        """Alusta tietokantatoiminnot.
        
            Muuttujat:
                database: tietokannasta vastaava olio
        """
        self._db = database

    def get_user_repository(self):
        """Luo tietokannan käyttäjätoiminnoista vastaavan olion.

            Palauttaa:
                UserRepository: tietokannan käyttäjätoiminnoista vastaava olio
        """
        return UserRepository(self._db)
