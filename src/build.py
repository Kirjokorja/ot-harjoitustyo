from database.initialize_db import DatabaseInitializer
from config import DATABASE_FILE_PATH, DATABASE_SCHEMA, DATABASE_CONTENT

def build():
    initializer = DatabaseInitializer(DATABASE_FILE_PATH, DATABASE_SCHEMA, DATABASE_CONTENT)
    initializer.initialize_database()

if __name__=="__main__":
    build()
