from time import sleep
import requests
import logging
import os
import io

# wait for the database to start
# sleep(10) # remove this later

from database import get_db_session, get_table
from minio_utils import send_photo
from dotenv import load_dotenv  # remove this later

load_dotenv()

BUCKET_NAME = os.environ["BUCKET_NAME"]

logging.basicConfig(
    filename="scraper.log",
    level=logging.DEBUG,
    format="%(asctime)s : %(levelname)s : %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logging.info("Service started.")


def _get_neutralized_terrorist_info():
    pass


def _get_wanted_terrorist_info():
    pass


def new_record():
    pass


def photo_url_creator():
    pass


def minio_name_genator():
    pass


def fetch():
    pass


if __name__ == "__main__":
    while True:
        logging.info("Updating information")
        fetch()
        logging.info("Service sleeping 1 day")
        sleep(24 * 60 * 60)
