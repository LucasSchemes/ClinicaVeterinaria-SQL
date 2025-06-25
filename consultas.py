import pandas as pd

def executar_consultas(cursor):
    while True:
        print("\n--- Consultas Sumarizadas ---")
        print("1. Total de faturas por cliente")
        print("2. Produtos mais vendidos por quantidade")
        print("3. Faturamento por espécie de pet")
        print("0. Voltar ao menu principal")
        opcao = input("Escolha uma consulta: ")

        if opcao == '1':
            consulta_faturas_por_cliente(cursor)
        elif opcao == '2':
            consulta_produtos_mais_vendidos(cursor)
        elif opcao == '3':
            consulta_faturamento_por_especie(cursor)
        elif opcao == '0':
            break
        else:
            print("Opção inválida.")

def consulta_faturas_por_cliente(cursor):
    print("\nConsulta: Total de faturas por cliente (somatório de valores).")

    sql = """
        SELECT c.nome AS Cliente, COUNT(f.id_fat) AS QuantidadeFaturas, SUM(f.valor_total) AS TotalFaturado
        FROM tb_cliente c
        JOIN tb_fatura f ON c.id_cli = f.id_cli_fkc
        GROUP BY c.nome
    """

    cursor.execute(sql)
    resultados = cursor.fetchall()

    print("\nCliente | Quantidade de Faturas | Total Faturado")
    for linha in resultados:
        print(f"{linha[0]} | {linha[1]} | R${linha[2]:.2f}")

    salvar_csv(resultados, ['Cliente', 'QuantidadeFaturas', 'TotalFaturado'], 'faturas_por_cliente.csv')

def consulta_produtos_mais_vendidos(cursor):
    print("\nConsulta: Produtos mais vendidos (quantidade total).")

    sql = """
        SELECT p.nome AS Produto, SUM(i.quantidade) AS QuantidadeVendida
        FROM tb_produto p
        JOIN tb_item_fatura i ON p.id_prod = i.id_prod_fkc
        JOIN tb_fatura f ON i.id_fat_fkc = f.id_fat
        GROUP BY p.nome
        ORDER BY QuantidadeVendida DESC
    """

    cursor.execute(sql)
    resultados = cursor.fetchall()

    print("\nProduto | Quantidade Vendida")
    for linha in resultados:
        print(f"{linha[0]} | {linha[1]}")

    salvar_csv(resultados, ['Produto', 'QuantidadeVendida'], 'produtos_mais_vendidos.csv')

def consulta_faturamento_por_especie(cursor):
    print("\nConsulta: Faturamento total por espécie de pet.")

    sql = """
        SELECT e.nome_especie AS Especie, SUM(f.valor_total) AS TotalFaturado
        FROM tb_fatura f
        JOIN tb_consulta c ON f.id_con_fkc = c.id_con
        JOIN tb_pet p ON c.id_pet_fkc = p.id_pet
        JOIN tb_raca r ON p.id_raca_fkc = r.id_raca
        JOIN tb_especie e ON r.id_esp_fkc = e.id_esp
        GROUP BY e.nome_especie
    """

    cursor.execute(sql)
    resultados = cursor.fetchall()

    print("\nEspécie | Total Faturado")
    for linha in resultados:
        print(f"{linha[0]} | R${linha[1]:.2f}")

    salvar_csv(resultados, ['Especie', 'TotalFaturado'], 'faturamento_por_especie.csv')

def salvar_csv(resultados, colunas, nome_arquivo):
    try:
        df = pd.DataFrame(resultados, columns=colunas)
        df.to_csv(nome_arquivo, index=False)
        print(f"Resultado salvo em: {nome_arquivo}")
    except Exception as e:
        print(f"Erro ao salvar CSV: {e}")
