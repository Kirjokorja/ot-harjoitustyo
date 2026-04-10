
class UserAlreadyExists(Exception):
    """Luokka käsittelee ilmoituksia poikkeustilanteessa, jossa käyttäjä on jo olemassa."""

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class PasswordTooShort(Exception):
    """Luokka käsittelee ilmoituksia poikkeustilanteessa, jossa salasana on liian lyhyt."""

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class PasswordsDoNotMatch(Exception):
    """Luokka käsittelee ilmoituksia poikkeustilanteessa, jossa salasanat eivät täsmää."""

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class UsernameTooShort(Exception):
    """Luokka käsittelee ilmoituksia poikkeustilanteessa, jossa käyttäjänimi on liian lyhyt."""

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class InvalidCredentials(Exception):
    """Luokka käsittelee ilmoituksia poikkeustilanteessa, jossa tunnus tai salasana ei ole oikein."""

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
