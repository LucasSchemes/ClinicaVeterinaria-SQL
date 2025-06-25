import os
from crud import CrudBase
from consultas import executar_consultas
from ia_module import sugerir_diagnostico_ia
import mysql.connector

# Configurações do banco de dados
config = {
    "database": "clinica_vet",
    "user": "lucasschemes",
    "password": "clinica123",
    "host": "localhost",
    "port": "3306"
}


try:
    conexao = mysql.connector.connect(**config)
    cursor = conexao.cursor()
    crud = CrudBase(conexao, cursor)
    print("\n🌟 Conexão com banco de dados realizada com sucesso! 🌟")
except Exception as e:
    print(f"❌ Erro ao conectar ao banco: {e}")
    exit()

def criar_tabelas():
    try:
        with open('criar_tabelas.sql', 'r') as file:
            comandos = file.read()
            for comando in comandos.split(';'):
                if comando.strip():
                    cursor.execute(comando)
            conexao.commit()
        print("✅ Tabelas criadas com sucesso.")
    except Exception as e:
        print(f"❌ Erro ao criar tabelas: {e}")

def carregar_dados_iniciais():
    try:
        with open('insert_inicial.sql', 'r') as file:
            comandos = file.read()
            for comando in comandos.split(';'):
                if comando.strip():
                    cursor.execute(comando)
            conexao.commit()
        print("✅ Dados carregados com sucesso.")
    except Exception as e:
        print(f"❌ Erro ao carregar dados: {e}")

def excluir_tabelas():
    try:
        with open('droptabelas.sql', 'r') as file:
            comandos = file.read()
            for comando in comandos.split(';'):
                if comando.strip():
                    cursor.execute(comando)
            conexao.commit()
        print("✅ Tabelas excluídas com sucesso.")
    except Exception as e:
        print(f"❌ Erro ao excluir tabelas: {e}")

def menu():
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
            criar_tabelas()
        elif opcao == '2':
            carregar_dados_iniciais()
        elif opcao == '3':
            excluir_tabelas()
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

    cursor.close()
    conexao.close()

if __name__ == "__main__":
    menu()
