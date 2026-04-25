from bcrypt import gensalt, hashpw, checkpw
from config import PASSWORD_MIN_LENGHT


class PasswordService:
    """Tarjoaa salasanapalveluja."""

    def __init__(self, pw_min_lenght=PASSWORD_MIN_LENGHT):
        self._pw_min_lenght = pw_min_lenght

    def hash_password(self, password):
        """Salaa salasanan luomalla siitä uuden merkkijonon hajauttamalla.

            Muuttujat:
                password: salasana

                Palauttaa:
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

                Palauttaa:
                    bool: True, jos salasanat täsmäävät, muuten False 
        """
        password_bytes = password_hash.encode('utf-8')
        compare_bytes = password_compare.encode('utf-8')
        return checkpw(compare_bytes, password_bytes)

    def password_long_enough(self, password):
        """Tarkistaa onko salasana tarpeeksi pitkä.

            Muutujat:
                password: salasana

                Palauttaa:
                    bool: True, jos salasana on riittävän pitkä, muuten False 
        """
        if len(password) < self._pw_min_lenght:
            return False
        return True

    def get_min_password_lenght(self):
        """Antaa palveluun asetetun salasanan minimipituuden.

            Palauttaa:
                PASSWORD_MIN_LENGHT (int): salasanan minimipituus
        """
        return self._pw_min_lenght


default_pw_service = PasswordService()
