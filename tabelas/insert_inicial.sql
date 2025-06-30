
-- Inserir espécies
INSERT INTO tb_especie (nome_especie) VALUES ('Canina');
INSERT INTO tb_especie (nome_especie) VALUES ('Felina');

-- Inserir raças
INSERT INTO tb_raca (nome_raca, id_esp_fkc) VALUES ('Labrador', 1);
INSERT INTO tb_raca (nome_raca, id_esp_fkc) VALUES ('Persa', 2);

-- Inserir clientes
INSERT INTO tb_cliente (nome, telefone, endereco_completo, cpf_cnpj) VALUES 
('Joao Silva', '48999999999', 'Rua das Flores, 123', '111.111.111-11'),
('Maria Santos', '48988888888', 'Av. Central, 456', '222.222.222-22');

-- Inserir funcionários
INSERT INTO tb_funcionario (nome, telefone, cpf, tipo_funcionario, crmv, especialidade) VALUES 
('Carlos Mendes', '48977777777', '333.333.333-33', 'Veterinario', 'CRMV123', 'Clinica Geral'),
('Ana Paula', '48966666666', '444.444.444-44', 'Atendente', NULL, NULL),
('Fernanda Lima', '48955555555', '555.555.555-55', 'Veterinario', 'CRMV124', 'Cirurgia'),
('Joao Neto', '48944444444', '666.666.666-66', 'Veterinario', 'CRMV125', 'Dermatologia');

-- Inserir pets
INSERT INTO tb_pet (nome, data_nascimento, sexo, status, id_cli_fkc, id_raca_fkc) VALUES 
('Rex', '2020-05-20', 'M', 'Ativo', 1, 1),
('Mia', '2019-03-15', 'F', 'Ativo', 2, 2);

-- Inserir agendamentos
INSERT INTO tb_agendamento (data_hora, fk_id_pet, fk_id_fun) VALUES 
('2025-06-24 10:00:00', 1, 1),
('2025-06-25 14:00:00', 2, 1),
('2025-06-26 09:00:00', 2, 4),
('2025-06-27 10:00:00', 1, 4),
('2025-06-28 11:00:00', 2, 3),
('2025-06-29 14:00:00', 1, 3);


-- Inserir consultas
INSERT INTO tb_consulta (id_pet_fkc, id_fun_fkc, id_age_fkc, queixa, diagnostico, status) VALUES 
(1, 1, 1, 'Tosse frequente', 'Resfriado leve', 'Concluida'),
(2, 1, 2, 'Apatia e falta de apetite', 'Infecção urinaria', 'Concluida'),
(1, 1, 3, 'Febre e vomito', 'Gastrite leve', 'Concluida'),
(2, 4, 4, 'Tosse seca', 'Resfriado', 'Concluida'),
(1, 4, 5, 'Coceira intensa', 'Alergia alimentar', 'Concluida'),
(2, 3, 6, 'Ferida na pata', 'Infecção bacteriana', 'Concluida'),
(1, 3, 6, 'Letargia', 'Deficiência vitamínica', 'Concluida');

-- Inserir produtos
INSERT INTO tb_produto (nome, preco, requer_prescricao, tipo) VALUES 
('Antibiotico A', 50.00, TRUE, 'Medicamento'),
('Vermifugo B', 30.00, FALSE, 'Medicamento'),
('Antibiotico C', 150.00, TRUE, 'Medicamento'),
('Vermifugo C', 30.00, TRUE, 'Medicamento'),
('Anti-inflamatorio C', 60.00, TRUE, 'Medicamento');

-- Inserir faturas
INSERT INTO tb_fatura (id_cli_fkc, id_con_fkc, data_emissao, valor_total, status) VALUES 
(1, 1, '2025-06-24', 80.00, 'Pago'),
(2, 2, '2025-06-25', 50.00, 'Pendente'),
(1, 3, '2025-06-28', 180.00, 'Pendente'),
(2, 4, '2025-06-29', 320.00, 'Pago'),
(1, 5, '2025-06-30', 100.00, 'Pago');

-- Inserir itens de fatura
INSERT INTO tb_item_fatura (id_fat_fkc, id_prod_fkc, quantidade) VALUES 
(1, 1, 1), 
(1, 2, 1), 
(2, 3, 1),
(2, 2, 2),
(3, 1, 1),
(4, 3, 2),
(5, 2, 1);

-- Inserir prescrições
INSERT INTO tb_prescricao (id_con_fkc, id_prod_fkc, receita) VALUES 
(1, 1, 'Administrar o antibiotico A por 7 dias.'),
(2, 2, 'Dar o vermifugo B conforme orientacao.'),
(3, 1, 'Repetir dose do Antibiotico A por 3 dias.'),
(4, 3, 'Aplicar Antibiotico C durante 7 dias.'),
(5, 3, 'Aplicar Antibiotico C em dias alternados.');
