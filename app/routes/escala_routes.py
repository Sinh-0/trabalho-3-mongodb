from fastapi import APIRouter, HTTPException, status, Query
from fastapi_pagination import Page
from fastapi_pagination.ext.beanie import paginate
from beanie import PydanticObjectId
from beanie.operators import In, GTE, LTE
from datetime import datetime

from app.models.escala import Escala
from app.models.funcionario import Funcionario
from app.models.setor import Setor

router = APIRouter(prefix="/escalas", tags=["Escalas"])

# 1. CREATE
@router.post("/", status_code=201, response_model=Escala)
async def criar_escala(escala: Escala):
    return await escala.create()

# 2. READ ALL (COM FILTRO DE DATA - Item 'd' dos requisitos)
@router.get("/", response_model=Page[Escala])
async def listar_escalas(
    ano: int | None = Query(None, description="Filtrar escalas de um ano específico"),
    data_inicio: datetime | None = Query(None, description="Filtrar a partir desta data (ISO 8601)"),
):
    query_busca = Escala.find_all()

    # d) Filtros por data/ano
    if ano:
        # Busca escalas que começam entre 01/01 e 31/12 do ano
        dt_start = datetime(ano, 1, 1)
        dt_end = datetime(ano, 12, 31, 23, 59, 59)
        query_busca = Escala.find(GTE(Escala.inicio, dt_start), LTE(Escala.inicio, dt_end))
    
    if data_inicio:
         query_busca = query_busca.find(GTE(Escala.inicio, data_inicio))

    # Transformer Manual
    async def carregar_dados_escala(itens: list[Escala]):
        for escala in itens:
            if escala.setor and escala.setor.ref.id:
                escala.setor = await Setor.get(escala.setor.ref.id)
            
            if escala.equipe:
                ids = [link.ref.id for link in escala.equipe if link.ref.id]
                if ids:
                    funcionarios = await Funcionario.find(In(Funcionario.id, ids)).to_list()
                    escala.equipe = funcionarios
        return itens

    return await paginate(query_busca, transformer=carregar_dados_escala)

# 3. READ ONE
@router.get("/{id}", response_model=Escala)
async def obter_escala(id: PydanticObjectId):
    escala = await Escala.get(id)
    if not escala:
        raise HTTPException(status_code=404, detail="Escala não encontrada")
    
    if escala.setor and escala.setor.ref.id:
        escala.setor = await Setor.get(escala.setor.ref.id)
    
    if escala.equipe:
        ids = [link.ref.id for link in escala.equipe if link.ref.id]
        if ids:
            escala.equipe = await Funcionario.find(In(Funcionario.id, ids)).to_list()

    return escala

# 4. UPDATE
@router.put("/{id}", response_model=Escala)
async def atualizar_escala(id: PydanticObjectId, dados_atualizados: Escala):
    escala_banco = await Escala.get(id)
    if not escala_banco:
        raise HTTPException(status_code=404, detail="Escala não encontrada")
    
    dados_atualizados.id = id
    await dados_atualizados.replace()
    return dados_atualizados

# 5. DELETE
@router.delete("/{id}", status_code=204)
async def deletar_escala(id: PydanticObjectId):
    escala = await Escala.get(id)
    if not escala:
        raise HTTPException(status_code=404, detail="Escala não encontrada")
    await escala.delete()
    return None