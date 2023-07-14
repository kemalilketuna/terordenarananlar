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
    username="postgres",
    password="postgres",
    host="db",
    port="5432",
    database="postgres",
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
    "wanted_list",
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
if not engine.dialect.has_table(connection, "wanted_list"):
    table.create(bind=engine)

connection.close()

stm = table.select()
result = session.execute(stm)
print(result.fetchone())
