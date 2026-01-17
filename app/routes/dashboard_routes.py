from fastapi import APIRouter
from app.models.funcionario import Funcionario
from app.models.escala import Escala
from app.models.setor import Setor

router = APIRouter(prefix="/dashboard", tags=["Dashboard / Estatísticas"])

@router.get("/geral")
async def obter_estatisticas_gerais():
    """
    e) Agregações e contagens utilizando aggregation pipeline
    g) Consultas complexas
    """
    # 1. Contagens simples
    total_func = await Funcionario.count()
    total_escalas = await Escala.count()
    total_setores = await Setor.count()

    # 2. Agregação: Média Salarial
    pipeline_media = [
        {"$group": {"_id": None, "media_salarial": {"$avg": "$salario"}}}
    ]
    
    # --- A CORREÇÃO ESTÁ AQUI EMBAIXO ---
    # Usamos .get_pymongo_collection() em vez de .get_motor_collection()
    motor_collection = Funcionario.get_pymongo_collection()
    
    # O aggregate do Motor retorna um cursor (sem await)
    cursor = motor_collection.aggregate(pipeline_media)
    
    # O to_list é que precisa ser aguardado
    resultado_media = await cursor.to_list(length=None)
    
    media = resultado_media[0]["media_salarial"] if resultado_media else 0

    return {
        "total_funcionarios": total_func,
        "total_escalas": total_escalas,
        "total_setores": total_setores,
        "media_salarial_empresa": round(media, 2)
    }