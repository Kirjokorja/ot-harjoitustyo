from entities.user import User
from database.db import (database as default_db)
from repositories.repository import RepositoryBase


class UserRepository(RepositoryBase):
    """Luokka vastaa käyttäjien tietokantatoiminnoista.

        Attribuutit:
            _db (DatabaseInterface): tietokannan käyttöliittymäolio
    """

    def __init__(self, db=default_db):
        super().__init__(db)

    def _get_user_from_row(self, row):
        if row:
            return User(u_id=row["id"], username=row["username"], password=row["password_hash"])
        return None

    def _get_users_from_rows(self, rows):
        return list(map(self._get_user_from_row, rows))

    def get_user(self, user_id):
        """Metodi hakee käyttäjää tunnusnumerolla.

        Muuttujat:
            user_id: käyttäjän tunnusnumero tietokannassa

        Palauttaa:
            User: käyttäjäolio
        """
        sql = """SELECT Users.id,
                    Users.username
            FROM Users
            AND Users.id = ?"""

        result = self._db.query(sql, [user_id])
        return self._get_user_from_row(result[0])

    def find_user_by_name(self, username):
        """Metodi etsii käyttäjää käyttäjänimellä.

        Muuttujat:
            username (string): käyttäjän tunnusnumero tietokannassa

        Palauttaa:
            User: käyttäjäolio
        """
        user = None
        sql = "SELECT id, username, password_hash FROM Users WHERE username = ?"
        query_list = self._db.query(sql, [username])
        if query_list:
            user = self._get_users_from_rows(query_list)[0]
        return user

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


default_user_repository = UserRepository()
