from fastapi import APIRouter, HTTPException, status
from fastapi_pagination import Page
from fastapi_pagination.ext.beanie import paginate
from beanie import PydanticObjectId

from app.models.funcionario import Funcionario
from app.models.setor import Setor

router = APIRouter(prefix="/funcionarios", tags=["Funcionários"])

# 1. CREATE
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Funcionario)
async def criar_funcionario(funcionario: Funcionario):
    novo_func = await funcionario.create()
    return novo_func

# 2. READ ALL (Com a correção de versão do Motor)
@router.get("/", response_model=Page[Funcionario])
async def listar_funcionarios():
    # Transformer para preencher o Setor manualmente
    async def carregar_links(itens: list[Funcionario]):
        for func in itens:
            if func.setor and func.setor.ref.id:
                # Busca o setor real no banco e substitui o link
                setor_real = await Setor.get(func.setor.ref.id)
                func.setor = setor_real
        return itens

    # Busca simples + Paginação com Transformer
    query = Funcionario.find_all()
    return await paginate(query, transformer=carregar_links)

# 3. READ ONE (Com busca manual)
@router.get("/{id}", response_model=Funcionario)
async def obter_funcionario(id: PydanticObjectId):
    funcionario = await Funcionario.get(id)
    if not funcionario:
        raise HTTPException(status_code=404, detail="Funcionário não encontrado")

    # Preenche o Setor manualmente
    if funcionario.setor and funcionario.setor.ref.id:
        funcionario.setor = await Setor.get(funcionario.setor.ref.id)

    return funcionario

# 4. UPDATE (AQUI ESTÁ O QUE FALTAVA!)
@router.put("/{id}", response_model=Funcionario)
async def atualizar_funcionario(id: PydanticObjectId, dados_atualizados: Funcionario):
    func_banco = await Funcionario.get(id)
    if not func_banco:
        raise HTTPException(status_code=404, detail="Funcionário não encontrado")
    
    # Garante que o ID do objeto é o mesmo da URL
    dados_atualizados.id = id
    
    # Substitui os dados no banco
    await dados_atualizados.replace()
    
    # Para retornar bonito, buscamos o setor novamente
    if dados_atualizados.setor and dados_atualizados.setor.ref.id:
        dados_atualizados.setor = await Setor.get(dados_atualizados.setor.ref.id)
        
    return dados_atualizados

# 5. DELETE
@router.delete("/{id}", status_code=204)
async def deletar_funcionario(id: PydanticObjectId):
    func = await Funcionario.get(id)
    if not func:
        raise HTTPException(status_code=404, detail="Não encontrado")
    await func.delete()
    return None