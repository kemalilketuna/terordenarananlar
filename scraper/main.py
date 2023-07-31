from time import sleep
import requests
import logging

# wait for the database to start
sleep(10)
from database_utils import *
from minio_utils import send_photo, _minio_name_genator, _minio_url_ceator


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


def website_photo_url(photo_url):
    base_url = "https://www.terorarananlar.pol.tr"
    return base_url + photo_url


def upload_photo_to_minio(name, surname, photo_url):
    minio_name = _minio_name_genator(name, surname, photo_url)
    url = website_photo_url(photo_url)
    response = requests.get(url)
    send_photo(response, minio_name)


def check_record_in_db(criminal, is_active):
    name = criminal["Adi"]
    surname = criminal["Soyadi"]
    birth_year = criminal["DogumTarihi"]
    birth_place = criminal["DogumYeri"]
    t_o_name = criminal["TOrgutAdi"]
    category_name = criminal["TKategoriAdi"]

    person_id = get_person_id(name, surname, birth_year, birth_place)
    category_id = get_category_id(category_name)
    t_o_id = get_t_o_id(t_o_name)
    last_record = get_last_record(person_id)

    if last_record == None or (
        last_record.id != person_id
        or last_record.category_id != category_id
        or last_record.t_o_id != t_o_id
        or last_record.is_active != is_active
    ):
        insert_record_to_db(person_id, t_o_id, category_id, is_active)


def check_photo_in_minio(criminal):
    name = criminal["Adi"]
    surname = criminal["Soyadi"]
    birth_year = criminal["DogumTarihi"]
    birth_place = criminal["DogumYeri"]

    person_id = get_person_id(name, surname, birth_year, birth_place)
    all_pictures = get_all_pictures(person_id)
    all_pictures_url = [picture.picture_url for picture in all_pictures]

    if criminal["GorselURL"]:
        for photo_url in criminal["GorselURL"]:
            minio_url = _minio_url_ceator(name, surname, photo_url)
            if minio_url not in all_pictures_url:
                upload_photo_to_minio(name, surname, photo_url)
                insert_picture_to_db(person_id, minio_url)


def fetch():
    neturalized_data = get_neutralized_terrorist_info()
    neturalized_list = sum(neturalized_data.values(), [])

    for person in neturalized_list:
        check_record_in_db(person, False)
        check_photo_in_minio(person)

    wanteds_data = get_wanted_terrorist_info()
    wanteds_list = sum(wanteds_data.values(), [])

    for person in wanteds_list:
        check_record_in_db(person, True)
        check_photo_in_minio(person)


if __name__ == "__main__":
    while True:
        logging.info("Updating information")
        fetch()
        logging.info("Service sleeping 1 day")
        sleep(24 * 60 * 60)
