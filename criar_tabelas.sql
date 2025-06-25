-- Script criar_tabelas.sql baseado no modelo lógico final

CREATE TABLE IF NOT EXISTS tb_especie (
    id_esp INTEGER PRIMARY KEY AUTO_INCREMENT,
    nome_especie VARCHAR(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS tb_raca (
    id_raca INTEGER PRIMARY KEY AUTO_INCREMENT,
    nome_raca VARCHAR(50) NOT NULL,
    id_esp_fkc INTEGER,
    FOREIGN KEY (id_esp_fkc) REFERENCES tb_especie(id_esp) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS tb_cliente (
    id_cli INTEGER PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(100) NOT NULL,
    telefone VARCHAR(20),
    endereco_completo TEXT,
    cpf_cnpj VARCHAR(20) UNIQUE
);

CREATE TABLE IF NOT EXISTS tb_funcionario (
    id_fun INTEGER PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(100) NOT NULL,
    telefone VARCHAR(20),
    cpf VARCHAR(14) UNIQUE,
    tipo_funcionario VARCHAR(20) NOT NULL, -- 'Atendente' ou 'Veterinario'
    crmv VARCHAR(30),                      -- Apenas se Veterinario
    especialidade VARCHAR(100)             -- Apenas se Veterinario
);

CREATE TABLE IF NOT EXISTS tb_pet (
    id_pet INTEGER PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(50) NOT NULL,
    data_nascimento DATE,
    sexo VARCHAR(10),
    status VARCHAR(20),
    id_cli_fkc INTEGER,
    id_raca_fkc INTEGER,
    FOREIGN KEY (id_cli_fkc) REFERENCES tb_cliente(id_cli) ON DELETE CASCADE,
    FOREIGN KEY (id_raca_fkc) REFERENCES tb_raca(id_raca) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS tb_agendamento (
    id_age INTEGER PRIMARY KEY AUTO_INCREMENT,
    data_hora TIMESTAMP NOT NULL,
    fk_id_pet INTEGER,
    fk_id_fun INTEGER,
    FOREIGN KEY (fk_id_pet) REFERENCES tb_pet(id_pet) ON DELETE CASCADE,
    FOREIGN KEY (fk_id_fun) REFERENCES tb_funcionario(id_fun) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS tb_consulta (
    id_con INTEGER PRIMARY KEY AUTO_INCREMENT,
    id_pet_fkc INTEGER,
    id_fun_fkc INTEGER,
    id_age_fkc INTEGER,
    queixa TEXT,
    diagnostico TEXT,
    status VARCHAR(50),
    FOREIGN KEY (id_pet_fkc) REFERENCES tb_pet(id_pet) ON DELETE CASCADE,
    FOREIGN KEY (id_fun_fkc) REFERENCES tb_funcionario(id_fun) ON DELETE SET NULL,
    FOREIGN KEY (id_age_fkc) REFERENCES tb_agendamento(id_age) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS tb_produto (
    id_prod INTEGER PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(100) NOT NULL,
    preco DECIMAL(10,2) NOT NULL,
    requer_prescricao BOOLEAN
);

CREATE TABLE IF NOT EXISTS tb_fatura (
    id_fat INTEGER PRIMARY KEY AUTO_INCREMENT,
    id_cli_fkc INTEGER,
    id_con_fkc INTEGER,
    data_emissao DATE,
    valor_total DECIMAL(10,2),
    status VARCHAR(20),
    FOREIGN KEY (id_cli_fkc) REFERENCES tb_cliente(id_cli) ON DELETE CASCADE,
    FOREIGN KEY (id_con_fkc) REFERENCES tb_consulta(id_con) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS tb_item_fatura (
    id_fat_fkc INTEGER,
    id_prod_fkc INTEGER,
    quantidade INTEGER,
    PRIMARY KEY (id_fat_fkc, id_prod_fkc),
    FOREIGN KEY (id_fat_fkc) REFERENCES tb_fatura(id_fat) ON DELETE CASCADE,
    FOREIGN KEY (id_prod_fkc) REFERENCES tb_produto(id_prod) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS tb_prescricao (
    id_con_fkc INTEGER,
    id_prod_fkc INTEGER,
    receita TEXT,
    PRIMARY KEY (id_con_fkc, id_prod_fkc),
    FOREIGN KEY (id_con_fkc) REFERENCES tb_consulta(id_con) ON DELETE CASCADE,
    FOREIGN KEY (id_prod_fkc) REFERENCES tb_produto(id_prod) ON DELETE CASCADE
);
