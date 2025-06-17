# consultas.py
from crud_base import executar_comando
import csv

# salvar arquivo da consulta
def salvar_csv(dados, cabecalho, nome_arquivo):
    
    try:
        with open(nome_arquivo, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(cabecalho)
            writer.writerows(dados)
        print(f"Dados salvos em '{nome_arquivo}'.")
    
    except Exception as e:
        print(f"Erro ao salvar CSV: {e}")

# consulta de atendimentos por mês
def consulta_atendimentos_mes():
    print("\n--- Consulta: Total de Atendimentos por Mês ---")
    
    query = """
        SELECT DATE_FORMAT(c.data_hora_agendada, '%Y-%m') AS mes_ano, COUNT(c.id) AS total_consultas
        FROM consulta c
        GROUP BY mes_ano
        ORDER BY mes_ano;
    """
    resultados = executar_comando(query, fetch=True)
    salvar_csv(resultados, ["Mês/Ano", "Total de Consultas"], "atendimentos_mes.csv")

# consulta de pets por espécie e veterinário
def consulta_pets_por_especie_e_vet():
    print("\n--- Consulta: Pets por Espécie e Veterinário ---")
    query = """
        SELECT v.nome, r.especie, COUNT(DISTINCT p.id)
        FROM consulta c
        JOIN pet p ON c.id_pet = p.id
        JOIN raca r ON p.id_raca = r.id
        JOIN veterinario v ON c.id_veterinario = v.id
        GROUP BY v.nome, r.especie
        ORDER BY v.nome;
    """
    resultados = executar_comando(query, fetch=True)
    salvar_csv(resultados, ["Veterinário", "Espécie", "Total"], "pets_por_especie_vet.csv")

# consulta da média de duração de tratamentos por especialidade
def consulta_media_tratamentos():
    print("\n--- Consulta: Média de Duração de Tratamentos por Especialidade ---")
    query = """
        SELECT v.especialidade, AVG(t.duracao_dias)
        FROM tratamento t
        JOIN consulta c ON t.id_consulta = c.id
        JOIN veterinario v ON c.id_veterinario = v.id
        GROUP BY v.especialidade;
    """
    resultados = executar_comando(query, fetch=True)
    salvar_csv(resultados, ["Especialidade", "Média Duração (dias)"], "media_duracao_tratamentos.csv")

def menu_consultas():
    while True:
        print("\n--- Menu Consultas ---")
        print("1. Atendimentos por Mês")
        print("2. Pets por Espécie e Veterinário")
        print("3. Média de Duração de Tratamentos")
        print("0. Voltar")
        op = input("Escolha: ")
        if op == "1": consulta_atendimentos_mes()
        elif op == "2": consulta_pets_por_especie_e_vet()
        elif op == "3": consulta_media_tratamentos()
        elif op == "0": break
        else: print("Inválido")