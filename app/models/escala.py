from typing import List
from datetime import datetime
from beanie import Document, Link
from app.models.funcionario import Funcionario
from app.models.setor import Setor

class Escala(Document):
    nome: str
    inicio: datetime
    fim: datetime
    ativa: bool = True
    
    # Uma escala pertence a um setor
    setor: Link[Setor]
    
    # Lista de funcionários (Muitos para Muitos)
    equipe: List[Link[Funcionario]] 

    class Settings:
        name = "escalas"