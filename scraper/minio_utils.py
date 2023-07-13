import os
from minio import Minio
import io
from dotenv import load_dotenv  # remove this later

load_dotenv()


USER_NAME = os.environ["MINIO_USER_NAME"]
PASSWORD = os.environ["MINIO_PASSWORD"]
BUCKET_NAME = os.environ["BUCKET_NAME"]

client = Minio(
    endpoint="localhost:9000", access_key=USER_NAME, secret_key=PASSWORD, secure=False
)

found = client.bucket_exists(BUCKET_NAME)
if not found:
    # set public read access
    with open("public_policy.json", "r") as f:
        policy = f.read()

        policy = policy.replace("BUCKET_NAME", BUCKET_NAME)
        client.make_bucket(BUCKET_NAME)
        client.set_bucket_policy(BUCKET_NAME, policy)


def send_photo(picture, file_name):
    value_as_bytes = picture.content
    value_as_a_stream = io.BytesIO(value_as_bytes)
    response = client.put_object(
        BUCKET_NAME, file_name, value_as_a_stream, length=len(value_as_bytes)
    )
    return response


def _minio_name_genator(name, surname, photo_url):
    end_part = photo_url.split("/")[-1]
    return f"{name}_{surname}_{end_part}"


def _minio_url_ceator(name, surname, photo_url):
    base_url = "http://localhost:9000"
    return f"{base_url}/{BUCKET_NAME}/{_minio_name_genator(name, surname, photo_url)}"
