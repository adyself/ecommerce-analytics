import os
from sqlalchemy import create_engine
from sqlalchemy.engine import URL

user = os.getenv("POSTGRES_USER", "postgres")
password = os.getenv("POSTGRES_PASSWORD", "postgres")
host = os.getenv("POSTGRES_HOST", "db")  # имя сервиса БД в docker-compose
port = int(os.getenv("POSTGRES_PORT", "5432"))
dbname = os.getenv("POSTGRES_DB", "ecomm")

url = URL.create(
    "postgresql+psycopg2",
    username=user,
    password=password,
    host=host,
    port=port,
    database=dbname,
)

engine = create_engine(url)

