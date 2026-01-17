from fastapi import APIRouter, HTTPException, status
from fastapi_pagination import Page
from fastapi_pagination.ext.beanie import paginate
from beanie import PydanticObjectId
from beanie.operators import In  # <--- 1. ADICIONAMOS ESSE IMPORT IMPORTANTE

from app.models.escala import Escala
from app.models.funcionario import Funcionario
from app.models.setor import Setor

router = APIRouter(prefix="/escalas", tags=["Escalas"])

# 1. CREATE
@router.post("/", status_code=201, response_model=Escala)
async def criar_escala(escala: Escala):
    return await escala.create()

# 2. READ ALL (CORRIGIDO)
@router.get("/", response_model=Page[Escala])
async def listar_escalas():
    async def carregar_dados_escala(itens: list[Escala]):
        for escala in itens:
            # Carregar Setor
            if escala.setor and escala.setor.ref.id:
                escala.setor = await Setor.get(escala.setor.ref.id)
            
            # Carregar Equipe
            if escala.equipe:
                # Pega os IDs da lista de links (garantindo que não sejam nulos)
                ids = [link.ref.id for link in escala.equipe if link.ref.id]
                
                if ids:
                    # <--- 2. AQUI ESTAVA O ERRO. MUDAMOS PARA USAR "In()"
                    # Antes: Funcionario.find(Funcionario.id.in_(ids)) -> ERRADO
                    # Agora: Funcionario.find(In(Funcionario.id, ids)) -> CERTO
                    funcionarios = await Funcionario.find(In(Funcionario.id, ids)).to_list()
                    escala.equipe = funcionarios
        return itens

    return await paginate(Escala.find_all(), transformer=carregar_dados_escala)

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
            # <--- CORRIGIMOS AQUI TAMBÉM PARA GARANTIR
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