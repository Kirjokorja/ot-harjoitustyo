from entities.user import User
from database.db import (database as default_db)
from repositories.repository import RepositoryBase


class UserRepository(RepositoryBase):
    """Luokka vastaa käyttäjien tietokantatoiminnoista.

        Attributes:
            _db (DatabaseInterface): tietokannan käyttöliittymäolio
    """

    def __init__(self, db=default_db):
        super().__init__(db)

    def _get_user_from_row(self, row):
        return User(u_id=row["id"], username=row["username"], password=row["password_hash"])

    def _get_users_from_rows(self, rows):
        return list(map(self._get_user_from_row, rows))

    def find_user_by_name(self, username):
        """Metodi etsii käyttäjää käyttäjänimellä.

        Args:
            username (string): käyttäjän tunnusnumero tietokannassa

        Returns:
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

        Args:
            user (User): käyttäjäolio

        Returns:
            user (User): käyttäjäolio
        """
        sql_users = "INSERT INTO Users (username, password_hash) VALUES (?, ?)"
        user_id = self._db.execute(sql_users, [user.username, user.password])
        user.u_id = user_id
        return user


default_user_repository = UserRepository()
