# sql.py
from crud_base import conectar
import mysql.connector

def criar_tabelas():
    
    comandos = [
        CREATE TABLE IF NOT EXISTS cliente (
            id INT PRIMARY KEY AUTO_INCREMENT, -- CORRIGIDO: Removido o 'PRIMARY' duplicado
            nome VARCHAR(100) NOT NULL,
            telefone VARCHAR(20),
            endereco_completo TEXT,
            cpf_cnpj VARCHAR(20) UNIQUE
        ) ENGINE=InnoDB;,
        # ... o restante dos seus comandos CREATE TABLE seguem aqui ...
        '''CREATE TABLE IF NOT EXISTS raca (
            id INT PRIMARY KEY AUTO_INCREMENT,
            nome VARCHAR(50) NOT NULL,
            especie VARCHAR(30) NOT NULL
        ) ENGINE=InnoDB;''',
        '''CREATE TABLE IF NOT EXISTS funcionario (
            id INT PRIMARY KEY AUTO_INCREMENT,
            nome VARCHAR(100) NOT NULL,
            telefone VARCHAR(20),
            cpf VARCHAR(14) UNIQUE
        ) ENGINE=InnoDB;''',
        '''CREATE TABLE IF NOT EXISTS veterinario (
            id INT PRIMARY KEY AUTO_INCREMENT,
            nome VARCHAR(100) NOT NULL,
            especialidade VARCHAR(100),
            crmv VARCHAR(30) UNIQUE
        ) ENGINE=InnoDB;''',
        '''CREATE TABLE IF NOT EXISTS pet (
            id INT PRIMARY KEY AUTO_INCREMENT,
            nome VARCHAR(50) NOT NULL,
            data_nascimento DATE,
            sexo VARCHAR(10),
            status VARCHAR(20),
            id_cliente INT,
            id_raca INT,
            FOREIGN KEY (id_cliente) REFERENCES cliente(id) ON DELETE CASCADE,
            FOREIGN KEY (id_raca) REFERENCES raca(id) ON DELETE SET NULL
        ) ENGINE=InnoDB;''',
        '''CREATE TABLE IF NOT EXISTS consulta (
            id INT PRIMARY KEY AUTO_INCREMENT,
            data_hora_agendada DATETIME NOT NULL,
            queixa TEXT,
            diagnostico TEXT,
            status VARCHAR(50),
            id_pet INT,
            id_veterinario INT,
            FOREIGN KEY (id_pet) REFERENCES pet(id) ON DELETE CASCADE,
            FOREIGN KEY (id_veterinario) REFERENCES veterinario(id) ON DELETE SET NULL
        ) ENGINE=InnoDB;''',
        '''CREATE TABLE IF NOT EXISTS tratamento (
            id INT PRIMARY KEY AUTO_INCREMENT,
            descricao TEXT NOT NULL,
            duracao_dias INT,
            id_consulta INT,
            FOREIGN KEY (id_consulta) REFERENCES consulta(id) ON DELETE CASCADE
        ) ENGINE=InnoDB;''',
        '''CREATE TABLE IF NOT EXISTS vacina (
            id INT PRIMARY KEY AUTO_INCREMENT,
            nome VARCHAR(100) NOT NULL,
            data_aplicacao DATE NOT NULL,
            lote VARCHAR(30),
            id_pet INT,
            FOREIGN KEY (id_pet) REFERENCES pet(id) ON DELETE CASCADE
        ) ENGINE=InnoDB;''',
        '''CREATE TABLE IF NOT EXISTS agendamento (
            id INT PRIMARY KEY AUTO_INCREMENT,
            data DATE NOT NULL,
            horario TIME NOT NULL,
            id_pet INT,
            id_veterinario INT,
            FOREIGN KEY (id_pet) REFERENCES pet(id) ON DELETE CASCADE,
            FOREIGN KEY (id_veterinario) REFERENCES veterinario(id) ON DELETE SET NULL
        ) ENGINE=InnoDB;''',
        '''CREATE TABLE IF NOT EXISTS receita (
            id INT PRIMARY KEY AUTO_INCREMENT,
            texto TEXT NOT NULL,
            id_consulta INT,
            FOREIGN KEY (id_consulta) REFERENCES consulta(id) ON DELETE CASCADE
        ) ENGINE=InnoDB;''',
        '''CREATE TABLE IF NOT EXISTS produto (
            id INT PRIMARY KEY AUTO_INCREMENT,
            nome VARCHAR(100) NOT NULL,
            preco DECIMAL(10,2) NOT NULL,
            prescricao TEXT
        ) ENGINE=InnoDB;''',
        '''CREATE TABLE IF NOT EXISTS fatura (
            id INT PRIMARY KEY AUTO_INCREMENT,
            valor_total DECIMAL(10,2),
            status VARCHAR(20),
            data_emissao DATE,
            id_cliente INT,
            FOREIGN KEY (id_cliente) REFERENCES cliente(id)
        ) ENGINE=InnoDB;''',
        '''CREATE TABLE IF NOT EXISTS item_fatura (
            id INT PRIMARY KEY AUTO_INCREMENT,
            id_fatura INT,
            id_produto INT,
            quantidade INT,
            FOREIGN KEY (id_fatura) REFERENCES fatura(id) ON DELETE CASCADE,
            FOREIGN KEY (id_produto) REFERENCES produto(id) ON DELETE CASCADE
        ) ENGINE=InnoDB;''',
        '''CREATE TABLE IF NOT EXISTS prescricao (
            id INT PRIMARY KEY AUTO_INCREMENT,
            id_consulta INT,
            id_produto INT,
            FOREIGN KEY (id_consulta) REFERENCES consulta(id),
            FOREIGN KEY (id_produto) REFERENCES produto(id)
        ) ENGINE=InnoDB;'''
    ]

    conn = conectar()
    if not conn: return
    try:
        with conn.cursor() as cur:
            print("\nCriando tabelas complementares...")
            for comando in comandos:
                cur.execute(comando)
            conn.commit()
            print("✅ Tabelas complementares criadas com sucesso!")
    except mysql.connector.Error as err:
        print(f"🚨 Erro: {err}")
        if conn: conn.rollback()
    finally:
        if conn and conn.is_connected():
            conn.close()

def eliminar_todas_tabelas():
    confirma = input("Confirma exclusão de todas as tabelas? (s/N): ").lower()
    if confirma != 's': return
    tabelas = ["prescricao", "item_fatura", "fatura", "produto",
               "receita", "agendamento", "vacina", "tratamento", "consulta",
               "pet", "funcionario", "veterinario", "raca", "cliente"]
    conn = conectar()
    if not conn: return
    try:
        with conn.cursor() as cur:
            cur.execute("SET FOREIGN_KEY_CHECKS = 0;")
            for t in tabelas:
                cur.execute(f"DROP TABLE IF EXISTS {t};")
            cur.execute("SET FOREIGN_KEY_CHECKS = 1;")
            conn.commit()
            print("✅ Todas as tabelas foram eliminadas.")
    except mysql.connector.Error as err:
        print(f"🚨 Erro: {err}")
        if conn: conn.rollback()
    finally:
        if conn and conn.is_connected(): conn.close()

def carregar_dados_iniciais():
    """Carrega dados de exemplo nas tabelas MySQL."""
    print("\nCarregando dados iniciais para MySQL (se as tabelas estiverem vazias)...")
    comandos_insert = [
        ("INSERT INTO cliente (nome, telefone, endereco_completo, cpf_cnpj) SELECT 'Ana Silva', '111-2222', 'Rua A, 123', '111.222.333-44' FROM (SELECT 1) AS tmp WHERE NOT EXISTS (SELECT 1 FROM cliente WHERE nome='Ana Silva');",),
        ("INSERT INTO cliente (nome, telefone, endereco_completo, cpf_cnpj) SELECT 'Bruno Costa', '333-4444', 'Av. B, 456', '555.666.777-88' FROM (SELECT 1) AS tmp WHERE NOT EXISTS (SELECT 1 FROM cliente WHERE nome='Bruno Costa');",),
        ("INSERT INTO raca (nome, especie) SELECT 'Labrador', 'Cachorro' FROM (SELECT 1) AS tmp WHERE NOT EXISTS (SELECT 1 FROM raca WHERE nome='Labrador');",),
        ("INSERT INTO raca (nome, especie) SELECT 'Siamês', 'Gato' FROM (SELECT 1) AS tmp WHERE NOT EXISTS (SELECT 1 FROM raca WHERE nome='Siamês');",),
        ("INSERT INTO veterinario (nome, especialidade, crmv) SELECT 'Dr. Carlos', 'Clínico Geral', 'CRMV/SC 1234' FROM (SELECT 1) AS tmp WHERE NOT EXISTS (SELECT 1 FROM veterinario WHERE nome='Dr. Carlos');",),
        ("INSERT INTO veterinario (nome, especialidade, crmv) SELECT 'Dra. Elisa', 'Felinos', 'CRMV/SC 5678' FROM (SELECT 1) AS tmp WHERE NOT EXISTS (SELECT 1 FROM veterinario WHERE nome='Dra. Elisa');",),
        ("INSERT INTO funcionario (nome, telefone, cpf) SELECT 'Fernanda Lima', '999-0000', '123.456.789-01' FROM (SELECT 1) AS tmp WHERE NOT EXISTS (SELECT 1 FROM funcionario WHERE nome='Fernanda Lima');",),
        ("INSERT INTO funcionario (nome, telefone, cpf) SELECT 'Ricardo Alves', '888-1111', '098.765.432-10' FROM (SELECT 1) AS tmp WHERE NOT EXISTS (SELECT 1 FROM funcionario WHERE nome='Ricardo Alves');",),
        ("INSERT INTO pet (nome, data_nascimento, sexo, status, id_cliente, id_raca) SELECT 'Rex', '2022-01-15', 'Macho', 'Ativo', (SELECT id FROM cliente WHERE nome='Ana Silva'), (SELECT id FROM raca WHERE nome='Labrador') FROM (SELECT 1) AS tmp WHERE NOT EXISTS (SELECT 1 FROM pet WHERE nome='Rex');",),
        ("INSERT INTO pet (nome, data_nascimento, sexo, status, id_cliente, id_raca) SELECT 'Mimi', '2023-03-20', 'Fêmea', 'Ativo', (SELECT id FROM cliente WHERE nome='Bruno Costa'), (SELECT id FROM raca WHERE nome='Siamês') FROM (SELECT 1) AS tmp WHERE NOT EXISTS (SELECT 1 FROM pet WHERE nome='Mimi');",),
        ("INSERT INTO produto (nome, preco, prescricao) SELECT 'Ração Premium', 85.50, 'Alimento balanceado para cães adultos.' FROM (SELECT 1) AS tmp WHERE NOT EXISTS (SELECT 1 FROM produto WHERE nome='Ração Premium');",),
        ("INSERT INTO produto (nome, preco, prescricao) SELECT 'Anti-pulgas X', 55.00, 'Aplicar mensalmente na nuca do animal.' FROM (SELECT 1) AS tmp WHERE NOT EXISTS (SELECT 1 FROM produto WHERE nome='Anti-pulgas X');",),
        ("INSERT INTO consulta (data_hora_agendada, queixa, diagnostico, status, id_pet, id_veterinario) SELECT '2024-10-01 10:00:00', 'Check-up anual', 'Saudável', 'Concluída', (SELECT id FROM pet WHERE nome='Rex'), (SELECT id FROM veterinario WHERE nome='Dr. Carlos') FROM (SELECT 1) AS tmp WHERE NOT EXISTS (SELECT 1 FROM consulta c JOIN pet p ON c.id_pet=p.id WHERE p.nome='Rex' AND c.data_hora_agendada='2024-10-01 10:00:00');",),
        ("INSERT INTO consulta (data_hora_agendada, queixa, diagnostico, status, id_pet, id_veterinario) SELECT '2024-11-05 14:30:00', 'Vacina V4', 'Imunização', 'Concluída', (SELECT id FROM pet WHERE nome='Mimi'), (SELECT id FROM veterinario WHERE nome='Dra. Elisa') FROM (SELECT 1) AS tmp WHERE NOT EXISTS (SELECT 1 FROM consulta c JOIN pet p ON c.id_pet=p.id WHERE p.nome='Mimi' AND c.data_hora_agendada='2024-11-05 14:30:00');",),
        ("INSERT INTO consulta (data_hora_agendada, queixa, diagnostico, status, id_pet, id_veterinario) SELECT '2024-11-15 09:00:00', 'Vômito', 'Gastroenterite Leve', 'Concluída', (SELECT id FROM pet WHERE nome='Mimi'), (SELECT id FROM veterinario WHERE nome='Dra. Elisa') FROM (SELECT 1) AS tmp WHERE NOT EXISTS (SELECT 1 FROM consulta c JOIN pet p ON c.id_pet=p.id WHERE p.nome='Mimi' AND c.data_hora_agendada='2024-11-15 09:00:00');",),
        ("INSERT INTO consulta (data_hora_agendada, queixa, diagnostico, status, id_pet, id_veterinario) SELECT '2024-12-01 11:00:00', 'Tosse', 'Bronquite', 'Concluída', (SELECT id FROM pet WHERE nome='Rex'), (SELECT id FROM veterinario WHERE nome='Dr. Carlos') FROM (SELECT 1) AS tmp WHERE NOT EXISTS (SELECT 1 FROM consulta c JOIN pet p ON c.id_pet=p.id WHERE p.nome='Rex' AND c.data_hora_agendada='2024-12-01 11:00:00');",),
        ("INSERT INTO tratamento (descricao, duracao_dias, id_consulta) SELECT 'Antibiótico Amoxicilina', 7, (SELECT c.id FROM consulta c JOIN pet p ON c.id_pet = p.id WHERE p.nome='Mimi' AND c.data_hora_agendada='2024-11-15 09:00:00') FROM (SELECT 1) AS tmp WHERE NOT EXISTS (SELECT 1 FROM tratamento WHERE id_consulta=(SELECT c.id FROM consulta c JOIN pet p ON c.id_pet = p.id WHERE p.nome='Mimi' AND c.data_hora_agendada='2024-11-15 09:00:00'));",),
        ("INSERT INTO vacina (nome, data_aplicacao, lote, id_pet) SELECT 'Anti-rábica', '2024-10-01', 'LOTE2024AR', (SELECT id FROM pet WHERE nome='Rex') FROM (SELECT 1) AS tmp WHERE NOT EXISTS (SELECT 1 FROM vacina WHERE nome='Anti-rábica' AND id_pet=(SELECT id FROM pet WHERE nome='Rex'));",),
        ("INSERT INTO agendamento (data, horario, id_pet, id_veterinario) SELECT '2025-06-10', '10:00:00', (SELECT id FROM pet WHERE nome='Rex'), (SELECT id FROM veterinario WHERE nome='Dr. Carlos') FROM (SELECT 1) AS tmp WHERE NOT EXISTS (SELECT 1 FROM agendamento WHERE data='2025-06-10' AND id_pet=(SELECT id FROM pet WHERE nome='Rex'));",),
        ("INSERT INTO receita (texto, id_consulta) SELECT 'Dipirona 1 gota por kg a cada 8 horas por 3 dias se febre.', (SELECT c.id FROM consulta c JOIN pet p ON c.id_pet = p.id WHERE p.nome='Mimi' AND c.data_hora_agendada='2024-11-15 09:00:00') FROM (SELECT 1) AS tmp WHERE NOT EXISTS (SELECT 1 FROM receita WHERE id_consulta=(SELECT c.id FROM consulta c JOIN pet p ON c.id_pet = p.id WHERE p.nome='Mimi' AND c.data_hora_agendada='2024-11-15 09:00:00'));",),
        ("INSERT INTO fatura (valor_total, status, data_emissao, id_cliente) SELECT 150.00, 'Pendente', '2024-12-01', (SELECT id FROM cliente WHERE nome='Ana Silva') FROM (SELECT 1) AS tmp WHERE NOT EXISTS (SELECT 1 FROM fatura WHERE valor_total=150.00 AND id_cliente=(SELECT id FROM cliente WHERE nome='Ana Silva'));",),
        ("INSERT INTO item_fatura (id_fatura, id_produto, quantidade) SELECT (SELECT id FROM fatura WHERE id_cliente=(SELECT id FROM cliente WHERE nome='Ana Silva') LIMIT 1), (SELECT id FROM produto WHERE nome='Ração Premium'), 2 FROM (SELECT 1) AS tmp WHERE NOT EXISTS (SELECT 1 FROM item_fatura WHERE id_fatura=(SELECT id FROM fatura WHERE id_cliente=(SELECT id FROM cliente WHERE nome='Ana Silva') LIMIT 1) AND id_produto=(SELECT id FROM produto WHERE nome='Ração Premium'));",),
        ("INSERT INTO prescricao (id_consulta, id_produto) SELECT (SELECT id FROM consulta c JOIN pet p ON c.id_pet = p.id WHERE p.nome='Mimi' AND c.data_hora_agendada='2024-11-15 09:00:00'), (SELECT id FROM produto WHERE nome='Anti-pulgas X') FROM (SELECT 1) AS tmp WHERE NOT EXISTS (SELECT 1 FROM prescricao WHERE id_consulta=(SELECT id FROM consulta c JOIN pet p ON c.id_pet = p.id WHERE p.nome='Mimi' AND c.data_hora_agendada='2024-11-15 09:00:00') AND id_produto=(SELECT id FROM produto WHERE nome='Anti-pulgas X'));",)
    ]
    
    conn = conectar()
    if not conn: return
    try:
        with conn.cursor() as cur:
            for comando in comandos_insert:
                try:
                    cur.execute(comando[0])
                except mysql.connector.Error as err:
                    # Ignore duplicate entry errors for idempotency
                    if err.errno == mysql.connector.errorcode.ER_DUP_ENTRY:
                        pass
                    else:
                        print(f"Erro ao inserir dados: {err}")
            conn.commit()
            print("✅ Dados iniciais carregados!")
    except mysql.connector.Error as err:
        print(f"🚨 Erro geral ao carregar dados iniciais: {err}")
        if conn: conn.rollback()
    finally:
        if conn and conn.is_connected():
            conn.close()