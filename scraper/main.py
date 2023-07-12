from time import sleep
import requests
import logging

# wait for the database to start
# sleep(10) # remove this later

from database import get_db_session, get_table
from minio_utils import send_photo

logging.basicConfig(
    filename="scraper.log",
    level=logging.DEBUG,
    format="%(asctime)s : %(levelname)s : %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logging.info("Service started.")


def _get_wanted_list():
    url = "https://www.terorarananlar.pol.tr/ISAYWebPart/TArananlar/GetTerorleArananlarList"
    while True:
        response = requests.post(url)
        if response.status_code == 200:
            break
        logging.error("Request to website is failed.")
        sleep(60 * 60)
    data = response.json()
    for value in data.values():
        for person in value:
            


def _get_neutralized_list():
    url = "https://www.terorarananlar.pol.tr/ISAYWebPart/TArananlar/GetEtkisizList"
    while True:
        response = requests.post(url)
        if response.status_code == 200:
            return response.json()
        logging.error("Request to website is failed.")
        sleep(60 * 60)


def request_wanted_data():
    wanted_list = _get_wanted_list()
    neutralized_list = _get_neutralized_list()

    all_terorists = []
    for value in wanted_list.values():
        all_terorists += value

    for value in neutralized_list.values():
        all_terorists += value

    return all_terorists


def _insert_information(session, table, **data):
    new_row = table.insert().values(data)
    session.execute(new_row)

def get_person_info(session, table, **data):
    stm = table.select().where(
        table.c.name == data["name"]
        and table.c.surname == data["surname"]
        and table.c.birth_year == data["birth_year"]
        and table.c.birth_place == data["birth_place"]
    )
    result = session.execute(stm)
    if result.rowcount == 0:
        return None
    else:
        return result.fetchone()


def _update_active_status(session, table, **data):
    past = get_person_info(session, table, **data)
    if past["isactive"] != data["isactive"]:
        stm = table.update().where(
            table.c.id == past["id"])
        stm = stm.values(isactive=data["isactive"])
        session.execute(stm)
        if data["isactive"]:
            logging.info(f"{data['name']} {data['surname']} is active again.")
        else:
            logging.info(f"{data['name']} {data['surname']} is neutralized.")

"""
def _update_photo(session, table, **data):
    past = get_person_info(session, table, **data)
    if past["photos"]["profile"] != data["photos"]["profile"]:
        stm = table.update().where(
            table.c.id == past["id"])
        stm = stm.values(photos=data["photos"])
        session.execute(stm)
        logging.info(f"{data['name']} {data['surname']}'s photo is updated.")
"""

def genarate_photo_url(person, photo_url):
    return f"https://www.terorarananlar.pol.tr{photo_url}"

def genarate_minio_url(person, photo_url):
    return f""

def _adapter(person, isactive):
    data = {
        "name": person["Ad"],
        "surname": person["Soyad"],
        "birth_year": person["DogumYili"],
        "birth_place": person["DogumYeri"],
        "terrorist_organization": person["TerorOrgutu"],
        "category": person["dsf"],
        "isactive": isactive,
    }

def fetch():
    session = fetch()
    table = get_table()

    data = request_wanted_data()
    for person in data:
        if not get_person_info
    session.close()


if __name__ == "__main__":
    while True:
        logging.info("Updating information")
        fetch()
        logging.info("Service sleeping 1 day")
        sleep(24 * 60 * 60)
