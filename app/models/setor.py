from typing import Optional
from beanie import Document
from pydantic import Field

class Setor(Document):
    """
    Modelo que representa um Setor no banco de dados.
    Herda de Document (Beanie) para virar uma coleção no MongoDB.
    """
    nome: str = Field(..., description="Nome do setor (Ex: TI, RH)")
    responsavel: str | None = Field(None, description="Nome do responsável pelo setor")
    
    class Settings:
        name = "setores"