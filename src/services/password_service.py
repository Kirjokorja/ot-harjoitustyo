from bcrypt import gensalt, hashpw, checkpw
from config import PASSWORD_MIN_LENGHT


class PasswordService:
    """Tarjoaa salasanapalveluja."""

    def __init__(self):
        pass

    def hash_password(self, password):
        """Salaa salasanan luomalla siitä uuden merkkijonon hajauttamalla.

            Muuttujat:
                password: salasana

                Palauttaa:
                    hash: hajautettu merkkijono
        """
        salt = gensalt()
        password_bytes = password.encode("utf-8")
        return hashpw(password_bytes, salt)

    def password_match(self, password_hash, password_compare):
        """Vertaa kahta salasanaa keskenään.

            Muutujat:
                password_hash: salattu salasana
                password_compare: salaamaton salasana, jota verrataan salattuun

                Palauttaa:
                    bool: True, jos salasanat täsmäävät, muuten False 
        """
        compare_bytes = password_compare.encode('utf-8')
        return checkpw(compare_bytes, password_hash)

    def password_long_enough(self, password):
        """Tarkistaa onko salasana tarpeeksi pitkä.

            Muutujat:
                password: salasana

                Palauttaa:
                    bool: True, jos salasana on riittävän pitkä, muuten False 
        """
        if len(password) < PASSWORD_MIN_LENGHT:
            return False
        return True


password_service = PasswordService()
