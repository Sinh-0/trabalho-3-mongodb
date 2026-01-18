from fastapi import APIRouter, HTTPException, status, Query
from fastapi_pagination import Page
from fastapi_pagination.ext.beanie import paginate
from beanie import PydanticObjectId
from beanie.operators import RegEx
from pydantic import BaseModel

# Importamos os modelos
from app.models.funcionario import Funcionario
from app.models.setor import Setor

router = APIRouter(prefix="/funcionarios", tags=["Funcionários"])

class FuncionarioUpdate(BaseModel):
    nome: str | None = None
    cpf: str | None = None
    email: str | None = None
    salario: float | None = None
    data_nascimento: str | None = None

# 1. CREATE
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Funcionario)
async def criar_funcionario(funcionario: Funcionario):
    # Regra: Verificar se o setor existe
    if funcionario.setor and funcionario.setor.ref.id:
        setor_existe = await Setor.get(funcionario.setor.ref.id)
        if not setor_existe:
            raise HTTPException(status_code=400, detail="Setor informado não existe.")
            
    novo_func = await funcionario.create()
    return novo_func

# 2. READ ALL (Com filtros de Texto e Ordenação)
@router.get("/", response_model=Page[Funcionario])
async def listar_funcionarios(
    nome: str | None = Query(None, description="Filtrar por nome (busca parcial)"),
    cpf: str | None = Query(None, description="Filtrar por CPF exato"),
    setor_id: str | None = Query(None, description="Filtrar por ID do Setor (Relacionamento)"), # <--- NOVO!
    ordenar_por: str = Query("nome", enum=["nome", "salario"], description="Campo para ordenação"),
    direcao: str = Query("asc", enum=["asc", "desc"], description="Direção da ordenação")
):
    query_busca = Funcionario.find_all()

    # Filtros
    if setor_id:
        # Busca funcionários onde o LINK do setor tem esse ID
        query_busca = Funcionario.find(Funcionario.setor.ref.id == PydanticObjectId(setor_id))

    # c) Busca por texto parcial
    if nome:
        query_busca = query_busca.find(RegEx(Funcionario.nome, nome, "i"))
    
    if cpf:
        query_busca = query_busca.find(Funcionario.cpf == cpf)

    # Ordenação
    if direcao == "asc":
        query_busca = query_busca.sort(ordenar_por)
    else:
        query_busca = query_busca.sort(f"-{ordenar_por}")

    # Transformer
    async def carregar_links(itens: list[Funcionario]):
        for func in itens:
            if func.setor and func.setor.ref.id:
                func.setor = await Setor.get(func.setor.ref.id)
        return itens

    return await paginate(query_busca, transformer=carregar_links)

# 3. READ ONE
@router.get("/{id}", response_model=Funcionario)
async def obter_funcionario(id: PydanticObjectId):
    funcionario = await Funcionario.get(id)
    if not funcionario:
        raise HTTPException(status_code=404, detail="Funcionário não encontrado")

    if funcionario.setor and funcionario.setor.ref.id:
        funcionario.setor = await Setor.get(funcionario.setor.ref.id)

    return funcionario

# 4. PATCH 
@router.patch("/{id}", response_model=Funcionario)
async def atualizar_parcial(id: PydanticObjectId, dados: FuncionarioUpdate):
    # Pega apenas os campos que não são None
    req = {k: v for k, v in dados.dict().items() if v is not None}
    
    if not req:
        raise HTTPException(status_code=400, detail="Nenhum dado enviado para atualização")

    update_query = {"$set": req}
    
    funcionario = await Funcionario.get(id)
    if not funcionario:
        raise HTTPException(status_code=404, detail="Funcionário não encontrado")
    
    await funcionario.update(update_query)
    
    # Recarrega o Setor
    if funcionario.setor and funcionario.setor.ref.id:
         funcionario.setor = await Setor.get(funcionario.setor.ref.id)
         
    return funcionario

# 5. PUT 
@router.put("/{id}", response_model=Funcionario)
async def atualizar_total(id: PydanticObjectId, dados_atualizados: Funcionario):
    func_banco = await Funcionario.get(id)
    if not func_banco:
        raise HTTPException(status_code=404, detail="Funcionário não encontrado")
    
    dados_atualizados.id = id
    await dados_atualizados.replace()
    
    if dados_atualizados.setor and dados_atualizados.setor.ref.id:
        dados_atualizados.setor = await Setor.get(dados_atualizados.setor.ref.id)
        
    return dados_atualizados

# 6. DELETE
@router.delete("/{id}", status_code=204)
async def deletar_funcionario(id: PydanticObjectId):
    func = await Funcionario.get(id)
    if not func:
        raise HTTPException(status_code=404, detail="Não encontrado")
    await func.delete()
    return None