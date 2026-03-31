import os
from dotenv import load_dotenv

currentdir = os.path.dirname(__file__)

try:
    load_dotenv(dotenv_path=os.path.join(currentdir, "..", "..", ".env.test"))
except FileNotFoundError:
    pass

#Tietokannan sijainti
DATABASE_FILENAME = os.getenv("DATABASE_FILENAME") or "test_database.db"
DATABASE_FILE_PATH = os.path.join(currentdir, "..", "..", "data", DATABASE_FILENAME)

#Tietokannan alustusarvot
DATABASE_SCHEMA = os.getenv("DATABASE_SCHEMA") or """
        CREATE TABLE Users (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE,
            password_hash TEXT
        );
    """
DATABASE_CONTENT = os.getenv("DATABASE_CONTENT") or """
        INSERT INTO Users (username, password_hash) VALUES ('Unhola', 'testi1');
        INSERT INTO Users (username, password_hash) VALUES ('Aava', 'testi2');
        INSERT INTO Users (username, password_hash) VALUES ('Pekka', 'testi3');
        INSERT INTO Users (username, password_hash) VALUES ('Tindeus', 'testi4');
    """