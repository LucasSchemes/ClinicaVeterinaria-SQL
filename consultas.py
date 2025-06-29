import os
import csv
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import MaxNLocator
def carregar_sql(nome_arquivo):
    try:
        caminho = os.path.join('consultas', nome_arquivo)
        with open(caminho, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        print(f"❌ Erro ao carregar arquivo SQL: {e}")
        return None

def exportar_csv(colunas, resultados, nome_arquivo_csv):
    try:
        pasta = 'exportacoes'
        if not os.path.exists(pasta):
            os.makedirs(pasta)

        caminho = os.path.join(pasta, nome_arquivo_csv)
        with open(caminho, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(colunas)
            writer.writerows(resultados)

        print(f"✅ Resultado exportado para {caminho}")
        print("💡 Você pode abrir este arquivo no Excel para criar o gráfico.")
    except Exception as e:
        print(f"❌ Erro ao exportar CSV: {e}")

def gerar_grafico_csv(nome_arquivo_csv, titulo, coluna_x, coluna_y):
    try:
        caminho_csv = os.path.join('exportacoes', nome_arquivo_csv)
        df = pd.read_csv(caminho_csv)

        if coluna_x not in df.columns or coluna_y not in df.columns:
            print("❌ Colunas não encontradas para gerar gráfico.")
            return

        sns.set(style="whitegrid")
        plt.figure(figsize=(10, 6))
        ax = sns.barplot(data=df, x=coluna_x, y=coluna_y, palette="crest")

        # Títulos e rótulos
        plt.title(titulo, fontsize=16, weight='bold')
        label_x = coluna_x.replace("_", " ").title()
        label_y = coluna_y.replace("_", " ").title()

        plt.xlabel(label_x, fontsize=12)
        plt.ylabel(label_y, fontsize=12)
        plt.xticks(rotation=0, ha='center')

        # Ajuste de escala Y com base no arquivo
        if 'consultas_por_veterinario' in nome_arquivo_csv:
            ax.set_ylim(0, 10)
            ax.yaxis.set_major_locator(MaxNLocator(integer=True))
        elif 'prescricoes_por_produto' in nome_arquivo_csv:
            ax.set_ylim(0, 10)
            ax.yaxis.set_major_locator(MaxNLocator(integer=True))
        elif 'faturamento_por_cliente' in nome_arquivo_csv:
            ax.set_ylim(0, 1000)
            ax.yaxis.set_major_locator(MaxNLocator(nbins=6, integer=True))
        else:
            ax.yaxis.set_major_locator(MaxNLocator(integer=True))  # padrão

        
        for p in ax.patches:
            valor = p.get_height()
            ax.annotate(f'{int(valor) if valor.is_integer() else f"{valor:.2f}"}',
                        (p.get_x() + p.get_width() / 2, valor),
                        ha='center', va='bottom', fontsize=10, color='black')

        plt.tight_layout()
        caminho_imagem = caminho_csv.replace(".csv", ".png")
        plt.savefig(caminho_imagem)
        plt.close()
        print(f"📊 Gráfico salvo em: {caminho_imagem}")

    except Exception as e:
        print(f"❌ Erro ao gerar gráfico: {e}")

def executar_consultas(cursor):
    while True:
        print("\n" + "=" * 50)
        print("📊 Consultas e Relatórios 📊".center(50))
        print("=" * 50)
        print("1. Faturamento total por cliente")
        print("2. Total de consultas por veterinário")
        print("3. Prescrições por produto")
        print("0. Voltar")
        print("=" * 50)

        opcao = input("Escolha uma consulta: ")

        if opcao == '1':
            consulta = carregar_sql('consulta_faturamento_por_cliente.sql')
            titulo = "Faturamento por Cliente"
            nome_csv = "faturamento_por_cliente.csv"
        elif opcao == '2':
            consulta = carregar_sql('consulta_consultas_por_veterinario.sql')
            titulo = "Consultas por Veterinário"
            nome_csv = "consultas_por_veterinario.csv"
        elif opcao == '3':
            consulta = carregar_sql('consulta_prescricoes_por_produto.sql')
            titulo = "Prescrições por Produto"
            nome_csv = "prescricoes_por_produto.csv"
        elif opcao == '0':
            break
        else:
            print("❌ Opção inválida.")
            continue

        if consulta:
            try:
                cursor.execute(consulta)
                resultados = cursor.fetchall()
                colunas = [desc[0] for desc in cursor.description]

                print(f"\n{titulo}")
                print(" | ".join(colunas))
                for linha in resultados:
                    print(" | ".join(str(campo) for campo in linha))

                print("\n✅ Consulta executada com sucesso!")

               
                exportar_csv(colunas, resultados, nome_csv)
                gerar_grafico_csv(nome_csv, titulo, colunas[0], colunas[1])

            except Exception as e:
                print(f"❌ Erro ao executar consulta: {e}")
        else:
            print("❌ Consulta não carregada.")
