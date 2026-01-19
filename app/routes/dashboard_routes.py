from fastapi import APIRouter
from app.models.funcionario import Funcionario
from app.models.escala import Escala
from app.models.setor import Setor

router = APIRouter(prefix="/dashboard", tags=["Dashboard / Estatísticas"])

@router.get("/geral")
async def obter_estatisticas_gerais():
    """
    e) Agregações e contagens 
    g) Consultas complexas
    """
    
    total_func = await Funcionario.count()
    total_escalas = await Escala.count()
    total_setores = await Setor.count()

    pipeline_media = [
        {"$group": {"_id": None, "media_salarial": {"$avg": "$salario"}}}
    ]
    
    motor_collection = Funcionario.get_pymongo_collection()
    
    cursor = motor_collection.aggregate(pipeline_media)
    
    resultado_media = await cursor.to_list(length=None)
    
    media = resultado_media[0]["media_salarial"] if resultado_media else 0

    return {
        "total_funcionarios": total_func,
        "total_escalas": total_escalas,
        "total_setores": total_setores,
        "media_salarial_empresa": round(media, 2)
    }