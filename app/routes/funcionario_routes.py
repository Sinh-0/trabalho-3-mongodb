from fastapi import APIRouter, HTTPException, status, Query
from fastapi_pagination import Page
from fastapi_pagination.ext.beanie import paginate
from beanie import PydanticObjectId
from beanie.operators import RegEx

from app.models.funcionario import Funcionario
from app.models.setor import Setor

router = APIRouter(prefix="/funcionarios", tags=["Funcionários"])

# 1. CREATE
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Funcionario)
async def criar_funcionario(funcionario: Funcionario):
    # Regra de negócio: Verificar se o setor existe antes de criar
    if funcionario.setor and funcionario.setor.ref.id:
        setor_existe = await Setor.get(funcionario.setor.ref.id)
        if not setor_existe:
            raise HTTPException(status_code=400, detail="Setor informado não existe.")
            
    novo_func = await funcionario.create()
    return novo_func

# 2. READ ALL (COM FILTROS: Texto, Relacionamento e Ordenação)
@router.get("/", response_model=Page[Funcionario])
async def listar_funcionarios(
    nome: str | None = Query(None, description="Filtrar por nome (busca parcial)"),
    cpf: str | None = Query(None, description="Filtrar por CPF exato"),
    ordenar_por: str = Query("nome", enum=["nome", "salario"], description="Campo para ordenação"),
    direcao: str = Query("asc", enum=["asc", "desc"], description="Direção da ordenação")
):
    # Inicia a query base
    query_busca = Funcionario.find_all()

    # c) Busca por texto parcial e case-insensitive
    if nome:
        query_busca = Funcionario.find(RegEx(Funcionario.nome, nome, "i"))
    
    # Busca exata
    if cpf:
        query_busca = query_busca.find(Funcionario.cpf == cpf)

    # f) Classificações e ordenações
    if direcao == "asc":
        query_busca = query_busca.sort(ordenar_por)
    else:
        query_busca = query_busca.sort(f"-{ordenar_por}")

    # Transformer manual (para carregar o Setor)
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

# 4. UPDATE
@router.put("/{id}", response_model=Funcionario)
async def atualizar_funcionario(id: PydanticObjectId, dados_atualizados: Funcionario):
    func_banco = await Funcionario.get(id)
    if not func_banco:
        raise HTTPException(status_code=404, detail="Funcionário não encontrado")
    
    dados_atualizados.id = id
    await dados_atualizados.replace()
    
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