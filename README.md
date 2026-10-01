# 🎮 Kit Pokémon em Python — Pokédex, Calculadora de Tipos, Montador de Times e Gerenciador Pessoal

> **Projeto Acadêmico:** Aplicação interativa em **Python 3.10+** com interface **Streamlit**, integrada à **PokéAPI** para busca de dados de Pokémon, cálculo de efetividade de tipos, montagem automática de times com **Algoritmo Guloso** e sistema de autenticação com gerenciamento de time pessoal persistido em **SQLite**.

🔗 **Repositório:** [https://github.com/roseanes-hue/desenweb.git](https://github.com/roseanes-hue/desenweb.git)

---

## 📋 Sobre o Projeto

Este projeto consiste em um **Kit Pokémon** desenvolvido para demonstrar a integração entre uma interface web interativa em **Python (Streamlit)** e a API pública **PokéAPI** (`pokeapi.co`).

A aplicação conta com **cinco módulos principais**: uma **Pokédex** para busca individual de Pokémon com exibição de *sprites* e estatísticas, uma **Calculadora de Tipos** para cálculo de efetividade entre os 18 tipos, um **Montador de Times** que utiliza um algoritmo guloso para recomendar equipes otimizadas, um **Avaliador de Times** para análise de cobertura e sinergia, e um sistema de **Autenticação & Gerenciamento de Time Pessoal** com banco de dados SQLite local.

---

## 🎨 Destaques da Interface & Experiência do Usuário

- 🔍 **Pokédex Interativa:** Busca por nome ou ID com exibição de *sprites*, tipos, atributos e barras de estatísticas.
- ⚔️ **Calculadora de Tipos:** Seleção interativa de tipos atacantes e defensores com cálculo instantâneo de multiplicadores ($0\times$, $0,25\times$, $0,5\times$, $1\times$, $2\times$, $4\times$).
- 🧠 **Montador de Times Automático:** Algoritmo guloso que monta equipes com até 6 membros, suportando posições travadas pelo usuário e filtro por tipo.
- 📊 **Avaliador de Times:** Análise de sinergia defensiva, cobertura ofensiva contra todos os 18 tipos e índice de tanque ($\text{HP} + \text{Def} + \text{SpDef}$).
- 🔐 **Autenticação "PC do Treinador":** Tela de login/cadastro com abas, senhas criptografadas (SHA-256), sessão via `st.session_state`.
- 🧑‍💻 **Meu Time Pokémon:** Área exclusiva para usuários logados gerenciarem time pessoal de até 6 Pokémon com sprites oficiais da PokéAPI, adição/remoção individual e limpeza total.

---

## 🛠️ Tecnologias Utilizadas

### **Frontend (Streamlit)**
- **Streamlit** — Framework Python para criação de interfaces web interativas e reativas.
- **st.session_state** — Gerenciamento de estado entre interações e painéis (inclui sessão de usuário autenticado).
- **st.sidebar** — Navegação lateral para alternância entre Pokédex, Calculadora, Montador, Avaliador e Meu Time.
- **st.tabs** — Abas para Login e Cadastro na tela de autenticação.
- **st.form** — Formulários validados para entrada de dados.

### **Backend (Python 3)**
- **Python 3.10+** — Linguagem principal de desenvolvimento.
- **Requests** — Biblioteca para requisições HTTP à PokéAPI.
- **Cache JSON** — Persistência local de dados para evitar chamadas redundantes à API.
- **Algoritmo Guloso** — Estratégia de otimização para montagem automática de times Pokémon.
- **SQLite (nativo)** — Banco de dados local para usuários e times pessoais (`pokemon_app.db`).
- **hashlib (nativo)** — Criptografia SHA-256 de senhas antes de armazenar.

---

## 📁 Estrutura de Arquivos do Projeto

```text
desenweb/
├── kit_pokemon/                    # Projeto Principal
│   ├── core/                       # Backend / Regras de Negócio
│   │   ├── __init__.py
│   │   ├── pokeapi_client.py       # Cliente da PokéAPI com cache local
│   │   ├── type_chart.py           # Tabela de efetividade entre tipos
│   │   ├── evaluator.py            # Avaliador estratégico (cobertura, sinergia)
│   │   ├── team_builder.py         # Montador de times (Algoritmo Guloso)
│   │   └── database.py             # SQLite: users, teams, auth, CRUD
│   │
│   ├── data/
│   │   ├── cache/                  # Cache local de Pokémon (auto-gerado)
│   │   └── type_matrix.json        # Matriz completa de relações entre os 18 tipos
│   │
│   ├── views/                      # Frontend / Interfaces Streamlit
│   │   ├── pokedex_view.py         # Painel Pokédex (busca, sprites, stats)
│   │   ├── calculator_view.py      # Painel Calculadora de Tipos
│   │   ├── builder_view.py         # Painel Montador de Times
│   │   ├── evaluator_view.py       # Painel Avaliador de Times
│   │   └── team_view.py            # Painel Meu Time (autenticado)
│   │
│   ├── app_cli.py                  # Ponto de entrada CLI (terminal)
│   ├── app_web.py                  # Ponto de entrada Web (Streamlit)
│   ├── requirements.txt            # Dependências (requests, streamlit)
│   └── pokemon_app.db              # Banco SQLite (criado em runtime)
│
├── api/                            # API Backend - Projeto Separado (FastAPI + SQLite)
├── frontend/                       # Frontend React - Projeto Separado (Vite + Tailwind)
├── doc/                            # Documentação técnica
│   ├── escopo_projeto_kit_pokemon.md
│   ├── plano_kit_pokemon.md
│   ├── plano_sistema_leads.md      # Doc. do projeto separado (Sistema de Leads)
│   └── plano_landingpage_nodejs.md # Doc. do projeto separado (Landing Page Node.js)
│
└── README.md                       # Este arquivo
```

---

## ⚡ Guia Rápido: Como Executar o Projeto

### **1. Clonar o Repositório**

```bash
git clone https://github.com/roseanes-hue/desenweb.git
cd desenweb/kit_pokemon
```

---

### **2. Instalar as Dependências (Primeira Execução)**

```bash
python -m venv .venv
# No Windows:
.venv\Scripts\pip install -r requirements.txt
# No Linux/Mac:
# source .venv/bin/activate && pip install -r requirements.txt
```

---

### 🚀 **3. Executar em Modo Web (Recomendado)**

```bash
# No Windows:
.venv\Scripts\streamlit run app_web.py

# No Linux/Mac:
# .venv/bin/streamlit run app_web.py
```

> O Streamlit iniciará o servidor na porta **8501** (`http://localhost:8501`).

---

### 💻 **4. Executar em Modo CLI (Terminal)**

```bash
# No Windows:
.venv\Scripts\python app_cli.py

# No Linux/Mac:
# .venv/bin/python app_cli.py
```

> Menu interativo via terminal para testes rápidos da Pokédex e Calculadora.

---

## 📊 Arquitetura do Sistema

```
+-----------------------------------------------------------------------+
|                        FRONTEND (Interface)                           |
|                                                                       |
|   [ Terminal CLI: app_cli.py ]       [ Web App: app_web.py ]        |
|                                             │                         |
|                                  ┌──────────┴──────────┐              |
|                                  ▼                     ▼              |
|                           pokedex_view          builder_view          |
|                                  ▼                     ▼              |
|                           calculator_view       evaluator_view       |
|                                  ▼                     ▼              |
|                              team_view (autenticado)                |
+-----------------------------------┼-----------------------------------+
                                    │
+-----------------------------------┼-----------------------------------+
|                                   ▼                                   |
|                        BACKEND (Core / Regras)                        |
|                                                                       |
|   pokeapi_client.py  ◄─►  type_chart.py  ◄─►  team_builder.py        |
|          │                      │                      │              |
|          ▼                      ▼                      ▼              |
|      [ PokéAPI ]         [ type_matrix ]          [ evaluator ]       |
|                                                                       |
|   database.py (SQLite)                                                |
|   ├─ users (id, username, email, password_hash)                      |
|   └─ teams (id, user_id, pokemon_name, sprite_url, stats, created)   |
+-----------------------------------------------------------------------+
```

> **Regra de Ouro:** A camada de Frontend atua apenas na captura de entradas e renderização visual. Toda a lógica de requisições HTTP, cálculo de multiplicadores, algoritmo guloso e persistência reside no Backend (`core/`).

---

## 🛑 Diretrizes de Qualidade

- **Tratamento de Exceções:** Erros de entrada do usuário (nomes incorretos de Pokémon) são tratados com mensagens informativas na interface.
- **Tempo de Execução:** O algoritmo guloso entrega a recomendação completa do time em tempo $< 2$ segundos.
- **Segurança:** Senhas armazenadas apenas como hash SHA-256 via `hashlib` nativo, nunca em texto plano.
- **Sessão:** Estado de autenticação gerenciado via `st.session_state.user` com logout disponível.
- **Crédito de Autoria:** Rodapé da aplicação e cabeçalho da documentação atribuem a criação do projeto a **Roseane Vilela de Sousa**.

---

## 📜 Licença e Créditos

Projeto acadêmico desenvolvido por **Roseane Vilela de Sousa**.

🔗 Repositório: [https://github.com/roseanes-hue/desenweb.git](https://github.com/roseanes-hue/desenweb.git)