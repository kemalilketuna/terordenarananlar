import os
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import URL
from sqlalchemy.orm import declarative_base
from dotenv import load_dotenv  # remove this later

load_dotenv()  # remove this later


url = URL.create(
    "postgresql+psycopg",
    username=os.environ["POSTGRES_USER"],
    password=os.environ["POSTGRES_PASSWORD"],
    host=os.environ["POSTGRES_HOST"],
    port=os.environ["POSTGRES_PORT"],
    database=os.environ["POSTGRES_DB"],
)

engine = create_engine(url)
engine = engine.execution_options(isolation_level="AUTOCOMMIT")

Base = declarative_base()
Base.metadata.create_all(bind=engine)
meta = MetaData()

metadata = MetaData()
table = Table(
    os.environ["POSTGRES_TABLE"],
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String),
    Column("surname", String),
    Column("birth_year", Integer),
    Column("birth_place", String),
    Column("terrorist_organization", String),
    Column("category", String),
    Column("isactive", Boolean),
    Column("photos", JSONB),
)

connection = engine.connect()
# Try to create the table, but ignore if it already exists
if not engine.dialect.has_table(connection, os.environ["POSTGRES_TABLE"]):
    # Create the table
    table.create(bind=engine)
connection.close()


def get_db_session():
    Session = sessionmaker(bind=engine)
    session = Session()

    return session


def get_table():
    global table
    return table
