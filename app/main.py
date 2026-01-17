from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.database import init_db
from fastapi_pagination import add_pagination

# Importe suas rotas aqui
from app.routes import setor_routes
from app.routes import funcionario_routes
from app.routes import escala_routes
from app.routes import dashboard_routes

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

app = FastAPI(
    title="API Trabalho 3 - MongoDB",
    lifespan=lifespan
)

# Registre as rotas aqui
add_pagination(app)
app.include_router(setor_routes.router)
app.include_router(funcionario_routes.router)
app.include_router(escala_routes.router)
app.include_router(dashboard_routes.router)



@app.get("/")
def health_check():
    return {"Tudo ok!"}