from database.initialize_db import DatabaseInitializer
from database.db import DatabaseInterface
from config import DATABASE_FILE_PATH, DATABASE_SCHEMA_PATH, DATABASE_SEED_PATH


def build():
    database = DatabaseInterface(DATABASE_FILE_PATH)
    initializer = DatabaseInitializer(
        database, DATABASE_SCHEMA_PATH, DATABASE_SEED_PATH)
    initializer.initialize_database()


if __name__ == "__main__":
    build()
