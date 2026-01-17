from fastapi import APIRouter, HTTPException, status
from fastapi_pagination import Page
from fastapi_pagination.ext.beanie import paginate
from typing import List
from beanie import PydanticObjectId

from app.models.setor import Setor
from pydantic import BaseModel

router = APIRouter(prefix="/setores", tags=["Setores"])

class SetorUpdate(BaseModel):
    nome: str | None = None
    responsavel: str | None = None

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Setor)
async def criar_setor(setor: Setor):
    novo_setor = await setor.create()
    return novo_setor

@router.get("/", response_model=Page[Setor])
async def listar_setores():
    return await paginate(Setor.find_all())

@router.get("/{id}", response_model=Setor)
async def obter_setor(id: PydanticObjectId):
    setor = await Setor.get(id)
    if not setor:
        raise HTTPException(status_code=404, detail="Setor não encontrado")
    return setor

@router.put("/{id}", response_model=Setor)
async def atualizar_setor(id: PydanticObjectId, dados_atualizacao: SetorUpdate):
    setor_banco = await Setor.get(id)
    if not setor_banco:
        raise HTTPException(status_code=404, detail="Setor não encontrado")
    
    atualizacao = dados_atualizacao.model_dump(exclude_unset=True)
    
    await setor_banco.update({"$set": atualizacao})
    
    
    return setor_banco

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def deletar_setor(id: PydanticObjectId):
    setor = await Setor.get(id)
    if not setor:
        raise HTTPException(status_code=404, detail="Setor não encontrado")
    
    await setor.delete()
    return None