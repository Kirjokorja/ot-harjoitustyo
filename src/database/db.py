import sqlite3
from config import DATABASE_FILE_PATH

class DatabaseInterface:
    """Luokka vastaa tietokantayhteydestä ja -toiminnoista."""

    def _get_connection(self):
        con = sqlite3.connect(DATABASE_FILE_PATH)
        con.execute("PRAGMA foreign_keys = ON")
        con.row_factory = sqlite3.Row
        return con

    def query(self, sql, params):
        """Lähettää kyselyn tietokannalle.
        
            Args:
                sql: kyselyn lause
                params: kyselyyn liitettävät lausekkeet
        """
        con = self._get_connection()
        result = con.execute(sql, params).fetchall()
        con.close()
        return result

    def execute(self, sql, params):
        """Lähettää komennon tietokannalle.
        
            Args:
                sql: komennon lause
                params: lauseeseen liitettävät lausekkeet
        """
        con = self._get_connection()
        result = con.execute(sql, params)
        con.commit()
        con.close()
        return result.lastrowid

    def executemany(self, sql, params):
        """Lähettää useamman kerran saman komennon tietokannalle.
        
            Args:
                sql: komennon lause
                params: lausekkeet kulleekkin komentoajolle
        """
        con = self._get_connection()
        result = con.executemany(sql, params)
        con.commit()
        con.close()

    def executescript(self, sql, params):
        """Lähettää useamman komennon tietokannalle.
        
            Args:
                sql: komentojen lauseet
                params: lauseisiin liitettävät lausekkeet
        """
        con = self._get_connection()
        result = con.executemany(sql, params)
        con.commit()
        con.close()

