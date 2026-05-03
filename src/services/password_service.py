from bcrypt import gensalt, hashpw, checkpw
import config as default_config


class PasswordService:
    """Tarjoaa salasanapalveluja.

        Attributes:
            _configs: palvelun ominaisuuksien arvot tiedostossa
    """

    def __init__(self, configs=default_config):
        """Luo uuden salasanapalveluolion.

            Args:
                configs: palvelun ominaisuuksien arvot tiedostossa
        """
        self._configs = configs

    def hash_password(self, password):
        """Salaa salasanan luomalla siitä uuden merkkijonon hajauttamalla.

            Args:
                password: salasana

                Returns:
                    String: hajautettu merkkijono
        """
        salt = gensalt()
        password_bytes = password.encode('utf-8')
        return hashpw(password_bytes, salt).decode('utf-8')

    def password_match(self, password_hash, password_compare):
        """Vertaa kahta salasanaa keskenään.

            Muutujat:
                password_hash: salattu salasana
                password_compare: salaamaton salasana, jota verrataan salattuun

                Returns:
                    bool: True, jos salasanat täsmäävät, muuten False 
        """
        password_bytes = password_hash.encode('utf-8')
        compare_bytes = password_compare.encode('utf-8')
        return checkpw(compare_bytes, password_bytes)

    def password_long_enough(self, password):
        """Tarkistaa onko salasana tarpeeksi pitkä.

            Muutujat:
                password: salasana

                Returns:
                    bool: True, jos salasana on riittävän pitkä, muuten False 
        """
        if len(password) < self._configs.PASSWORD_MIN_LENGHT:
            return False
        return True

    def get_min_password_lenght(self):
        """Antaa palveluun asetetun salasanan minimipituuden.

            Returns:
                int: salasanan minimipituus
        """
        return self._configs.PASSWORD_MIN_LENGHT


default_pw_service = PasswordService()
