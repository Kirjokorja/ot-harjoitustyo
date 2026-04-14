import os
from dotenv import load_dotenv

currentdir = os.path.dirname(__file__)

try:
    load_dotenv(dotenv_path=os.path.join(currentdir, "..", "..", ".env.test"))
except FileNotFoundError:
    pass

# Tietokannan sijainti
DATABASE_FILENAME = os.getenv("DATABASE_FILENAME") or "test_database.db"
DATABASE_FILE_PATH = os.path.join(
    currentdir, "..", "..", "data", DATABASE_FILENAME)

# Tietokannan alustuskäskyt
DATABASE_SCHEMA_FILENAME = os.getenv(
    "DATABASE_SCHEMA_FILENAME") or "schema.sql"
DATABASE_SCHEMA_PATH = os.path.join(currentdir, "..", DATABASE_SCHEMA_FILENAME)
DATABASE_SEED_FILENAME = os.getenv("DATABASE_SEED_FILENAME") or "seed.sql"
DATABASE_SEED_PATH = os.path.join(
    currentdir, "..", DATABASE_SEED_FILENAME)
