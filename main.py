from sql import criar_tabelas, eliminar_todas_tabelas, carregar_dados_iniciais
from consultas import menu_consultas
from ia_module import sugerir_diagnostico_ia
from crud_base import menu_crud, listar_registros, conectar, pedir_input, selecionar_id


campos_cliente = [('nome', str, None, True), ('telefone', str, None, False), ('endereco_completo', str, None, False), ('cpf_cnpj', str, None, True)]

campos_pet = [('nome', str, None, True), ('data_nascimento', str, None, False), ('sexo', str, None, False), ('status', str, None, False), ('id_cliente', int, ('cliente', 'nome'), True), ('id_raca', int, ('raca', 'nome'), True)]

campos_veterinario = [('nome', str, None, True), ('especialidade', str, None, False), ('crmv', str, None, True)]

campos_funcionario = [('nome', str, None, True), ('telefone', str, None, False), ('cpf', str, None, True)]

campos_consulta = [('data_hora_agendada', str, None, True), ('queixa', str, None, False), ('diagnostico', str, None, False), ('status', str, None, False), ('id_pet', int, ('pet', 'nome'), True), ('id_veterinario', int, ('veterinario', 'nome'), True)]

campos_produto = [('nome', str, None, True), ('preco', float, None, True), ('prescricao', str, None, False)]

campos_fatura = [('valor_total', float, None, True), ('status', str, None, True), ('data_emissao', str, None, True), ('id_cliente', int, ('cliente', 'nome'), True)]

campos_item_fatura = [('id_fatura', int, ('fatura', 'id'), True), ('id_produto', int, ('produto', 'nome'), True), ('quantidade', int, None, True)]

campos_prescricao = [('id_consulta', int, ('consulta cons', "CONCAT(cons.id, ' - ', cons.data_hora_agendada)"), True), ('id_produto', int, ('produto', 'nome'), True)]

campos_raca = [('nome', str, None, True), ('especie', str, None, True)]

campos_tratamento = [('descricao', str, None, True), ('duracao_dias', int, None, True), ('id_consulta', int, ('consulta cons', "CONCAT(cons.id, ' - ', cons.data_hora_agendada)"), True)]

campos_vacina = [('nome', str, None, True), ('data_aplicacao', str, None, True), ('lote', str, None, False), ('id_pet', int, ('pet', 'nome'), True)]

campos_agendamento = [('data', str, None, True), ('horario', str, None, True), ('id_pet', int, ('pet', 'nome'), True), ('id_veterinario', int, ('veterinario', 'nome'), True)]

campos_receita = [('texto', str, None, True), ('id_consulta', int, ('consulta cons', "CONCAT(cons.id, ' - ', cons.data_hora_agendada)"), True)]


def listar_clientes(): listar_registros("cliente", "id, nome, telefone, endereco_completo, cpf_cnpj", order_by="nome")
def listar_pets(): listar_registros("pet", "p.id, p.nome, p.data_nascimento, p.sexo, p.status, c.nome AS cliente, r.nome AS raca", "JOIN cliente c ON p.id_cliente = c.id JOIN raca r ON p.id_raca = r.id", order_by="p.nome")
def listar_veterinarios(): listar_registros("veterinario", "id, nome, especialidade, crmv", order_by="nome")
def listar_funcionarios(): listar_registros("funcionario", "id, nome, telefone, cpf", order_by="nome")
def listar_consultas(): listar_registros("consulta", "con.id, con.data_hora_agendada, con.queixa, con.diagnostico, con.status, p.nome AS pet, v.nome AS veterinario", "JOIN pet p ON con.id_pet = p.id JOIN veterinario v ON con.id_veterinario = v.id", order_by="con.data_hora_agendada DESC")
def listar_produtos(): listar_registros("produto", "id, nome, preco, prescricao", order_by="nome")
def listar_faturas(): listar_registros("fatura", "f.id, f.valor_total, f.status, f.data_emissao, c.nome AS cliente", "JOIN cliente c ON f.id_cliente = c.id", order_by="data_emissao DESC")
def listar_itens_fatura(): listar_registros("item_fatura", "it.id, it.id_fatura, p.nome AS produto, it.quantidade", "JOIN produto p ON it.id_produto = p.id", order_by="it.id")
def listar_prescricoes(): listar_registros("prescricao", "pr.id, CONCAT(c.id, ' - ', c.data_hora_agendada) AS consulta, p.nome AS produto", "JOIN consulta c ON pr.id_consulta = c.id JOIN produto p ON pr.id_produto = p.id", order_by="pr.id")
def listar_racas(): listar_registros("raca", "id, nome, especie", order_by="nome")
def listar_tratamentos(): listar_registros("tratamento", "t.id, t.descricao, t.duracao_dias, CONCAT(c.id, ' - ', c.data_hora_agendada) AS consulta", "JOIN consulta c ON t.id_consulta = c.id", order_by="t.id")
def listar_vacinas(): listar_registros("vacina", "v.id, v.nome, v.data_aplicacao, v.lote, p.nome AS pet", "JOIN pet p ON v.id_pet = p.id", order_by="v.data_aplicacao DESC")
def listar_agendamentos(): listar_registros("agendamento", "a.id, a.data, a.horario, p.nome AS pet, v.nome AS veterinario", "JOIN pet p ON a.id_pet = p.id JOIN veterinario v ON a.id_veterinario = v.id", order_by="a.data DESC, a.horario DESC")
def listar_receitas(): listar_registros("receita", "r.id, r.texto, CONCAT(c.id, ' - ', c.data_hora_agendada) AS consulta", "JOIN consulta c ON r.id_consulta = c.id", order_by="r.id")

def menu_gerenciamento_crud(): 
    while True:
        print("\n--- Menu CRUD Principal ---")
        print("1. Clientes")
        print("2. Pets")
        print("3. Veterinários")
        print("4. Funcionários")
        print("5. Consultas")
        print("6. Raças")
        print("7. Tratamentos")
        print("8. Vacinas")
        print("9. Agendamentos")
        print("10. Receitas")
        print("0. Voltar")
        op = input("Escolha: ")
        if op == "1": menu_crud("Cliente", "cliente", campos_cliente, listar_clientes)
        elif op == "2": menu_crud("Pet", "pet", campos_pet, listar_pets)
        elif op == "3": menu_crud("Veterinário", "veterinario", campos_veterinario, listar_veterinarios)
        elif op == "4": menu_crud("Funcionário", "funcionario", campos_funcionario, listar_funcionarios)
        elif op == "5": menu_crud("Consulta", "consulta", campos_consulta, listar_consultas)
        elif op == "6": menu_crud("Raça", "raca", campos_raca, listar_racas)
        elif op == "7": menu_crud("Tratamento", "tratamento", campos_tratamento, listar_tratamentos)
        elif op == "8": menu_crud("Vacina", "vacina", campos_vacina, listar_vacinas)
        elif op == "9": menu_crud("Agendamento", "agendamento", campos_agendamento, listar_agendamentos)
        elif op == "10": menu_crud("Receita", "receita", campos_receita, listar_receitas)
        elif op == "0": break
        else: print("Inválido")


def menu_gerenciamento_extendido():
    while True:
        print("\n--- Menu Extra (Produtos, Faturas, etc.) ---")
        print("1. Produtos")
        print("2. Faturas")
        print("3. Itens de Fatura")
        print("4. Prescrições")
        print("0. Voltar")
        op = input("Escolha: ")
        if op == "1": menu_crud("Produto", "produto", campos_produto, listar_produtos)
        elif op == "2": menu_crud("Fatura", "fatura", campos_fatura, listar_faturas)
        elif op == "3": menu_crud("Item Fatura", "item_fatura", campos_item_fatura, listar_itens_fatura)
        elif op == "4": menu_crud("Prescrição", "prescricao", campos_prescricao, listar_prescricoes)
        elif op == "0": break
        else: print("Inválido")

def menu_principal_completo():
    
    print("\n Sistema Veterinário Completo Iniciado!")
    
    while True:
        print("\n======= MENU COMPLETO =======")
        print("1. CRUD Principal (Clientes, Pets, etc.)")
        print("2. Consultas Avançadas")
        print("3. IA: Sugestão Diagnóstica")
        print("4. Gerenciar Produtos, Faturas, Prescrições")
        print("5. Criar Todas as Tabelas")
        print("6. Carregar Dados Iniciais")
        print("7. Eliminar TODAS as Tabelas")
        print("0. Sair")
        
        opcao = input("Escolha uma opção: ")
     
        if opcao == "1": menu_gerenciamento_crud()
        elif opcao == "2": menu_consultas()
        elif opcao == "3": sugerir_diagnostico_ia()
        elif opcao == "4": menu_gerenciamento_extendido()
        elif opcao == "5": criar_tabelas()
        elif opcao == "6": carregar_dados_iniciais()
        elif opcao == "7": eliminar_todas_tabelas()
        elif opcao == "0": print("Ate logo!"); break
        else: print("Opção inválida")

if __name__ == "__main__":
    menu_principal_completo()