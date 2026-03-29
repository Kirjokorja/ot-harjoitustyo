class User:
    """Luokka kuvaa yksittäistä käyttäjää.

    Attribuutit:
        id (int): käyttäjän tunnusnumero ja pääavain tietokannassa
        username (str): käyttäjän käyttäjänimi
        password (str): salasana hajautettuna merkkijonona
    """

    def __init__(self, user_id = None, username = None, password = None):
        """Alusta uusi käyttäjä.
        
        Muuttujat:
            id (int): käyttäjän tunnusnumero ja pääavain tietokannassa
            username (str): käyttäjän käyttäjänimi
            password (str): salasana hajautettuna merkkijonona
        """
        self.id = user_id
        self.username = username
        self.password = password
