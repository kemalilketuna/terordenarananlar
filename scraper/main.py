from time import sleep
import requests
import logging

# wait for the database to start
sleep(10)
from database import get_db_session, get_table

logging.basicConfig(
    filename="scraper.log",
    level=logging.DEBUG,
    format="%(asctime)s : %(levelname)s : %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logging.info("Service started.")


def request_data():
    url = "https://www.terorarananlar.pol.tr/ISAYWebPart/TArananlar/GetTerorleArananlarList"
    while True:
        response = requests.post(url)
        if response.status_code == 200:
            return response.json()
        logging.error("Request to website is failed.")
        sleep(60 * 60)


def insert_data(session, table, data):
    new_row = table.insert().values(**data)


def update():
    session = get_db_session()
    table = get_table()

    # turn this function
    data = {
        "name": "John",
        "surname": "Doe",
        "birth_year": 1990,
        "birth_place": "City",
        "terrorist_organization": "None",
        "category": "sari",
        "isactive": True,
        "photos": {"profile": "image.jpg"},
    }
    new_row = table.insert().values(**data)
    session.execute(new_row)

    # Commit the changes
    session.commit()
    print("Data inserted successfully!")

    # Close the connection
    session.close()


if __name__ == "__main__":
    while True:
        logging.info("Updating information")
        update()
        logging.info("Service sleeping 1 day")
        sleep(24 * 60 * 60)
