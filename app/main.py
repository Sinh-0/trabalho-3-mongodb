from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.database import init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield
   

app = FastAPI(
    title="API Trabalho 3 - MongoDB",
    lifespan=lifespan
)

@app.get("/")
def health_check():
    return {"status": "ok", "banco": "conectado"}

