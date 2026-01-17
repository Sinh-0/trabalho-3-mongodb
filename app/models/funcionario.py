from beanie import Document, Link
from pydantic import BaseModel, Field, EmailStr
from datetime import date
from typing import Annotated

# Importamos o Setor para criar o vínculo
from app.models.setor import Setor

# 1. Documento Embutido (Vive dentro do funcionário)
class Endereco(BaseModel):
    rua: str
    cidade: str
    estado: str = Field(min_length=2, max_length=2) # Ex: CE, SP

# 2. Documento Principal (Coleção no Banco)
class Funcionario(Document):
    nome: str
    cpf: str = Field(unique=True) # CPF deve ser único
    email: EmailStr
    data_nascimento: date
    salario: float
    
    # Embutido: Os dados do endereço ficam salvos aqui dentro
    endereco: Endereco 
    
    # Relacionamento: Guarda apenas o ID do setor
    setor: Link[Setor]

    class Settings:
        name = "funcionarios"