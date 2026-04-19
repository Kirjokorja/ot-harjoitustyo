
class TypeClass:
    """Luokka kuvaa tietokohteiden luokkia tietokannassa.

    Attribuutit:
        t_id (int): luokan tunnusluku ja pääavain tietokannassa
        title (str): luokan nimi
        value (str): luokkaan kuuluva arvo
    """

    def __init__(self, t_id=None, title=None, value=None):
        """Alusta uusi käyttäjä.

        Muuttujat:
            t_id (int): yksilöivä tunnusluku
            title (str): tietokohteen nimi
            value (str): luokka-arvo
        """
        self.t_id = t_id
        self.title = title
        self.value = value
