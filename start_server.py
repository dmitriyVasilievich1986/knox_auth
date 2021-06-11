from django.core.management import execute_from_command_line
from os import environ
from time import sleep
import psycopg2
import logging

logging.basicConfig(level=logging.INFO)
logger: logging.Logger = logging.getLogger(__name__)

ATTEMPT_DELAY: int = 20
MAX_ATTEMPTS: int = 5

DB_PASSWORD: str = environ.get("DB_PASSWORD", "root")
DB_USER: str = environ.get("DB_USER", "postgres")
DB_NAME: str = environ.get("DB_DBNAME", "astra")

HOST: str = environ.get("HOST", "localhost")
PORT: int = environ.get("PORT", 8000)

DB_HOST: str = environ.get("DB_HOST", "localhost")
DB_PORT: int = environ.get("DB_PORT", 5432)

db_data_string: str = f"dbname={DB_NAME} user={DB_USER} password={DB_PASSWORD} host={DB_HOST} port={DB_PORT}"

while MAX_ATTEMPTS:
    logger.info(
        f"Try to connect to DB: {db_data_string}. Attempts left: {MAX_ATTEMPTS}"
    )
    try:
        conn = psycopg2.connect(
            password=DB_PASSWORD,
            dbname=DB_NAME,
            user=DB_USER,
            host=DB_HOST,
            port=DB_PORT,
        )
        conn.close()
        logger.info("Connected successfully")
        break
    except (psycopg2.OperationalError, Exception) as err:
        logger.error(err)
        MAX_ATTEMPTS -= 1
    MAX_ATTEMPTS and sleep(ATTEMPT_DELAY)

if MAX_ATTEMPTS:
    environ.setdefault("DJANGO_SETTINGS_MODULE", "auth.settings")
    execute_from_command_line(["manage.py", "makemigrations"])
    execute_from_command_line(["manage.py", "migrate"])
    execute_from_command_line(["manage.py", "runserver", f"{HOST}:{PORT}"])
