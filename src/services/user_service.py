from entities.user import User
from exceptions import (user_exceptions as default_exceptions)
from repositories.user_repository import (
    user_repository as default_user_repository)
from services.password_service import (password_service as default_pw_service)
from config import USERNAME_MIN_LENGHT


class UserService:
    """Luokka vastaa käyttäjään liittyvistä toiminnoista sovelluksessa.

        Attribuutit:
            _user_repository (UserRepository): 
                käyttäjkäyttäjien tietokantatoiminnoista vastaava olio
            _exceptions: käyttäjävirheet
            _password_service: salasanankäsittelypalvelu
            _user: istunnon käyttäjäolio
    """

    def __init__(self, user_repository=default_user_repository,
                 exceptions=default_exceptions,
                 password_service=default_pw_service
                 ):
        """Alusta käyttäjäpalvelu.

            Muuttujat:
                user_repository (UserRepository): 
                    käyttäjkäyttäjien tietokantatoiminnoista vastaava olio
                exceptions: käyttäjävirheet
                password_service: salasanankäsittelypalvelu
        """
        self._user_repository = user_repository
        self._exceptions = exceptions
        self._password_service = password_service
        self._user = None

    def create_user(self, username, password, password_confirm):
        """Metodi luo uuden käyttäjän.

            Muuttujat:
                username (str): käyttäjänimi
                password (str): käyttäjän salasana
                password_confirm (str): vahvistussalasana

            Ilmoittaa:
                UserAlreadyExists: virhe, joka syntyy käyttäjätunnuksen ollessa jo käytössä

            Palauttaa:
                User: käyttäjäolio
        """
        if (self._username_acceptable(username) and
                self._password_acceptable(password, password_confirm)):
            user_check = self._user_repository.find_user_by_name(username)
            if user_check:
                message = f"Käyttäjänimi {user_check.username} on jo käytössä."
                raise self._exceptions.UserAlreadyExists(message)
            password_hash = self._password_service.hash_password(password)
            return self._user_repository.add_user(
                User(username=username, password=password_hash))
        return None

    def _username_acceptable(self, username):
        if len(username) < USERNAME_MIN_LENGHT:
            message = "Käyttäjänimi on liian lyhyt."
            raise self._exceptions.UsernameTooShort(message)
        return True

    def _password_acceptable(self, password, password_confirm):
        if not self._password_service.password_long_enough(password):
            message = "Salasana on liian lyhyt."
            raise self._exceptions.PasswordTooShort(message)
        if password != password_confirm:
            message = "Salasanat eivät täsmää."
            raise self._exceptions.PasswordsDoNotMatch(message)
        return True

    def login(self, username, password):
        """Metodi kirjaa käyttäjän sisään.

            Muuttujat:
                username (str): käyttäjänimi
                password (str): käyttäjän salasana

            Ilmoittaa:
                InvalidCredentials: virhe, joka syntyy väärän tunnuksen seurauksena
        """
        user = self._user_repository.find_user_by_name(username)

        if not user or not self._password_service.password_match(user.password, password):
            raise self._exceptions.InvalidCredentials(
                "Väärä käyttäjänimi tai salasana")

        self._user = user

    def logout(self):
        """Metodi kirjaa käyttäjän ulos."""

        self._user = None

    def get_current_user(self):
        """Antaa istunnon käyttäjän.

            Ilmoittaa:
                NoSessionFound: virhe, joka syntyy, kun käyttäjä ei ole kirjautuneena sisään

            Palauttaa:
                User: käyttäjäolio 
        """
        if not self._user:
            raise self._exceptions.NoSessionFound("Istuntoa ei ole olemassa.")

        return self._user

    def get_exceptions(self):
        """Antaa palvelun virheilmoitusluokat.

            Palauttaa:
                _exceptions: palvelun virheilmoitusluokat
        """
        return self._exceptions

    def get_min_password_lenght(self):
        return self._password_service.get_min_password_lenght()


user_service = UserService()
