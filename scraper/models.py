import os
from sqlalchemy import (
    Column,
    DateTime,
    Integer,
    String,
    ForeignKey,
    Boolean,
    UniqueConstraint,
    create_engine,
    func,
)
from sqlalchemy.orm import Relationship, declarative_base, sessionmaker, scoped_session
from sqlalchemy.engine import URL

POSTGRES_USER = os.environ["POSTGRES_USER"]
POSTGRES_PASSWORD = os.environ["POSTGRES_PASSWORD"]
POSTGRES_HOST = os.environ["POSTGRES_HOST"]
POSTGRES_PORT = os.environ["POSTGRES_PORT"]
POSTGRES_DB = os.environ["POSTGRES_DB"]

url = URL.create(
    "postgresql+psycopg",
    username=POSTGRES_USER,
    password=POSTGRES_PASSWORD,
    host=POSTGRES_HOST,
    port=POSTGRES_PORT,
    database=POSTGRES_DB,
)

engine = create_engine(url)
engine = engine.execution_options(isolation_level="AUTOCOMMIT")
session = scoped_session(sessionmaker(bind=engine))


Base = declarative_base()


class T_o(Base):
    __tablename__ = "t_o"
    t_o_id = Column(Integer, primary_key=True, autoincrement=True)
    t_o_name = Column(String(45), nullable=False, index=True, unique=True)

    def __str__(self):
        return f"{self.__class__.__name__}, t_organization: {self.t_o_name}"


class Category(Base):
    __tablename__ = "categories"
    category_id = Column(Integer, primary_key=True, autoincrement=True)
    category_name = Column(String(10), nullable=False, index=True, unique=True)

    def __str__(self):
        return f"{self.__class__.__name__}, category: {self.category_name}"


class Record(Base):
    __tablename__ = "records"
    record_id = Column(Integer, primary_key=True, autoincrement=True)
    id = Column(
        Integer,
        ForeignKey("persons.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    t_o_id = Column(Integer, ForeignKey("t_o.t_o_id"), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.category_id"), nullable=False)
    is_active = Column(Boolean, nullable=False)
    record_time = Column(
        DateTime(timezone=True), server_default=func.timezone("utc+4", func.now())
    )

    def __str__(self):
        return f"{self.__class__.__name__}, record_id: {self.record_id}, person_id: {self.id},is_active: {self.is_active}"


class Picture(Base):
    __tablename__ = "pictures"
    picture_id = Column(Integer, primary_key=True, autoincrement=True)
    id = Column(
        Integer,
        ForeignKey("persons.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    picture_url = Column(String(120), nullable=False)
    record_time = Column(DateTime(timezone=True), server_default=func.now())

    def __str__(self):
        return f"{self.__class__.__name__}, picture_id: {self.picture_id}, person_id: {self.id}, picture: {self.picture}"


class Person(Base):
    __tablename__ = "persons"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(80), nullable=False, index=True)
    surname = Column(String(80), nullable=False, index=True)
    birth_year = Column(Integer, index=True)
    birth_place = Column(String(80), index=True)

    # records = Relationship("Record", backref="person")
    # pictures = Relationship("Picture", backref="person")

    UniqueConstraint(name, surname, birth_year, birth_place, name="unique_person")

    def __str__(self):
        return f"{self.__class__.__name__}, name: {self.name} {self.surname}"


Base.metadata.create_all(engine)
