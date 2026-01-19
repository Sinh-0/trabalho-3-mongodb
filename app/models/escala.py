from typing import List
from datetime import datetime
from beanie import Document, Link, PydanticObjectId
from app.models.funcionario import Funcionario
from app.models.setor import Setor

class Escala(Document):
    nome: str
    inicio: datetime
    fim: datetime
    ativa: bool = True
    
    setor: Link[Setor]
    
    equipe: List[Link[Funcionario]] 

    class Settings:
        name = "escalas"