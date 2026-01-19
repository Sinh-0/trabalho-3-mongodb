from beanie import Document, Link
from pydantic import BaseModel, Field, EmailStr
from datetime import date
from typing import Annotated

from app.models.setor import Setor

class Endereco(BaseModel):
    rua: str
    cidade: str
    estado: str = Field(min_length=2, max_length=2)

class Funcionario(Document):
    nome: str
    cpf: str = Field(unique=True)
    email: EmailStr
    data_nascimento: date
    salario: float
    
    endereco: Endereco 
    
    setor: Link[Setor]

    class Settings:
        name = "funcionarios"