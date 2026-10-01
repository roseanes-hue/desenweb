# Documento de Escopo do Projeto: Kit Pokémon em Python

**Versão:** 1.1  
**Data:** Setembro de 2026  
**Status:** Aprovado para Desenvolvimento  
**Linguagem Principal:** Python 3.10+  
**Interface:** Terminal (CLI) + Web (Streamlit)  

---

## 1. Resumo Executivo

O **Kit Pokémon** é uma aplicação modular projetada para entusiastas e jogadores de Pokémon que buscam desde consultas rápidas de dados até auxílio estratégico avançado na formação de equipes. O desenvolvimento adota uma abordagem **incremental em 5 camadas**, garantindo a entrega rápida de um Produto Mínimo Viável (MVP) totalmente funcional na primeira fase, agregando complexidade lógica, visual e de persistência progressivamente.

---

## 2. Visão Geral e Objetivos do Projeto

### 2.1 Objetivo Geral
Desenvolver um conjunto de ferramentas integradas em Python para consulta de dados da PokéAPI, cálculo de interações elementares, recomendação automatizada de times equilibrados usando inteligência algorítmica, e gerenciamento pessoal de times com autenticação de usuários.

### 2.2 Objetivos Específicos
* **Consumo de API Externa:** Integrar com a PokéAPI RESTful para dados atualizados e dinâmicos sem custo de autenticação.
* **Lógica Puramente Local:** Implementar estruturas de dados e algoritmos eficientes para cálculos offline (tabela de tipos e algoritmo de recomendação).
* **Interface Amigável:** Prover visualização interativa e responsiva via Streamlit.
* **Otimização Estratégica:** Implementar um algoritmo guloso (*Greedy Algorithm*) capaz de ponderar múltiplos fatores de sinergia e propor equipes equilibradas em tempo quase instantâneo.
* **Persistência e Personalização:** Permitir que usuários criem contas, autentiquem-se e gerenciem seus próprios times Pokémon persistidos em banco de dados local.

---

## 3. Arquitetura Incremental por Camadas

```
+-------------------------------------------------------------+
| Camada 5: Autenticação & Gerenciamento de Time Pessoal      |
+-------------------------------------------------------------+
                              ▲
                              │
+-------------------------------------------------------------+
| Camada 4: Montador de Time (Algoritmo Guloso & Sinergia)    |
+-------------------------------------------------------------+
                              ▲
                              │
+-------------------------------------------------------------+
| Camada 3: Interface Web Interativa (Streamlit Dashboard)    |
+-------------------------------------------------------------+
                              ▲
                              │
+-------------------------------------------------------------+
| Camada 2: Calculadora de Efetividade de Tipos (Offline)     |
+-------------------------------------------------------------+
                              ▲
                              │
+-------------------------------------------------------------+
| Camada 1: Pokédex de Consulta CLI (MVP Base - PokéAPI)      |
+-------------------------------------------------------------+
```

---

## 4. Detalhamento Funcional das Camadas

### Camada 1 — Pokédex de Consulta (MVP / Base)
* **Escopo:** Interface em Linha de Comando (CLI) para busca individualizada.
* **Entrada do Usuário:** Nome em inglês (ex: `gengar`) ou número da ID nacional (ex: `94`).
* **Integração:** Consumo do endpoint publicamente acessível da PokéAPI (`https://pokeapi.co/api/v2/pokemon/{id_ou_nome}`).
* **Saída e Exibição:**
  * **Informações Básicas:** Nome, ID, Tipos (primário e secundário).
  * **Dimensões:** Altura (metros) e Peso (quilogramas).
  * **Estatísticas de Base (*Base Stats*):** HP, Attack, Defense, Special Attack, Special Defense, Speed, e Total.
  * **Visual:** URL e download/exibição do sprite oficial do Pokémon.

---

### Camada 2 — Calculadora de Efetividade de Tipos
* **Escopo:** Módulo lógico offline para análise de interações elementares entre tipos.
* **Implementação:** Matriz de tipos estruturada localmente através de dicionários Python (`dict`), dispensando chamadas de rede.
* **Funcionalidades:**
  * Seleção de **Tipo Atacante** e **Tipo Defensor** (simples ou duplo).
  * Cálculo exato do multiplicador de dano final:
    * **Super Efetivo ($2\times$ ou $4\times$):** Dano amplificado.
    * **Dano Normal ($1\times$):** Dano padrão.
    * **Pouco Efetivo ($0,5\times$ ou $0,25\times$):** Dano reduzido.
    * **Sem Efeito ($0\times$):** Imunidade total.
  * **Utilidade:** Serve tanto como ferramenta standalone quanto como subsistema para o avaliador da Camada 4.

---

### Camada 3 — Interface Web Interativa (Streamlit)
* **Escopo:** Migração visual do terminal para um painel web moderno, ágil e intuitivo.
* **Tecnologia:** Streamlit (desenvolvimento de aplicações web orientadas a dados puramente em Python).
* **Recursos de Interface:**
  * Barra lateral de navegação entre as ferramentas (Pokédex, Calculadora, Montador, Meu Time).
  * Campo de pesquisa inteligente com autocompletar e validação imediata.
  * Renderização visual de estatísticas em barras coloridas ou gráficos de radar.
  * Exibição em grid dos *sprites* e imagens oficiais em alta resolução.
  * Tela de login/cadastro com tema "Acesso ao PC do Treinador" (quando não autenticado).

---

### Camada 4 — Montador de Time Inteligente (*Team Builder*)
* **Escopo:** Sistema avançado de recomendação para montagem automática de equipes estratégicas compostas por 6 Pokémon.

#### 4.1 Pilares da Avaliação Estratégica
1. **Cobertura Ofensiva:** O time é pontuado positivamente se conseguir aplicar dano super efetivo ($2\times$ ou $4\times$) em todas as 18 combinações de tipos existentes no jogo.
2. **Sinergia Defensiva:** O algoritmo penaliza formações que compartilham fraquezas acumuladas sem ter parceiros na equipe que as resistam ou anulem.
3. **Função de Tanque (*Sustentabilidade*):** Identificação de Pokémon com pontuação alta combinada nas métricas de $\text{HP} + \text{Defesa} + \text{Defesa Especial}$.

#### 4.2 Modos de Operação do Usuário
* **Modo 100% Sugerido:** O sistema gera a equipe completa de 6 integrantes a partir do zero.
* **Modo Posições Travadas (Misto):** O usuário fixa de 1 a 5 Pokémon de sua preferência, e o algoritmo preenche os slots restantes garantindo a melhor cobertura para o grupo.
* **Modo Preferência por Tipo:** O usuário define um tipo foco (ex: *Fada* ou *Dragão*), e o algoritmo prioriza ou exige a inclusão de integrantes desse tipo.

#### 4.3 Abordagem Algorítmica: Algoritmo Guloso (*Greedy Algorithm*)
* Em vez de calcular todas as combinações possíveis de $1000+$ Pokémon (o que seria computacionalmente inviável para execução rápida em tempo real), o sistema adiciona os membros **um por um**.
* A cada etapa, o algoritmo testa os candidatos disponíveis e escolhe aquele que entrega o **maior ganho marginal relativo** à equipe atual (melhor complemento defensivo/ofensivo).
* **Desempenho Esperado:** Tempo de execução $< 2$ segundos no computador do usuário.

---

### Camada 5 — Autenticação & Gerenciamento de Time Pessoal
* **Escopo:** Sistema de controle de acesso e persistência de times pessoais por usuário.

#### 5.1 Autenticação de Usuário
* **Tela de Acesso:** Tema "Acesso ao PC do Treinador" com duas abas: "Entrar no PC" e "Cadastrar Novo Treinador".
* **Cadastro:** Nome de usuário único, email único, senha (mínimo 6 caracteres, confirmação).
* **Login:** Nome de usuário e senha.
* **Segurança:** Senhas criptografadas com SHA-256 via `hashlib` nativo antes de armazenar no banco.
* **Sessão:** Gerenciada via `st.session_state.user` com logout disponível na barra lateral.

#### 5.2 Gerenciamento de Time Pessoal ("Meu Time")
* **Acesso:** Nova área no menu lateral disponível apenas para usuários autenticados.
* **Capacidade:** Até 6 Pokémon por usuário.
* **Funcionalidades:**
  * Busca de Pokémon por nome ou ID via PokéAPI com preview (sprite, tipos, stats).
  * Adição ao time com validação de limite (máx. 6).
  * Visualização do time em cards com sprite oficial e estatísticas base.
  * Remoção individual de Pokémon do time.
  * Limpeza completa do time.
* **Persistência:** Dados salvos em SQLite local (`pokemon_app.db`) com tabelas `users` e `teams`.
* **Bloqueio:** Usuários não autenticados veem apenas a tela de login; todas as funcionalidades ficam bloqueadas.

---

## 5. Backlog e Extensões Opcionais

Recursos secundários a serem desenvolvidos exclusivamente após a validação completa e estável das 5 camadas principais:

| Funcionalidade | Descrição | Complexidade |
| :--- | :--- | :--- |
| **Sugestão de Golpes via STAB** | Recomendação automatizada de movimentos com bônus do mesmo tipo (*Same Type Attack Bonus*). | Média |
| **Curadoria de Habilidades (*Abilities*)** | Mapeamento e atribuição de pesos para habilidades passivas relevantes em batalha (ex: *Levitate*, *Intimidate*). | Alta (Requer curadoria de dados local) |
| **Exportação de Time** | Exportar a equipe gerada no formato padrão *Showdown Text* para uso em simuladores externos. | Baixa |
| **Compartilhamento de Time** | Gerar link/código para compartilhar time pessoal com outros usuários. | Média |
| **Histórico de Times** | Versionamento e histórico de alterações no time pessoal. | Média |

---

## 6. Requisitos do Sistema

### 6.1 Requisitos Funcionais (RF)
* **RF01:** O sistema deve buscar informações de Pokémon diretamente da PokéAPI.
* **RF02:** O sistema deve calcular o multiplicador exato de dano entre tipos primários e secundários.
* **RF03:** A interface web deve permitir alternar livremente entre as funcionalidades sem reiniciar o estado da aplicação.
* **RF04:** O montador de time deve permitir ao usuário travar membros específicos do time antes de executar a recomendação.
* **RF05:** O montador deve exibir o relatório explicativo com os pontos fortes e fraquezas do time gerado.
* **RF06:** O sistema deve permitir cadastro de usuários com username, email e senha criptografada.
* **RF07:** O sistema deve autenticar usuários e manter sessão ativa via `st.session_state`.
* **RF08:** Usuários autenticados devem poder gerenciar time pessoal de até 6 Pokémon com sprites e stats da PokéAPI.
* **RF09:** Usuários não autenticados devem ser bloqueados de acessar qualquer funcionalidade além do login/cadastro.

### 6.2 Requisitos Não-Funcionais (RNF)
* **RNF01:** A aplicação deve ser escrita integralmente em Python 3.10+.
* **RNF02:** O algoritmo de recomendação não deve levar mais de 3 segundos para responder.
* **RNF03:** As requisições à API devem implementar mecanismo de *caching* em memória/disco para otimizar tempo de resposta e evitar sobrecarga na PokéAPI.
* **RNF04:** A interface web deve ser responsiva e funcional em navegação desktop.
* **RNF05:** Senhas devem ser armazenadas apenas como hash SHA-256, nunca em texto plano.
* **RNF06:** Banco de dados SQLite deve ser criado automaticamente na primeira execução.

---

## 7. Estrutura Proposta do Projeto

```
kit_pokemon/
│
├── core/
│   ├── __init__.py
│   ├── pokeapi_client.py    # Gerenciador de requisições e cache da PokéAPI
│   ├── type_chart.py        # Matriz e funções de efetividade de tipos
│   ├── evaluator.py         # Métricas de cobertura defensiva e ofensiva
│   ├── team_builder.py      # Lógica do algoritmo guloso para recomendação
│   └── database.py          # SQLite: users, teams, auth, CRUD
│
├── data/
│   ├── cache/               # Cache local de Pokémon (auto-gerado)
│   └── type_matrix.json     # Mapeamento local das interações de tipos
│
├── views/
│   ├── pokedex_view.py      # Renderização do painel da Pokédex no Streamlit
│   ├── calculator_view.py   # Renderização da calculadora no Streamlit
│   ├── builder_view.py      # Renderização do montador no Streamlit
│   ├── evaluator_view.py    # Renderização do avaliador de times
│   └── team_view.py         # Renderização do gerenciamento de time pessoal
│
├── app_cli.py               # Interface de Linha de Comando (Camadas 1 e 2)
├── app_web.py               # Ponto de entrada da aplicação Streamlit (Camadas 3, 4, 5)
├── requirements.txt         # Dependências do projeto (requests, streamlit, etc.)
├── pokemon_app.db           # Banco SQLite (criado em runtime)
└── README.md                # Documentação técnica de instalação e uso
```

---

## 8. Cronograma Estimado de Desenvolvimento

```
[Semana 1] ─── Camada 1: Pokédex CLI + Consumo da PokéAPI
[Semana 2] ─── Camada 2: Calculadora de Tipos & Matriz Local
[Semana 3] ─── Camada 3: Interface Web com Streamlit
[Semana 4] ─── Camada 4: Algoritmo Guloso do Montador de Time
[Semana 5] ─── Camada 5: Autenticação, SQLite & Gerenciamento de Time Pessoal
[Semana 6] ─── Polimento, Caching & Extensões Opcionais
```