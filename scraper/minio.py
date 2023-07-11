import os
from minio import Minio
import io

from dotenv import load_dotenv  # remove this later

load_dotenv()

USER_NAME = os.environ("MINIO_USER_NAME")
PASSWORD = os.environ("MINIO_PASSWORD")
BUCKET_NAME = os.environ("BUCKET_NAME")

client = Minio(
    endpoint="localhost:9000", access_key=USER_NAME, secret_key=PASSWORD, secure=False
)

found = client.bucket_exists(BUCKET_NAME)
if not found:
    client.make_bucket(BUCKET_NAME)


def send_photo(picture):
    value_as_bytes = picture.content

    value_as_a_stream = io.BytesIO(value_as_bytes)

    response = client.put_object(
        "files", "my_key.jpeg", value_as_a_stream, length=len(value_as_bytes)
    )

    return response
