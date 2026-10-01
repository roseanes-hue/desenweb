# Plano de Execução do Projeto: Kit Pokémon em Python

**Criadora do Projeto:** Roseane Vilela de Sousa
**Linguagem Principal:** Python 3.10+
**Arquitetura:** Modular desacoplada em Backend (`core/`) e Frontend (`views/`, `app_cli.py`, `app_web.py`)

---

## 1. Visão Geral e Arquitetura do Sistema

Este documento fornece as diretrizes e o roteiro de desenvolvimento para o **Open Code** programar o sistema **Kit Pokémon**, respeitando a separação entre backend e frontend e a pilha de tecnologias já estabelecidas.

### Fluxo de Comunicação entre Camadas

```
+-----------------------------------------------------------------------+
|                        FRONTEND (Interface)                           |
|                                                                       |
|   [ Terminal CLI: app_cli.py ]       [ Web App: app_web.py ]        |
|                                             │                         |
|                                  ┌──────────┴──────────┐              |
|                                  ▼                     ▼              |
|                           pokedex_view          builder_view          |
+--------------------------------──┼─────────────────────┼--------------+
│ (Chamadas diretas)  │
+--------------------------------──┼─────────────────────┼--------------+
|                                  ▼                     ▼              |
|                        BACKEND (Core / Regras)                        |
|                                                                       |
|   pokeapi_client.py  ◄─►  type_chart.py  ◄─►  team_builder.py        |
|          │                      │                      │              |
|          ▼                      ▼                      ▼              |
|      [ PokéAPI ]         [ type_matrix ]          [ evaluator ]       |
+-----------------------------------------------------------------------+
```

> **Regra de Ouro:** A camada de Frontend deve atuar apenas na captura de entradas e renderização de elementos visuais. Toda a lógica de requisição HTTP, cálculo de multiplicadores e execução de algoritmo guloso deve residir no Backend (`core/`).

---

## 2. Divisão de Responsabilidades Técnicas

### 2.1 Backend (`core/` & `data/`)

* **Cliente de API e Cache (`core/pokeapi_client.py`)**: Responsável pelas requisições HTTP (`requests`) para a PokéAPI (`pokeapi.co`). Deve gerenciar erros de conexão e manter um repositório local em cache JSON para evitar chamadas redundantes.
* **Tabela de Tipos (`core/type_chart.py` & `data/type_matrix.json`)**: Estrutura local com as relações entre os 18 tipos de Pokémon. Fornece funções puras para calcular multiplicadores de dano ($0\times$, $0,25\times$, $0,5\times$, $1\times$, $2\times$, $4\times$).
* **Avaliador Estratégico (`core/evaluator.py`)**: Processa métricas de cobertura de fraquezas, sinergia defensiva e cálculo do índice de tanque ($\text{HP} + \text{Def} + \text{SpDef}$).
* **Recomendador de Time (`core/team_builder.py`)**: Implementa o **Algoritmo Guloso (*Greedy Algorithm*)**, permitindo montagem 100% automática, montagem com posições travadas pelo usuário ou filtro por tipo.

### 2.2 Frontend (`views/`, `app_cli.py`, `app_web.py`)

* **Interface de Linha de Comando (`app_cli.py`)**: Execução via terminal para testes rápidos das Camadas 1 e 2.
* **Painel Pokédex (`views/pokedex_view.py`)**: Interface Streamlit para busca individual, exibição de *sprites*, características físicas e barras de estatísticas.
* **Painel Calculadora (`views/calculator_view.py`)**: Interface Streamlit para seleção interativa de tipos atacantes e defensores.
* **Painel Montador de Times (`views/builder_view.py`)**: Interface Streamlit para travamento de integrantes e exibição da equipe recomendada com relatório de cobertura.
* **Ponto de Entrada Web (`app_web.py`)**: Inicialização do Streamlit, menu lateral (`st.sidebar`) e gerenciamento do estado (`st.session_state`).

---

## 3. Roteiro Passo a Passo para o Open Code

### Passo 1: Estruturação dos Arquivos e Dependências

1. Criar o arquivo `requirements.txt`:

   ```text
   requests>=2.31.0
   streamlit>=1.30.0
   ```

2. Criar a árvore de diretórios do projeto:

   ```text
   kit_pokemon/
   ├── core/
   │   ├── __init__.py
   │   ├── pokeapi_client.py
   │   ├── type_chart.py
   │   ├── evaluator.py
   │   └── team_builder.py
   ├── data/
   │   └── type_matrix.json
   ├── views/
   │   ├── pokedex_view.py
   │   ├── calculator_view.py
   │   └── builder_view.py
   ├── app_cli.py
   ├── app_web.py
   └── requirements.txt
   ```

### Passo 2: Programação do Backend (`core/`)

1. **`core/pokeapi_client.py`**:
   * Criar a classe `PokeAPIClient`.
   * Implementar o método `get_pokemon(name_or_id)` para extrair nome, ID, tipos, atributos e *sprites*.
   * Implementar persistência simples em cache na pasta `data/cache/`.

2. **`core/type_chart.py`**:
   * Preencher `data/type_matrix.json` com a matriz completa de tipos.
   * Criar a função `calculate_effectiveness(attacker_type, defender_types)`.

3. **`core/evaluator.py`**:
   * Criar funções para avaliar se um time possui respostas ofensivas contra todos os 18 tipos e medir sobreposição de fraquezas.

4. **`core/team_builder.py`**:
   * Implementar a classe `GreedyTeamBuilder`, que adiciona sequencialmente o Pokémon que maximiza o ganho de cobertura e sinergia da equipe até completar 6 membros.

### Passo 3: Programação do Frontend e Interfaces

1. **`app_cli.py`**:
   * Implementar menu interativo via terminal para execução rápida da busca Pokédex e da Calculadora.

2. **`views/`**:
   * Construir as funções de renderização para Streamlit em cada arquivo específico da pasta `views/`.

3. **`app_web.py`**:
   * Configurar a navegação por abas/menu lateral e integrar os componentes com as chamadas das funções do `core/`.

---

## 4. Diretrizes de Qualidade e Atribuição

* **Crédito de Autoria:** O rodapé da aplicação Streamlit e o cabeçalho da documentação devem atribuir a criação do projeto a **Roseane Vilela de Sousa**.
* **Tratamento de Exceções:** Tratar erros de entrada do usuário (como nomes incorretos de Pokémon) com mensagens informativas na interface.
* **Tempo de Execução:** O algoritmo guloso deve entregar a recomendação completa do time em tempo $< 2$ segundos.
