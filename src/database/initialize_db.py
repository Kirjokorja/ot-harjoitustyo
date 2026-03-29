from database.db import DatabaseInterface

class DatabaseInitializer:
    """Luokka vastaa tietokannan alustamisesta.

        Attribuutit:
            _db (DatabaseInterface): tietokannan käyttöliittymäolio
            _schema (str): tietokantakaavio
            _content (str): tietokantaan lisättävä sisältö
    """
    def __init__(self, file_path, schema, content):
        """Luo tietokannan alustusolio.

        Muuttujat:
            file_path (str): tietokannan sijainti
            schema (str): tietokantakaavio
            content (str): tietokantaan lisättävä sisältö
        """
        self._db = DatabaseInterface(file_path)
        self._schema = schema
        self._content = content

    def _drop_all_tables(self):
        """Metodi tyhjentää tietokannan tauluista."""

        sql_table_names = """
                SELECT tbl_name 
                FROM sqlite_master
                WHERE type = ?
            """

        result = self._db.query(sql_table_names, ['table'])

        if result:
            sql_drop = "DROP TABLE IF EXISTS "
            for row in result:
                sql_drop += row["tbl_name"] + ";"
            self._db.executescript(sql_drop)

    def _create_tables(self):
        """Metodi luo tietokantaan taulut."""

        self._db.executescript(self._schema)

    def _create_content(self):
        """Metodi lisää tietokohteita tietokantaan."""
        self._db.executescript(self._content)

    def initialize_database(self):
        """Metodi alustaa tietokannan."""

        self._drop_all_tables()
        self._create_tables()
        if self._content:
            self._create_content()
