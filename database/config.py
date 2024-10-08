import os
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()
user = os.getenv("DB_USERNAME")
password = os.getenv("DB_PASSWORD")
host = os.getenv("DB_HOST")
port = os.getenv("DB_PORT")
database = os.getenv("DB_DATABASE")

DATABASE_URL = "postgresql+psycopg://{0}:{1}@{2}:{3}/{4}".format(
    user, password, host, port, database)


def openConnection():
    try:
        db = create_engine(DATABASE_URL)
        return db
    except Exception as e:
        print(e)
        print("Database connection error. Terminating..")
        exit(1)
