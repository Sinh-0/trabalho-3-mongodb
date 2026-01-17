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
    # Contagens simples
    total_func = await Funcionario.count()
    total_escalas = await Escala.count()
    total_setores = await Setor.count()

    # Agregação: Média Salarial
    pipeline_media = [
        {"$group": {"_id": None, "media_salarial": {"$avg": "$salario"}}}
    ]
    resultado_media = await Funcionario.aggregate(pipeline_media).to_list()
    media = resultado_media[0]["media_salarial"] if resultado_media else 0

    return {
        "total_funcionarios": total_func,
        "total_escalas": total_escalas,
        "total_setores": total_setores,
        "media_salarial_empresa": round(media, 2)
    }