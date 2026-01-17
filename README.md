# Trabalho 3 - Persistência com MongoDB

## Diagrama de Classes
```mermaid
classDiagram
    class Setor {
        +_id: ObjectId
        +nome: str
        +responsavel: str
    }

    class Endereco {
        +rua: str
        +cidade: str
        +estado: str
    }

    class Funcionario {
        +_id: ObjectId
        +nome: str
        +cpf: str
        +email: str
        +salario: float
        +data_nascimento: date
        +endereco: Endereco
        +setor: Link~Setor~
    }

    class Escala {
        +_id: ObjectId
        +nome: str
        +inicio: datetime
        +fim: datetime
        +ativa: bool
        +setor: Link~Setor~
        +equipe: List~Link~Funcionario~~
    }

    %% Relacionamentos
    Funcionario *-- Endereco : "Contém (Embutido)"
    Funcionario --> Setor : "Pertence a (1:N)"
    Escala --> Setor : "Pertence a (1:N)"
    Escala "1" --> "N" Funcionario : "Equipe (M:N)"
```