# crud_base.py
import mysql.connector
from mysql.connector import errorcode

DB_CONFIG = {
    "database": "clinica_vet",
    "user": "lucasschemes",
    "password": "clinica123",
    "host": "localhost",
    "port": "3306"
}

def conectar():
    try:
        return mysql.connector.connect(**DB_CONFIG)
    except mysql.connector.Error as err:
        print(f"Erro ao conectar: {err}")
        return None

def executar_comando(comando, params=None, fetch=False):
    conn = conectar()
    if not conn: return None if fetch else False
    try:
        with conn.cursor() as cur:
            cur.execute(comando, params)
            if fetch:
                resultado = cur.fetchall()
            conn.commit()
            return resultado if fetch else True
    except mysql.connector.Error as err:
        print(f"Erro SQL: {err}")
        if conn: conn.rollback()
        return None if fetch else False
    finally:
        if conn and conn.is_connected():
            conn.close()

def listar_registros(tabela, colunas="*", joins="", where="", order_by=None):
    alias = tabela.split(' ')[-1] if ' ' in tabela else tabela
    query = f"SELECT {colunas} FROM {tabela} {joins} {where} ORDER BY {order_by or alias + '.id'}"
    registros = executar_comando(query, fetch=True)
    for r in registros or []:
        print(r)
    return registros

def pedir_input(mensagem, tipo=str, obrigatorio=True, opcoes=None):
    
    while True:
        valor = input(mensagem + ": ").strip()
        if not valor and not obrigatorio:
            return None
        
        try:
            if tipo == str and ('data' in mensagem.lower() or 'horario' in mensagem.lower()) and valor:
                pass
            return tipo(valor)
        
        except ValueError:
            print("Entrada inválida.")

def selecionar_id(tabela, nome_campo_display="nome", id_campo="id"):
    
    registros = listar_registros(tabela, f"{id_campo}, {nome_campo_display}")
    
    if not registros:
        print("Nenhum registro encontrado.")
        return None
    
    while True:
        
        try:
            valor = int(input(f"Digite o ID de {tabela}: "))
            
            if any(r[0] == valor for r in registros):
                return valor
            
            else:
                print("ID não encontrado. Tente novamente.")
        
        except ValueError:
            print("ID inválido. Por favor, digite um número.")

def menu_crud(nome_entidade, tabela, campos, listar_func):
    
    def cadastrar():
        valores = []
        colunas = []
        for nome, tipo, fk, obrig in campos: 
            
            if fk:
                val = selecionar_id(fk[0], fk[1])
                if obrig and val is None: 
                    print(f"Campo {nome_entidade}.{nome} é obrigatório. Cadastro cancelado.")
                    return False 
            
            else:
                val = pedir_input(f"{nome_entidade}.{nome}", tipo, obrig)
            valores.append(val)
            colunas.append(nome)
        
        query = f"INSERT INTO {tabela} ({', '.join(colunas)}) VALUES ({', '.join(['%s']*len(valores))})"
        if executar_comando(query, tuple(valores)):
            print(f"{nome_entidade} cadastrado com sucesso!")
        else:
            print(f"Erro ao cadastrar {nome_entidade}.")
        return True

    def atualizar():
        print(f"\n--- Atualizar {nome_entidade} ---")
        listar_func()
        id_registro = pedir_input(f"Digite o ID do {nome_entidade} para atualizar", int, True)
        if id_registro is None: return

        updates = []
        params = []
        for nome, tipo, fk, obrigatorio_campo in campos: # Renomeado para evitar conflito de nomes
            resposta = pedir_input(f"Novo valor para {nome_entidade}.{nome} (deixe em branco para não alterar)", tipo, False)
            if resposta is not None:
                updates.append(f"{nome} = %s")
                params.append(resposta)
        
        if not updates:
            print("Nenhuma alteração informada.")
            return

        params.append(id_registro) # Adiciona o ID ao final dos parâmetros
        query = f"UPDATE {tabela} SET {', '.join(updates)} WHERE id = %s"
        if executar_comando(query, tuple(params)):
            print(f"✅ {nome_entidade} atualizado com sucesso!")
        else:
            print(f"❌ Erro ao atualizar {nome_entidade}.")

    def deletar():
        print(f"\n--- Deletar {nome_entidade} ---")
        listar_func()
        id_registro = pedir_input(f"Digite o ID do {nome_entidade} para deletar", int, True)
        if id_registro is None: return
        
        query = f"DELETE FROM {tabela} WHERE id = %s"
        if executar_comando(query, (id_registro,)):
            print(f"✅ {nome_entidade} deletado com sucesso!")
        else:
            print(f"❌ Erro ao deletar {nome_entidade}.")

    while True:
        print(f"\n--- {nome_entidade} ---")
        print("1. Listar")
        print("2. Cadastrar")
        print("3. Atualizar")
        print("4. Deletar")
        print("0. Voltar")
        op = input("Escolha: ")
        if op == "1": listar_func()
        elif op == "2": cadastrar()
        elif op == "3": atualizar()
        elif op == "4": deletar()
        elif op == "0": break
        else: print("Inválido")