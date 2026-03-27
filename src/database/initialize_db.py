import db
from config import DATABASE_SCHEMA, DATABASE_INIT

def drop_all_tables():
    """Metodi tyhjentää tietokannan tauluista."""

    sql_table_names = """
            SELECT tbl_name 
            FROM sqlite_master
            WHERE type = ?
        """

    result = db.query(sql_table_names, ['table'])

    sql_drop = "DROP TABLE VALUES (?)"
    db.executemany(sql_drop, result)
        
def create_tables():
    """Metodi luo tietokantaan taulut."""

    sql = """
            BEGIN; 
            ?
            COMMIT;
        """

    db.executescipt(sql, [DATABASE_SCHEMA])
    db.executescipt(sql, [DATABASE_INIT])

def initialize_database():
    """Metodi alustaa tietokannan."""

    drop_all_tables()
    create_tables()
