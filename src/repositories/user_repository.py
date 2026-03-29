
class UserRepository:
    """Luokka vastaa käyttäjien tietokantatoiminnoista.
    
        Attribuutit:
            _db (DatabaseInterface): tietokannan käyttöliittymäolio
    """

    def __init__(self, database):
        """Luo käyttäjärepo.

            Muuttujat:
                database (DatabaseInterface): tietokannan käyttöliittymäolio
        """
        self._db = database

    def get_user(self, user_id):
        """Metodi hakee käyttäjää tunnusnumerolla.
        
        Muuttujat:
            user_id: käyttäjän tunnusnumero tietokannassa

        Palauttaa:
            tuple: monikko, joka sisältää yhden käyttäjän tunnusnumeron ja käyttäjänimen
        """
        sql = """SELECT Users.id,
                    Users.username
            FROM Users
            AND Users.id = ?"""

        result = self._db.query(sql, [user_id])
        return result[0]

    def find_user_by_name(self, username):
        """Metodi etsii käyttäjää käyttäjänimellä.
        
        Muuttujat:
            username (string): käyttäjän tunnusnumero tietokannassa

        Palauttaa:
            lista: lista käyttäjänimiä monikkojen sisällä
        """
        sql = "SELECT username FROM Users WHERE username = ?"
        return self._db.query(sql, [username])

    def add_user(self, user):
        """Metodi lisää käyttäjän tietokantaan.
        
        Muuttujat:
            user (User): käyttäjäolio

        Palauttaa:
            user (User): käyttäjäolio
        """
        sql_users = "INSERT INTO Users (username, password_hash) VALUES (?, ?)"
        user_id = self._db.execute(sql_users, [user.username, user.password])
        user.id = user_id
        return user
