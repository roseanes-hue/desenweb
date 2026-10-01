import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

import streamlit as st
from views import pokedex_view, calculator_view, builder_view, evaluator_view, team_view
from core import (
    init_database,
    register_user,
    authenticate_user,
    verify_email_code,
    resend_verification_code,
)
from core.email_service import send_verification_email, is_configured

st.set_page_config(
    page_title="Kit Pokémon",
    page_icon="🎮",
    layout="wide",
)

init_database()

if "user" not in st.session_state:
    st.session_state.user = None
if "verify_username" not in st.session_state:
    st.session_state.verify_username = None
if "verify_email" not in st.session_state:
    st.session_state.verify_email = None

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

elif st.session_state.verify_username:
    st.title("📧 Verificação de E-mail")
    st.write(f"Enviamos um código de 6 dígitos para **{st.session_state.verify_email}**")
    st.write("Digite o código abaixo para ativar sua conta:")

    with st.form("verify_form"):
        code = st.text_input("Código de Verificação", max_chars=6, placeholder="000000")
        col1, col2 = st.columns(2)
        with col1:
            submitted = st.form_submit_button("Verificar", type="primary")
        with col2:
            resend = st.form_submit_button("Reenviar Código")

        if submitted:
            if code and len(code) == 6:
                success, message = verify_email_code(st.session_state.verify_username, code)
                if success:
                    st.success(message)
                    st.session_state.verify_username = None
                    st.session_state.verify_email = None
                    st.rerun()
                else:
                    st.error(message)
            else:
                st.warning("Digite o código de 6 dígitos.")

        if resend:
            success, message, new_code = resend_verification_code(st.session_state.verify_username)
            if success and new_code:
                email_sent, email_msg = send_verification_email(
                    st.session_state.verify_email,
                    st.session_state.verify_username,
                    new_code
                )
                if email_sent:
                    st.success(message)
                else:
                    st.error(f"{message} Mas falha ao enviar e-mail: {email_msg}")
            else:
                st.error(message)

    if st.button("← Voltar ao Login"):
        st.session_state.verify_username = None
        st.session_state.verify_email = None
        st.rerun()

else:
    st.title("💻 Acesso ao PC do Treinador")
    st.write("Faça login ou cadastre-se para acessar o Kit Pokémon.")

    if not is_configured():
        st.warning("⚠️ SMTP não configurado. O envio de e-mail de verificação não funcionará até configurar o arquivo `.env`.")

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
                        success, message, verification_code = register_user(username, email, password)
                        if success:
                            email_sent, email_msg = send_verification_email(email, username, verification_code)
                            if email_sent:
                                st.session_state.verify_username = username
                                st.session_state.verify_email = email
                                st.success(message)
                                st.rerun()
                            else:
                                st.error(f"Cadastro criado, mas falha ao enviar e-mail: {email_msg}")
                        else:
                            st.error(message)
                else:
                    st.warning("Preencha todos os campos.")