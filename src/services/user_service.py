from entities.user import User
from user_exceptions import UserAlreadyExists

class UserService:
    """Luokka vastaa käyttäjään liittyvistä toiminnoista sovelluksessa.
    
        Attribuutit:
            _user_repository (UserRepository): 
                käyttäjkäyttäjien tietokantatoiminnoista vastaava olio
    """

    def __init__(self, user_repository):
        """Alusta käyttäjäpalvelu.
    
        Muuttujat:
            user_repository (UserRepository): käyttäjkäyttäjien tietokantatoiminnoista vastaava olio
    """
        self._user_repository = user_repository

    def create_user(self, username, password):
        """Metodi luo uuden käyttäjän.

        Muuttujat:
            username (str): käyttäjänimi
            password (str): käyttäjän salasana

        Ilmoittaa:
            UserAlreadyExists: virhe, joka syntyy käyttäjätunnuksen ollessa jo käytössä

        Palauttaa:
            ueser (User): käyttäjäolio
        """
        user_check = self._user_repository.find_user_by_name(username)
        if user_check:
            raise UserAlreadyExists(f"Käyttäjänimi {user_check[0]["username"]} on jo käytössä.")
        user = self._user_repository.add_user(User(username=username, password=password))
        return user
