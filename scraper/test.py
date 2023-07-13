from database import get_db_session, get_table
import requests
from time import sleep
from sqlalchemy import and_

table = get_table()
session = get_db_session()

# session.query(table).filter(table.c.id == 2).update({"category": "kırmızı"})

# stm = session.query(table).filter(table.c.id == 2).first()
# print(stm.category)


def get_info_from_db(session, table, **person_info):
    stm = (
        session.query(table)
        .filter(
            and_(
                table.c.name == person_info["name"],
                table.c.surname == person_info["surname"],
                table.c.birth_year == person_info["birth_year"],
                table.c.birth_place == person_info["birth_place"],
            )
        )
        .first()
    )
    return stm


def get_wanted_terrorist_info():
    response = requests.post(
        "https://www.terorarananlar.pol.tr/ISAYWebPart/TArananlar/GetTerorleArananlarList"
    )
    return response.json()


data = get_wanted_terrorist_info()

for category in data.values():
    for person in category:
        name = person["Adi"]
        surname = person["Soyadi"]
        year = person["DogumTarihi"]
        place = person["DogumYeri"]
        person_db = get_info_from_db(
            session,
            table,
            name=name,
            surname=surname,
            birth_year=year,
            birth_place=place,
        )
        if person_db.category != person["TKategoriAdi"]:
            print(person)
            print(person_db)
            input()
        print(person_db.id, end=" ")


def get_neutralized_terrorist_info():
    response = requests.post(
        "https://www.terorarananlar.pol.tr/ISAYWebPart/TArananlar/GetEtkisizList"
    )
    return response.json()


data = get_neutralized_terrorist_info()


for category in data.values():
    for person in category:
        name = person["Adi"]
        surname = person["Soyadi"]
        year = person["DogumTarihi"]
        place = person["DogumYeri"]
        person_db = get_info_from_db(
            session,
            table,
            name=name,
            surname=surname,
            birth_year=year,
            birth_place=place,
        )
        if person_db.category != person["TKategoriAdi"]:
            print(person)
            print(person_db)
            input()
        print(person_db.id, end=" ")
