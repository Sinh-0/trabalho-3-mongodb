import asyncio
import random
from app.database import init_db
from app.models.setor import Setor
from app.models.funcionario import Funcionario, Endereco
from app.models.escala import Escala

async def main():
    await init_db()
    print("🔌 Banco conectado.")

    print("🧹 Limpando dados antigos...")
    await Escala.delete_all()
    await Funcionario.delete_all()
    await Setor.delete_all()

    # 1. Cria Setores
    print("🏢 Criando Setores...")
    nomes_setores = ["Tecnologia", "Recursos Humanos", "Financeiro", "Operações", "Marketing"]
    setores_objs = []
    
    for nome in nomes_setores:
        setor = await Setor(nome=nome, responsavel=f"Gerente {nome[:3]}").create()
        setores_objs.append(setor)

    # 2. Cria 20 Funcionários com Nomes Reais
    print("👷 Criando 20 Funcionários...")
    
    nomes_primeiros = ["Lucas", "Ana", "Marcos", "Beatriz", "João", "Mariana", "Pedro", "Julia", "Gabriel", "Larissa", "Rafael", "Camila"]
    sobrenomes = ["Silva", "Santos", "Oliveira", "Souza", "Rodrigues", "Ferreira", "Almeida", "Costa", "Pereira", "Lima"]
    cargos = ["Desenvolvedor", "Analista", "Gerente", "Assistente", "Estagiário", "Coordenador"]
    
    funcionarios_objs = []
    
    for i in range(20):
        nome_completo = f"{random.choice(nomes_primeiros)} {random.choice(sobrenomes)}"
        setor_escolhido = random.choice(setores_objs)
        salario_base = random.randint(2500, 12000)
        
        # Gera data aleatória entre 1980 e 2000
        ano_nasc = random.randint(1980, 2003)
        mes_nasc = random.randint(1, 12)
        dia_nasc = random.randint(1, 28)
        
        func = await Funcionario(
            nome=nome_completo,
            cpf=f"{random.randint(100,999)}.{random.randint(100,999)}.{random.randint(100,999)}-{random.randint(10,99)}",
            email=f"{nome_completo.lower().replace(' ', '.')}@empresa.com",
            data_nascimento=f"{ano_nasc}-{mes_nasc:02d}-{dia_nasc:02d}",
            salario=float(salario_base),
            endereco=Endereco(
                rua=f"Rua {random.choice(['das Flores', 'do Sol', 'da Paz', 'Principal'])}, {random.randint(1, 500)}", 
                cidade=random.choice(["Quixadá", "Fortaleza", "Sobral", "Juazeiro"]), 
                estado="CE"
            ),
            setor=setor_escolhido
        ).create()
        funcionarios_objs.append(func)

    # 3. Cria 10 Escalas
    print("📅 Criando 10 Escalas...")
    tipos_escala = ["Plantão Fim de Semana", "Turno Manhã", "Turno Tarde", "Sobreaviso Noturno"]
    
    for i in range(10):
        # Seleciona de 2 a 4 funcionários aleatórios
        equipe_random = random.sample(funcionarios_objs, k=random.randint(2, 4))
        
        # Tenta pegar o setor da maioria ou do primeiro (para ficar coerente)
        setor_da_escala = equipe_random[0].setor 
        
        mes = random.randint(1, 12)
        dia = random.randint(1, 20)
        
        await Escala(
            nome=f"{random.choice(tipos_escala)} - Grupo {i+1}",
            inicio=f"2026-{mes:02d}-{dia:02d}T08:00:00",
            fim=f"2026-{mes:02d}-{dia+5:02d}T18:00:00",
            ativa=True,
            setor=setor_da_escala,
            equipe=equipe_random
        ).create()

    print("concluído")

if __name__ == "__main__":
    asyncio.run(main())