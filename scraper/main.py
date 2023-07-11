from time import sleep
import requests
import logging

logging.basicConfig(
    filename="main.log",
    level=logging.DEBUG,
    format="%(asctime)s : %(levelname)s : %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
# wait for the database to start
sleep(10)
from database import get_db_session, get_table

logging.info("Service started.")

session = get_db_session()
table = get_table()

# turn this function
data = {
    "name": "John",
    "surname": "Doe",
    "birth_year": 1990,
    "birth_place": "City",
    "terrorist_organization": "None",
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
