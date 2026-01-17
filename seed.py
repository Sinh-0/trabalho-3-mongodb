import asyncio
from app.database import init_db
from app.models.setor import Setor
from app.models.funcionario import Funcionario, Endereco
from app.models.escala import Escala

async def main():
    # 1. Inicia o Banco
    await init_db()
    print("🔌 Banco conectado.")

    # 2. Limpa o Banco (Deleta tudo para não duplicar)
    print("🧹 Limpando dados antigos...")
    await Escala.delete_all()
    await Funcionario.delete_all()
    await Setor.delete_all()

    # 3. Cria Setores
    print("🏢 Criando Setores...")
    ti = await Setor(nome="Tecnologia", responsavel="Weslem").create()
    rh = await Setor(nome="Recursos Humanos", responsavel="Maria").create()

    # 4. Cria Funcionários
    print("👷 Criando Funcionários...")
    
    end1 = Endereco(rua="Rua A, 10", cidade="Quixadá", estado="CE")
    func1 = await Funcionario(
        nome="João Dev", 
        cpf="111.111.111-11", 
        email="joao@ti.com", 
        data_nascimento="1990-01-01", 
        salario=5000.0, 
        endereco=end1,
        setor=ti # Link direto com o objeto
    ).create()

    end2 = Endereco(rua="Rua B, 20", cidade="Fortaleza", estado="CE")
    func2 = await Funcionario(
        nome="Ana Front", 
        cpf="222.222.222-22", 
        email="ana@ti.com", 
        data_nascimento="1995-05-05", 
        salario=6000.0, 
        endereco=end2,
        setor=ti
    ).create()

    end3 = Endereco(rua="Rua C, 30", cidade="Sobral", estado="CE")
    func3 = await Funcionario(
        nome="Carlos RH", 
        cpf="333.333.333-33", 
        email="carlos@rh.com", 
        data_nascimento="1985-10-10", 
        salario=4000.0, 
        endereco=end3,
        setor=rh
    ).create()

    # 5. Cria Escalas
    print("📅 Criando Escalas...")
    
    # Escala TI (João e Ana)
    await Escala(
        nome="Plantão Deploy",
        inicio="2026-02-01T22:00:00",
        fim="2026-02-02T06:00:00",
        ativa=True,
        setor=ti,
        equipe=[func1, func2] # Lista de objetos linkados
    ).create()

    # Escala RH (Só Carlos)
    await Escala(
        nome="Plantão Recrutamento",
        inicio="2026-02-05T08:00:00",
        fim="2026-02-05T18:00:00",
        ativa=True,
        setor=rh,
        equipe=[func3]
    ).create()

    print("✅ Seed concluído com sucesso! Banco populado.")

if __name__ == "__main__":
    asyncio.run(main())