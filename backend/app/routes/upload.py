from fastapi import APIRouter, UploadFile, File
from app.minio_client import client, BUCKET
import uuid
import os

router = APIRouter()

@router.post("/imagen")
async def subir_imagen(file: UploadFile = File(...)):
    extension = os.path.splitext(file.filename)[1]
    nombre = f"{uuid.uuid4()}{extension}"

    client.put_object(
        BUCKET,
        nombre,
        file.file,
        length=-1,
        part_size=10*1024*1024,
        content_type=file.content_type
    )

    url = f"http://localhost:9000/{BUCKET}/{nombre}"
    return {"url": url}
