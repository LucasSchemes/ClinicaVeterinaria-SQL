class CrudBase:
    def __init__(self, conexao, cursor):
        self.conn = conexao
        self.cursor = cursor

        # Mapeamento: tabela no banco -> nome bonito
        self.tabelas = {
            "tb_especie": "Espécies",
            "tb_raca": "Raças",
            "tb_cliente": "Clientes",
            "tb_funcionario": "Funcionários",
            "tb_pet": "Pets",
            "tb_agendamento": "Agendamentos",
            "tb_consulta": "Consultas",
            "tb_produto": "Produtos",
            "tb_fatura": "Faturas",
            "tb_item_fatura": "Itens de Fatura",
            "tb_prescricao": "Prescrições"
        }

    def menu_crud(self):
        while True:
            print("\n" + "=" * 50)
            print("🔧  Menu de Gerenciamento de Registros 🔧".center(50))
            print("=" * 50)

            for i, (tabela, nome_bonito) in enumerate(self.tabelas.items(), 1):
                print(f"{i}. {nome_bonito}")

            print("0. Voltar ao menu principal")
            print("=" * 50)

            try:
                opcao = int(input("Escolha uma tabela para gerenciar: "))
                if opcao == 0:
                    break
                elif 1 <= opcao <= len(self.tabelas):
                    tabela_selecionada = list(self.tabelas.keys())[opcao - 1]
                    self.menu_operacoes(tabela_selecionada, self.tabelas[tabela_selecionada])
                else:
                    print("❌ Opção inválida. Tente novamente.")
            except ValueError:
                print("❌ Por favor, digite um número válido.")

    def menu_operacoes(self, tabela, nome_bonito):
        while True:
            print("\n" + "=" * 50)
            print(f"📋  Operações para {nome_bonito} 📋".center(50))
            print("=" * 50)
            print("1. Inserir")
            print("2. Listar")
            print("3. Atualizar")
            print("4. Deletar")
            print("0. Voltar")
            print("=" * 50)

            opcao = input("Escolha uma operação: ")

            if opcao == '1':
                self.inserir(tabela)
            elif opcao == '2':
                self.listar(tabela)
            elif opcao == '3':
                self.atualizar(tabela)
            elif opcao == '4':
                self.deletar(tabela)
            elif opcao == '0':
                break
            else:
                print("❌ Opção inválida.")

    def listar(self, tabela):
        try:
            self.cursor.execute(f"SELECT * FROM {tabela}")
            linhas = self.cursor.fetchall()
            colunas = [desc[0] for desc in self.cursor.description]

            print("\n--- Registros encontrados ---")
            print(" | ".join(colunas))
            for linha in linhas:
                print(" | ".join(str(campo) for campo in linha))
        except Exception as e:
            print(f"❌ Erro ao listar: {e}")

    def inserir(self, tabela):
        try:
            self.cursor.execute(f"DESCRIBE {tabela}")
            colunas = self.cursor.fetchall()
            campos = []
            valores = []

            for coluna in colunas:
                nome = coluna[0]
                if 'auto_increment' in coluna[5].lower():
                    continue
                valor = input(f"{nome}: ")
                campos.append(nome)
                valores.append(valor if valor else None)

            campos_str = ", ".join(campos)
            valores_str = ", ".join(["%s"] * len(valores))
            sql = f"INSERT INTO {tabela} ({campos_str}) VALUES ({valores_str})"

            self.cursor.execute(sql, valores)
            self.conn.commit()
            print("✅ Registro inserido com sucesso!")
        except Exception as e:
            print(f"❌ Erro ao inserir: {e}")

    def atualizar(self, tabela):
        try:
            id_coluna = self.obter_coluna_id(tabela)
            id_valor = input(f"Informe o valor de {id_coluna} do registro a ser atualizado: ")

            self.cursor.execute(f"DESCRIBE {tabela}")
            colunas = self.cursor.fetchall()

            updates = []
            valores = []

            for coluna in colunas:
                nome = coluna[0]
                if nome == id_coluna:
                    continue
                novo_valor = input(f"Novo valor para {nome} (pressione Enter para manter): ")
                if novo_valor:
                    updates.append(f"{nome} = %s")
                    valores.append(novo_valor)

            if not updates:
                print("⚠️ Nenhuma alteração feita.")
                return

            valores.append(id_valor)
            sql = f"UPDATE {tabela} SET {', '.join(updates)} WHERE {id_coluna} = %s"
            self.cursor.execute(sql, valores)
            self.conn.commit()
            print("✅ Registro atualizado com sucesso!")
        except Exception as e:
            print(f"❌ Erro ao atualizar: {e}")

    def deletar(self, tabela):
        try:
            id_coluna = self.obter_coluna_id(tabela)
            id_valor = input(f"Informe o valor de {id_coluna} do registro a ser deletado: ")
            sql = f"DELETE FROM {tabela} WHERE {id_coluna} = %s"
            self.cursor.execute(sql, (id_valor,))
            self.conn.commit()
            print("✅ Registro deletado com sucesso!")
        except Exception as e:
            print(f"❌ Erro ao deletar: {e}")

    def obter_coluna_id(self, tabela):
        self.cursor.execute(f"DESCRIBE {tabela}")
        for coluna in self.cursor.fetchall():
            if coluna[0].startswith("id_") and coluna[4] == "PRI":
                return coluna[0]
        return "id"
