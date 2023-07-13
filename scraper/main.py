from time import sleep
import requests
import logging
import os
import json

# wait for the database to start
# sleep(10) # remove this later

from database import get_info_from_db, _insert_to_db
from minio_utils import send_photo, _minio_name_genator, _minio_url_ceator
from dotenv import load_dotenv  # remove this later

load_dotenv()

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


def photo_url_creator(photo_url):
    base_url = "https://www.terorarananlar.pol.tr"
    return base_url + photo_url


def upload_photo_to_minio(name, surname, photo_url):
    minio_name = _minio_name_genator(name, surname, photo_url)
    url = photo_url_creator(photo_url)
    response = requests.get(url)
    send_photo(response, minio_name)


def insert_to_db(person, isactive):
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
                _minio_url_ceator(adapter["name"], adapter["surname"], photo_url)
            )
            upload_photo_to_minio(adapter["name"], adapter["surname"], photo_url)
        adapter["photos"] = json.dumps(photos_db, ensure_ascii=False)

    _insert_to_db(adapter)


def update_person_db(person):
    pass


def fetch():
    wanted_list = get_wanted_terrorist_info()
    neutralized_list = get_neutralized_terrorist_info()

    for category in neutralized_list.values():
        for neutralized_person in category:
            person_db = get_info_from_db(
                name=neutralized_person["Adi"],
                surname=neutralized_person["Soyadi"],
                birth_year=neutralized_person["DogumTarihi"],
                birth_place=neutralized_person["DogumYeri"],
            )
            if not person_db:
                insert_to_db(neutralized_person, False)
            else:
                update_person_db(neutralized_person)

    for category in wanted_list.values():
        for wanted_person in category:
            person_db = get_info_from_db(
                name=wanted_person["Adi"],
                surname=wanted_person["Soyadi"],
                birth_year=wanted_person["DogumTarihi"],
                birth_place=wanted_person["DogumYeri"],
            )
            if not person_db:
                insert_to_db(wanted_person, True)
            else:
                update_person_db(wanted_person)


if __name__ == "__main__":
    while True:
        logging.info("Updating information")
        fetch()
        logging.info("Service sleeping 1 day")
        sleep(24 * 60 * 60)
