import os
from dotenv import load_dotenv

currentdir = os.path.dirname(__file__)

try:
    load_dotenv(dotenv_path=os.path.join(currentdir, "..", "..", ".env.test"))
except FileNotFoundError:
    pass

# Tietokannan sijainti
TEST_DATABASE_FILENAME = os.getenv("TEST_DATABASE_FILENAME") or "test_database.db"
TEST_DATABASE_FILE_PATH = os.path.join(
    currentdir, "..", "..", "data", TEST_DATABASE_FILENAME)

# Tietokannan alustuskäskyt
TEST_DATABASE_SCHEMA_FILENAME = os.getenv(
    "TEST_DATABASE_SCHEMA_FILENAME") or "test_schema.sql"
TEST_DATABASE_SCHEMA_PATH = os.path.join(currentdir, "..", TEST_DATABASE_SCHEMA_FILENAME)
TEST_DATABASE_SEED_FILENAME = os.getenv("TEST_DATABASE_SEED_FILENAME") or "test_seed.sql"
TEST_DATABASE_SEED_PATH = os.path.join(
    currentdir, "..", TEST_DATABASE_SEED_FILENAME)
