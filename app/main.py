from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.database import init_db

# Importe suas rotas aqui
from app.routes import setor_routes

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

app = FastAPI(
    title="API Trabalho 3 - MongoDB",
    lifespan=lifespan
)

# Registre as rotas aqui
app.include_router(setor_routes.router)

@app.get("/")
def health_check():
    return {"status": "ok", "banco": "conectado"}