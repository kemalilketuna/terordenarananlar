from time import sleep
import requests
import logging
import os
import json

# wait for the database to start
# sleep(10) # remove this later

from database import get_db_session, get_table
from minio_utils import send_photo
from dotenv import load_dotenv  # remove this later

load_dotenv()

BUCKET_NAME = os.environ["BUCKET_NAME"]

logging.basicConfig(
    filename="scraper.log",
    level=logging.INFO,
    format="%(asctime)s : %(levelname)s : %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logging.info("Service started.")


def get_neutralized_terrorist_info():
    response = requests.post(
        "https://www.terorarananlar.pol.tr/ISAYWebPart/TArananlar/GetEtkisizList"
    )
    return response.json()


def get_wanted_terrorist_info():
    response = requests.post(
        "https://www.terorarananlar.pol.tr/ISAYWebPart/TArananlar/GetTerorleArananlarList"
    )
    return response.json()


# change it
def _insert_to_db(session, table, person_db):
    new_row = table.insert().values(person_db)
    session.execute(new_row)


def get_info_from_db(session, table, person_db):
    stm = table.select().where(
        table.c.name == person_db["name"]
        and table.c.surname == person_db["surname"]
        and table.c.birth_year == person_db["birth_year"]
        and table.c.birth_place == person_db["birth_place"]
    )
    result = session.execute(stm)
    if result.rowcount == 0:
        return None
    else:
        return result.fetchone()


def photo_url_creator(photo_url):
    base_url = "https://www.terorarananlar.pol.tr"
    return base_url + photo_url


def _minio_name_genator(name, surname, photo_url):
    end_part = photo_url.split("/")[-1]
    return f"{name}_{surname}_{end_part}"


def minio_url_ceator(name, surname, photo_url):
    base_url = "http://localhost:9000"
    return f"{base_url}/{BUCKET_NAME}/{_minio_name_genator(name, surname, photo_url)}"


def upload_photo_to_minio(name, surname, photo_url):
    minio_name = _minio_name_genator(name, surname, photo_url)
    url = photo_url_creator(photo_url)
    response = requests.get(url)
    send_photo(response, minio_name)


def _adapter(wanted_person, isactive):
    adapter = {}
    adapter["name"] = wanted_person["Adi"]
    adapter["surname"] = wanted_person["Soyadi"]
    try:
        adapter["birth_year"] = int(wanted_person["DogumTarihi"])
    except:
        adapter["birth_year"] = None
    adapter["birth_place"] = wanted_person["DogumYeri"]
    adapter["terrorist_organization"] = wanted_person["TOrgutAdi"]
    adapter["category"] = wanted_person["TKategoriAdi"]
    adapter["isactive"] = isactive

    photos_db = []
    if not wanted_person["GorselURL"]:
        adapter["photos"] = json.dumps(photos_db)
    else:
        for photo_url in wanted_person["GorselURL"]:
            photos_db.append(
                minio_url_ceator(adapter["name"], adapter["surname"], photo_url)
            )
            upload_photo_to_minio(adapter["name"], adapter["surname"], photo_url)
        adapter["photos"] = json.dumps(photos_db, ensure_ascii=False)
    return adapter


def fetch():
    table = get_table()
    session = get_db_session()

    wanted_list = get_wanted_terrorist_info()
    neutralized_list = get_neutralized_terrorist_info()

    for category in wanted_list.values():
        for wanted_person in category:
            person_db = _adapter(wanted_person, True)
            _insert_to_db(session, table, person_db)

    for category in neutralized_list.values():
        for neutralized_person in category:
            person_db = _adapter(neutralized_person, False)
            _insert_to_db(session, table, person_db)


if __name__ == "__main__":
    while True:
        logging.info("Updating information")
        fetch()
        logging.info("Service sleeping 1 day")
        sleep(24 * 60 * 60)
