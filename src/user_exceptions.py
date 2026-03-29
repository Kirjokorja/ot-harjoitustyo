
class UserAlreadyExists(Exception):
    """Luokka käsittelee ilmoituksia poikkeustilanteessa, jossa käyttäjä on jo olemassa."""

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
