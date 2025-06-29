
class gerencia_registros:
    def __init__(self, conexao, cursor):
        self.conn = conexao
        self.cursor = cursor

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

        self.chaves_estrangeiras = {
            'tb_pet': {
                'id_cli_fkc': ('tb_cliente', 'id_cli', 'nome'),
                'id_raca_fkc': ('tb_raca', 'id_raca', 'nome_raca')
            },
            'tb_agendamento': {
                'fk_id_pet': ('tb_pet', 'id_pet', 'nome'),
                'fk_id_fun': ('tb_funcionario', 'id_fun', 'nome')
            },
            'tb_consulta': {
                'id_pet_fkc': ('tb_pet', 'id_pet', 'nome'),
                'id_fun_fkc': ('tb_funcionario', 'id_fun', 'nome'),
                'id_age_fkc': ('tb_agendamento', 'id_age', 'id_age')
            },
            'tb_fatura': {
                'id_cli_fkc': ('tb_cliente', 'id_cli', 'nome'),
                'id_con_fkc': ('tb_consulta', 'id_con', 'id_con')
            },
            'tb_item_fatura': {
                'id_fat_fkc': ('tb_fatura', 'id_fat', 'id_fat'),
                'id_prod_fkc': ('tb_produto', 'id_prod', 'nome')
            },
            'tb_prescricao': {
                'id_con_fkc': ('tb_consulta', 'id_con', 'id_con'),
                'id_prod_fkc': ('tb_produto', 'id_prod', 'nome')
            },
            'tb_raca': {
                'id_esp_fkc': ('tb_especie', 'id_esp', 'nome_especie')
            }
        }

    def listar_opcoes(self, tabela, id_coluna, nome_coluna):
        try:
            self.cursor.execute(f"SELECT {id_coluna}, {nome_coluna} FROM {tabela}")
            opcoes = self.cursor.fetchall()
            if not opcoes:
                print(f"\n⚠️ Nenhum registro encontrado em {tabela}.")
                return
            print(f"\n--- Opções disponíveis em {tabela} ---")
            for opcao in opcoes:
                print(f"{opcao[0]} - {opcao[1]}")
        except Exception as e:
            print(f"❌ Erro ao listar opções: {e}")

    def buscar_id_por_nome(self, tabela, id_coluna, nome_coluna, nome_busca):
        try:
            self.cursor.execute(f"SELECT {id_coluna} FROM {tabela} WHERE {nome_coluna} = %s", (nome_busca,))
            resultado = self.cursor.fetchone()
            if resultado:
                return resultado[0]
            else:
                print("❌ Registro não encontrado.")
                return None
        except Exception as e:
            print(f"❌ Erro ao buscar ID: {e}")
            return None

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

                if tabela in self.chaves_estrangeiras and nome in self.chaves_estrangeiras[tabela]:
                    ref_tabela, ref_id, ref_nome = self.chaves_estrangeiras[tabela][nome]
                    self.listar_opcoes(ref_tabela, ref_id, ref_nome)
                    valor = input(f"{nome} (ID): ")
                else:
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
            self.listar(tabela)
            chaves_primarias = self.obter_chaves_primarias(tabela)
            condicoes = []
            valores_condicao = []

            for chave in chaves_primarias:
                valor = input(f"Informe o valor de {chave} do registro a ser atualizado: ")
                condicoes.append(f"{chave} = %s")
                valores_condicao.append(valor)

            if not self.registro_existe(tabela, chaves_primarias, valores_condicao):
                print("❌ Registro não encontrado. Atualização cancelada.")
                return

            self.cursor.execute(f"DESCRIBE {tabela}")
            colunas = self.cursor.fetchall()
            updates = []
            valores_novos = []

            for coluna in colunas:
                nome = coluna[0]
                if nome in chaves_primarias:
                    continue
                novo_valor = input(f"Novo valor para {nome} (pressione Enter para manter): ")
                if novo_valor:
                    updates.append(f"{nome} = %s")
                    valores_novos.append(novo_valor)

            if not updates:
                print("⚠️ Nenhuma alteração feita.")
                return

            sql = f"UPDATE {tabela} SET {', '.join(updates)} WHERE {' AND '.join(condicoes)}"
            self.cursor.execute(sql, valores_novos + valores_condicao)
            self.conn.commit()
            print("✅ Registro atualizado com sucesso!")
        except Exception as e:
            print(f"❌ Erro ao atualizar: {e}")

    def deletar(self, tabela):
        try:
            self.listar(tabela)
            chaves_primarias = self.obter_chaves_primarias(tabela)
            condicoes = []
            valores_condicao = []

            for chave in chaves_primarias:
                valor = input(f"Informe o valor de {chave} do registro a ser deletado: ")
                condicoes.append(f"{chave} = %s")
                valores_condicao.append(valor)

            if not self.registro_existe(tabela, chaves_primarias, valores_condicao):
                print("❌ Registro não encontrado. Exclusão cancelada.")
                return

            sql = f"DELETE FROM {tabela} WHERE {' AND '.join(condicoes)}"
            self.cursor.execute(sql, valores_condicao)
            self.conn.commit()
            print("✅ Registro deletado com sucesso!")
        except Exception as e:
            print(f"❌ Erro ao deletar: {e}")

    def obter_chaves_primarias(self, tabela):
        self.cursor.execute(f"DESCRIBE {tabela}")
        return [coluna[0] for coluna in self.cursor.fetchall() if coluna[3] == 'PRI']

    def registro_existe(self, tabela, chaves_primarias, valores):
        try:
            condicoes = [f"{chave} = %s" for chave in chaves_primarias]
            sql = f"SELECT COUNT(*) FROM {tabela} WHERE {' AND '.join(condicoes)}"
            self.cursor.execute(sql, valores)
            return self.cursor.fetchone()[0] > 0
        except Exception as e:
            print(f"❌ Erro ao verificar existência: {e}")
            return False
