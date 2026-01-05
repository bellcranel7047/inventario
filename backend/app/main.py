from fastapi import FastAPI
from app.routes.upload import router as upload_router

app = FastAPI(title="Inventario con MinIO")

@app.get("/")
def root():
    return {"status": "Inventario funcionando"}

app.include_router(upload_router, prefix="/productos", tags=["Productos"])
