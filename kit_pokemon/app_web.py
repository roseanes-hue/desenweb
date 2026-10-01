import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

import streamlit as st
from views import pokedex_view, calculator_view, builder_view, evaluator_view, team_view
from core import init_database, register_user, authenticate_user

st.set_page_config(
    page_title="Kit Pokémon",
    page_icon="🎮",
    layout="wide",
)

init_database()

if "user" not in st.session_state:
    st.session_state.user = None

st.sidebar.title("🎮 Kit Pokémon")
st.sidebar.write("Criado por **Roseane Vilela de Sousa**")
st.sidebar.markdown("---")

if st.session_state.user:
    st.sidebar.write(f"👤 Logado como: **{st.session_state.user['username']}**")
    if st.sidebar.button("🚪 Sair"):
        st.session_state.user = None
        st.rerun()
    st.sidebar.markdown("---")

    pagina = st.sidebar.radio(
        "Navegação",
        ["🔍 Pokédex", "⚔️ Calculadora de Tipos", "🧠 Montador de Times", "📊 Avaliador de Times", "🧑‍💻 Meu Time"],
    )

    st.sidebar.markdown("---")
    st.sidebar.caption("Dados: PokéAPI | Python + Streamlit")

    if pagina == "🔍 Pokédex":
        pokedex_view.render()
    elif pagina == "⚔️ Calculadora de Tipos":
        calculator_view.render()
    elif pagina == "🧠 Montador de Times":
        builder_view.render()
    elif pagina == "📊 Avaliador de Times":
        evaluator_view.render()
    elif pagina == "🧑‍💻 Meu Time":
        team_view.render()
else:
    st.title("💻 Acesso ao PC do Treinador")
    st.write("Faça login ou cadastre-se para acessar o Kit Pokémon.")

    tab_login, tab_register = st.tabs(["🔐 Entrar no PC", "📝 Cadastrar Novo Treinador"])

    with tab_login:
        st.subheader("Login")
        with st.form("login_form"):
            username = st.text_input("Nome de Usuário")
            password = st.text_input("Senha", type="password")
            submitted = st.form_submit_button("Entrar", type="primary")

            if submitted:
                if username and password:
                    success, message, user_data = authenticate_user(username, password)
                    if success:
                        st.session_state.user = user_data
                        st.success(message)
                        st.rerun()
                    else:
                        st.error(message)
                else:
                    st.warning("Preencha todos os campos.")

    with tab_register:
        st.subheader("Cadastro")
        with st.form("register_form"):
            username = st.text_input("Nome de Usuário")
            email = st.text_input("Email")
            password = st.text_input("Senha", type="password")
            password_confirm = st.text_input("Confirmar Senha", type="password")
            submitted = st.form_submit_button("Cadastrar", type="primary")

            if submitted:
                if username and email and password and password_confirm:
                    if password != password_confirm:
                        st.error("As senhas não conferem.")
                    elif len(password) < 6:
                        st.error("A senha deve ter pelo menos 6 caracteres.")
                    else:
                        success, message = register_user(username, email, password)
                        if success:
                            st.success(message)
                        else:
                            st.error(message)
                else:
                    st.warning("Preencha todos os campos.")