import sqlite3
from config import DATABASE_FILE_PATH


class DatabaseInterface:
    """Luokka vastaa tietokantayhteydestä ja -toiminnoista.

        Attribuutit:
            _file_path (str): tietokannan sijainti
    """

    def __init__(self, file_path):
        """Luo tietokannan käyttöliittymää hallinoiva olio.

            Muuttujat:
                file_path (str): tietokannan sijainti
        """
        self._file_path = file_path

    def _get_connection(self):
        con = sqlite3.connect(self._file_path)
        con.execute("PRAGMA foreign_keys = ON")
        con.row_factory = sqlite3.Row
        return con

    def query(self, sql, params):
        """Lähettää kyselyn tietokannalle.

        Muuttujat:
            sql (str): kyselyn lause
            params (list): kyselyyn liitettävät lausekkeet

        Palauttaa:
            list: lista kyselyn luoman taulun rivejä
        """
        con = self._get_connection()
        result = con.execute(sql, params).fetchall()
        con.close()
        return result

    def execute(self, sql, params):
        """Lähettää komennon tietokannalle.

        Muuttujat:
            sql (str): komennon lause
            params (list): lauseeseen liitettävät lausekkeet

        Palauttaa:
            int: viimeisimmän tietokantaan lisätyn rivin pääavain
        """
        con = self._get_connection()
        result = con.execute(sql, params)
        row_id = result.lastrowid
        con.commit()
        con.close()
        return row_id

    def executemany(self, sql, params):
        """Lähettää useamman kerran saman komennon tietokannalle.

        Muuttujat:
            sql (string): komennon lause
            params (list): lausekkeet kulleekkin komentoajolle
        """
        con = self._get_connection()
        con.executemany(sql, params)
        con.commit()
        con.close()

    def executescript(self, statements):
        """Lähettää useamman komennon tietokannalle.

        Muuttujat:
            statements (str): komentojen lauseet
        """
        con = self._get_connection()
        con.executescript(statements)
        con.commit()
        con.close()


database = DatabaseInterface(DATABASE_FILE_PATH)
