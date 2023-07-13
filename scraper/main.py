from time import sleep
import requests
import logging
import os
import json

# wait for the database to start
# sleep(10) # remove this later

from database import get_db_session, get_table, get_info_from_db
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


def insert_to_db(session, table, person, isactive):
    adapter = {}
    adapter["name"] = person["Adi"]
    adapter["surname"] = person["Soyadi"]
    try:
        adapter["birth_year"] = int(person["DogumTarihi"])
    except:
        adapter["birth_year"] = None
    adapter["birth_place"] = person["DogumYeri"]
    adapter["terrorist_organization"] = person["TOrgutAdi"]
    adapter["category"] = person["TKategoriAdi"]
    adapter["isactive"] = isactive

    photos_db = []
    if not person["GorselURL"]:
        adapter["photos"] = json.dumps(photos_db)
    else:
        for photo_url in person["GorselURL"]:
            photos_db.append(
                minio_url_ceator(adapter["name"], adapter["surname"], photo_url)
            )
            upload_photo_to_minio(adapter["name"], adapter["surname"], photo_url)
        adapter["photos"] = json.dumps(photos_db, ensure_ascii=False)

    _insert_to_db(session, table, adapter)


def update_person_db(session, table, person, person_db, isactive):
    pass


def fetch():
    table = get_table()
    session = get_db_session()

    wanted_list = get_wanted_terrorist_info()
    neutralized_list = get_neutralized_terrorist_info()

    for category in neutralized_list.values():
        for neutralized_person in category:
            insert_to_db(session, table, neutralized_person, False)

    for category in wanted_list.values():
        for wanted_person in category:
            insert_to_db(session, table, wanted_person, True)

    session.close()


if __name__ == "__main__":
    while True:
        logging.info("Updating information")
        fetch()
        logging.info("Service sleeping 1 day")
        sleep(24 * 60 * 60)
