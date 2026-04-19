class User:
    """Luokka kuvaa yksittäistä käyttäjää.

    Attribuutit:
        u_id (int): käyttäjän tunnusluku ja pääavain tietokannassa
        username (str): käyttäjänimi
        password (str): salasana hajautettuna merkkijonona
    """

    def __init__(self, u_id=None, username=None, password=None):
        """Alusta uusi käyttäjä.

        Muuttujat:
            u_id (int): käyttäjän tunnusnumero ja pääavain tietokannassa
            username (str): käyttäjän käyttäjänimi
            password (str): salasana hajautettuna merkkijonona
        """
        self.u_id = u_id
        self.username = username
        self.password = password
