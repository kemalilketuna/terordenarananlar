import os
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import URL
from sqlalchemy.orm import declarative_base
from sqlalchemy import and_

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

Session = sessionmaker(bind=engine)
session = Session()

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
if not engine.dialect.has_table(connection, os.environ["POSTGRES_TABLE"]):
    table.create(bind=engine)
connection.close()


def get_info_from_db(**person_info):
    global session
    stm = table.select().where(
        and_(
            table.c.name == person_info["name"],
            table.c.surname == person_info["surname"],
            table.c.birth_year == person_info["birth_year"],
            table.c.birth_place == person_info["birth_place"],
        )
    )
    result = session.execute(stm)
    if result.rowcount == 0:
        return None
    else:
        return result.fetchone()


def _update_category(db_id, new_category):
    session.query(table).filter(table.c.id == db_id).update({"category": new_category})


def _update_photos(db_id, photos_json):
    session.query(table).filter(table.c.id == db_id).update({"photos": photos_json})


def _update_isactive(db_id, new_isactive):
    session.query(table).filter(table.c.id == db_id).update({"isactive": new_isactive})


def _insert_to_db(data):
    new_row = table.insert().values(data)
    session.execute(new_row)
