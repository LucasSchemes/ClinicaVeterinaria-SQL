# Clínica Veterinária – Sistema de Gestão com SQL e Python

Este projeto integra scripts SQL para modelagem de banco de dados com uma interface em Python para gerência e consultas. A ideia central é facilitar o controle de pacientes, atendimentos e informações veterinárias.

---

##  Estrutura do Repositório

- **`tabelas/`** – Scripts SQL para criação de tabelas (modelagem lógica).
- **`consultas/`** – Scripts SQL com consultas pré-definidas.
- **`.env.example`** – Exemplo de configuração de variáveis de ambiente (como credenciais e conexões com banco).
- **`main.py`** – Script principal para controlar o funcionamento geral da aplicação.
- **`gerenciar.py`** – Interface para operações CRUD sobre entidades (clientes, pacientes, atendimentos etc.).
- **`consultas.py`** – Acesso a relatórios e consultas analíticas pré-definidas via SQL.
- **`ia_module.py`** – Módulo com funcionalidades que envolvem inteligência artificial — possivelmente para recomendações ou automações.
- **Imagens** – Representações visuais do **Modelo Conceitual** e **Modelo Lógico** do banco de dados (ER, DER, diagramas) :contentReference[oaicite:1]{index=1}.

---

##  Objetivo do Projeto

Construir um sistema de gerenciamento para clínica veterinária, que inclui:

- Modelagem lógica e implementação de banco de dados via SQL.
- Execução de consultas úteis para gestão (relatórios financeiros, atendimentos, etc.).
- Interface em Python para facilitar a operação do sistema.
- Uso potencial de inteligência artificial para suporte à decisão ou automação.

---

##  Tecnologias Utilizadas

- **SQL** (PostgreSQL, MySQL ou similar) para modelagem e consultas.
- **Python 3.x** para scripts e interface interativa.
- **Gerenciamento de Ambiente** via `.env` (genérico para conexão com banco).
- Possível uso de bibliotecas de IA em `ia_module.py` (ex.: scikit-learn, SpaCy, TensorFlow, etc.).

---

##  Instalação

1. Clone o repositório:

   ```bash
   git clone https://github.com/LucasSchemes/ClinicaVeterinaria-SQL.git
   cd ClinicaVeterinaria-SQL
   ```
2. Copie o arquivo de ambiente e configure suas variáveis:
   ```bash
   cp .env.example .env
   Edite o .env conforme sua configuração (host, usuário, senha, banco etc.)
   ```
3. Crie o banco de dados e as tabelas usando os scripts SQL:
   ```bash
   Exemplo para PostgreSQL
    psql -U seu_usuario -d seu_banco -f tabelas/create_tables.sql
   ```
4. (Opcional) Popule o banco com dados iniciais, se existirem scripts de inserção no repositório.
5. Instale dependências em Python (se necessário):
   ```bash
   pip install -r requirements.txt
    ```

## Execução 
- Execute o script principal:
```bash
python main.py
```
