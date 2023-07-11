import logging
import os

# import psycopg
from sqlalchemy import Column, Integer, String, Boolean, JSON
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import URL
from sqlalchemy.orm import declarative_base
from dotenv import load_dotenv  # remove this later

load_dotenv()  # remove this later

logging.basicConfig(
    filename="scraper.log",
    level=logging.DEBUG,
)


url = URL.create(
    "postgresql+psycopg",
    username=os.environ["POSTGRES_USER"],
    password=os.environ["POSTGRES_PASSWORD"],
    host=os.environ["POSTGRES_HOST"],
    port=os.environ["POSTGRES_PORT"],
    database=os.environ["POSTGRES_DB"],
)

engine = create_engine(url)

Base = declarative_base()
Base.metadata.create_all(bind=engine)
meta = MetaData()

metadata = MetaData()
my_table = Table(
    "wanted_list",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String),
    Column("surname", String),
    Column("birth_year", Integer),
    Column("birth_place", String),
    Column("terrorist_organization", String),
    Column("isactive", Boolean),
    Column("photos", JSON),
)

connection = engine.connect()
# Try to create the table, but ignore if it already exists
if not engine.dialect.has_table(connection, "wanted_list"):
    # Create the table
    my_table.create(bind=engine)
    logging.info("Wanted table is initialized.")
else:
    logging.info("Wanted table is already initialized.")
connection.close()


def get_db_session():
    Session = sessionmaker(bind=engine)
    session = Session()
    return session


def get_table():
    global my_table
    return my_table
