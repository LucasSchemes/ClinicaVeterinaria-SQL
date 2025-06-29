import mysql.connector
from gerenciar import gerencia_registros
from consultas import executar_consultas
from ia_module import sugerir_diagnostico_ia

def menu(conexao, cursor):
    crud = gerencia_registros(conexao, cursor)

    while True:
        print("\n" + "=" * 50)
        print("🐾  Sistema de Gestão - Clínica Veterinária 🐾".center(50))
        print("=" * 50)
        print("1️⃣  Criar tabelas do banco")
        print("2️⃣  Carregar dados iniciais")
        print("3️⃣  Excluir tabelas do banco")
        print("4️⃣  Gerenciar registros (CRUD)")
        print("5️⃣  Consultas e Relatórios")
        print("6️⃣  IA: Sugestão de diagnóstico")
        print("0️⃣  Sair do sistema")
        print("=" * 50)

        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            criar_tabelas(cursor, conexao)
        elif opcao == '2':
            carregar_dados_iniciais(cursor, conexao)
        elif opcao == '3':
            excluir_tabelas(cursor, conexao)
        elif opcao == '4':
            crud.menu_crud()
        elif opcao == '5':
            executar_consultas(cursor)
        elif opcao == '6':
            sugerir_diagnostico_ia()
        elif opcao == '0':
            print("\n👋 Encerrando o sistema. Até logo!")
            break
        else:
            print("❌ Opção inválida. Tente novamente.")

def criar_tabelas(cursor, conexao):
    try:
        with open('tabelas/criar_tabelas.sql', 'r') as file:
            comandos = file.read()
            for comando in comandos.split(';'):
                if comando.strip():
                    cursor.execute(comando)
            conexao.commit()
        print("✅ Tabelas criadas com sucesso.")
    except Exception as e:
        print(f"❌ Erro ao criar tabelas: {e}")

def carregar_dados_iniciais(cursor, conexao):
    try:
        with open('tabelas/insert_inicial.sql', 'r') as file:
            comandos = file.read()
            for comando in comandos.split(';'):
                if comando.strip():
                    cursor.execute(comando)
            conexao.commit()
        print("✅ Dados carregados com sucesso.")
    except Exception as e:
        print(f"❌ Erro ao carregar dados: {e}")

def excluir_tabelas(cursor, conexao):
    try:
        with open('tabelas/droptabelas.sql', 'r') as file:
            comandos = file.read()
            for comando in comandos.split(';'):
                if comando.strip():
                    cursor.execute(comando)
            conexao.commit()
        print("✅ Tabelas excluídas com sucesso.")
    except Exception as e:
        print(f"❌ Erro ao excluir tabelas: {e}")

if __name__ == "__main__":
    try:
        with mysql.connector.connect(
            user='lucasschemes',
            password='clinica123',
            host='localhost',
            database='clinica_vet',
            port=3306
        ) as conexao:
            with conexao.cursor() as cursor:
                print("\n🌟 Conexão com banco de dados realizada com sucesso! 🌟")
                menu(conexao, cursor)

    except Exception as e:
        print(f"❌ Erro ao conectar ao banco: {e}")
