from entities.user import User
from services.service import ServiceBase
from services.password_service import default_pw_service
from exceptions import (user_exceptions as default_exceptions)
from repositories.user_repository import default_user_repository
import config as default_config


class UserService(ServiceBase):
    """Luokka vastaa käyttäjään liittyvistä toiminnoista sovelluksessa.

        Attributes:
            _repository (UserRepository):
                käyttäjien tietokantatoiminnoista vastaava olio
            _exceptions: käyttäjävirheet
            _password_service: salasanankäsittelypalvelu
            _user: istunnon käyttäjäolio
            _username_min_lenght (int): käyttäjänimen minimipituus
            _configs: palvelun ominaisuuksien arvot tiedostossa
    """

    def __init__(
        self,
        repository=default_user_repository,
        exceptions=default_exceptions,
        password_service=default_pw_service,
        configs=default_config
    ):
        """Alusta käyttäjäpalvelu.

            Args:
                repository (UserRepository):
                    käyttäjien tietokantatoiminnoista vastaava olio
                exceptions: käyttäjävirheet
                password_service: salasanankäsittelypalvelu
                configs: palvelun ominaisuuksien arvot tiedostossa
        """
        super().__init__(repository=repository, exceptions=exceptions)
        self._password_service = password_service
        self._configs = configs
        self._user = None

    def create_user(self, username, password, password_confirm):
        """Metodi luo uuden käyttäjän.

            Args:
                username (str): käyttäjänimi
                password (str): käyttäjän salasana
                password_confirm (str): vahvistussalasana

            Raises:
                UserAlreadyExists: virhe, joka syntyy käyttäjätunnuksen ollessa jo käytössä

            Returns:
                User: käyttäjäolio
        """
        self._username_acceptable(username=username)
        self._password_acceptable(
            password=password, password_confirm=password_confirm)
        self._user_exists(username=username)
        password_hash = self._password_service.hash_password(password)
        user = self._repository.add_user(
            User(username=username, password=password_hash))
        return user

    def _user_exists(self, username):
        user_check = self._repository.find_user_by_name(username)
        if user_check:
            message = f"Käyttäjänimi {user_check.username} on jo käytössä."
            raise self._exceptions.UserAlreadyExists(message)

    def _username_acceptable(self, username):
        if len(username) < self._configs.USERNAME_MIN_LENGHT:
            message = "Käyttäjänimi on liian lyhyt."
            raise self._exceptions.UsernameTooShort(message)

    def _password_acceptable(self, password, password_confirm):
        if not self._password_service.password_long_enough(password):
            message = "Salasana on liian lyhyt."
            raise self._exceptions.PasswordTooShort(message)
        if password != password_confirm:
            message = "Salasanat eivät täsmää."
            raise self._exceptions.PasswordsDoNotMatch(message)

    def login(self, username, password):
        """Metodi kirjaa käyttäjän sisään.

            Args:
                username (str): käyttäjänimi
                password (str): käyttäjän salasana

            Raises:
                InvalidCredentials: virhe, joka syntyy väärän tunnuksen seurauksena
                ASessionAlreadyExists: virhe, joka syntyy jonkun ollessa jo kirjautuneena

            Returns:
                _user (User): istunnon käyttäjäolio
        """
        if self._user:
            raise self._exceptions.ASessionAlreadyExists(
                "Istunto on jo käynnissä.")

        user = self._repository.find_user_by_name(username)

        if not user or not self._password_service.password_match(user.password, password):
            raise self._exceptions.InvalidCredentials(
                "Käyttäjänimi tai salasana on virheellinen.")

        self._user = user

        return self._user

    def logout(self):
        """Metodi kirjaa käyttäjän ulos."""

        self._user = None

    def get_current_user(self):
        """Antaa istunnon käyttäjän.

            Raises:
                SessionNotFound: virhe, joka syntyy, kun käyttäjä ei ole kirjautuneena sisään

            Returns:
                User: käyttäjäolio 
        """
        if not self._user:
            raise self._exceptions.SessionNotFound("Istuntoa ei ole olemassa.")

        return self._user

    def get_min_password_lenght(self):
        return self._password_service.get_min_password_lenght()


default_user_service = UserService()
