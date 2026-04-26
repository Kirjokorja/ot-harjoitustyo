import locale
from database.db import (database as default_db)
from config import (DATABASE_SCHEMA_PATH as default_schema,
                    DATABASE_SEED_PATH as default_seed)


class DatabaseInitializer:
    """Luokka vastaa tietokannan alustamisesta.

        Attributes:
            _db (DatabaseInterface): tietokannan käyttöliittymäolio
            _schema (str): sql tietokantakaaviotiedosto
            _seed (str): tietokannan alustussisältötiedosto
    """

    def __init__(self, database=default_db, schema=default_schema, seed=default_seed):
        """Luo tietokannan alustusolio.

        Args:
            file_path (str): tietokannan sijainti
            schema (str): sql tietokantakaaviotiedosto
            seed (str): tietokannan alustussisältötiedosto
        """
        self._db = database
        self._schema = schema
        self._seed = seed

    def _drop_all_tables(self):
        """Metodi tyhjentää tietokannan tauluista."""

        sql_table_names = """
                SELECT tbl_name 
                FROM sqlite_master
                WHERE type = ?
            """

        result = self._db.query(sql_table_names, ['table'])

        if result:
            statement = "DROP TABLE IF EXISTS "
            sql_drop = ""
            for table in result:
                sql_drop += statement + table['tbl_name'] + ";"
            self._db.executescript(sql_drop)

    def _create_tables(self):
        """Metodi luo tietokantaan taulut."""

        with open(self._schema, encoding=locale.getencoding()) as file:
            sql = file.read()
        self._db.executescript(sql)

    def _create_content(self):
        """Metodi lisää tietokohteita tietokantaan."""

        with open(self._seed, encoding=locale.getencoding()) as file:
            sql = file.read()
        self._db.executescript(sql)

    def initialize_database(self):
        """Metodi alustaa tietokannan."""

        self._drop_all_tables()
        self._create_tables()
        if self._seed:
            self._create_content()
