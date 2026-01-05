from minio import Minio
import os
from dotenv import load_dotenv

load_dotenv()

client = Minio(
    f"{os.getenv('MINIO_ENDPOINT')}:{os.getenv('MINIO_PORT')}",
    access_key=os.getenv("MINIO_ACCESS_KEY"),
    secret_key=os.getenv("MINIO_SECRET_KEY"),
    secure=False
)

BUCKET = os.getenv("MINIO_BUCKET")

if not client.bucket_exists(BUCKET):
    client.make_bucket(BUCKET)
