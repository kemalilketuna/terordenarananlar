from minio import Minio
import os
from dotenv import load_dotenv  # remove this later

load_dotenv()

access_key = os.environ("MINIO_USER_NAME")
secret_key = os.environ("MINIO_PASSWORD")
password = "minio123"

lient = Minio(
    endpoint="localhost:9000", access_key=access_key, secret_key=password, secure=False
)
