from database.initialize_db import DatabaseInitializer
from database.db import DatabaseInterface
from config import DATABASE_FILE_PATH, DATABASE_SCHEMA, DATABASE_CONTENT


def build():
    database = DatabaseInterface(DATABASE_FILE_PATH)
    initializer = DatabaseInitializer(
        database, DATABASE_SCHEMA, DATABASE_CONTENT)
    initializer.initialize_database()


if __name__ == "__main__":
    build()
