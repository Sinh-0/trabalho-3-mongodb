from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie

from app.config import settings
from app.models.setor import Setor 
from app.models.funcionario import Funcionario

async def init_db():
    client = AsyncIOMotorClient(settings.MONGODB_URL)
    database = client[settings.DATABASE_NAME]
    
    await init_beanie(
        database=database, 
        document_models=[
            Setor,
            Funcionario
        ]
    )
    
    print("✅ Conexão com MongoDB e Beanie iniciada com sucesso!")

