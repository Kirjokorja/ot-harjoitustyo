from repositories.user_repository import UserRepository
from database.db import (database as default_db)

class Repositories:
    """Luokka kokoaa tietokantatoiminnot yhteen.
    
        Attribuutit:
            _db: tietokannasta vastaava olio 
    """

    def __init__(self, db=default_db):
        """Alusta tietokantatoiminnot.
        
            Muuttujat:
                database: tietokannasta vastaava olio
        """
        self._db = db

    def get_user_repository(self):
        """Luo tietokannan käyttäjätoiminnoista vastaavan olion.

            Palauttaa:
                UserRepository: tietokannan käyttäjätoiminnoista vastaava olio
        """
        return UserRepository(self._db)

repository = Repositories()
