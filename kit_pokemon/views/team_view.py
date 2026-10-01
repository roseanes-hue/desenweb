import streamlit as st
import requests
from core import get_user_team, save_team_pokemon, remove_team_pokemon, clear_user_team
from core import render_stat_row, inject_stat_css


POKEAPI_BASE = "https://pokeapi.co/api/v2"


def fetch_pokemon_data(pokemon_name: str) -> dict | None:
    try:
        response = requests.get(f"{POKEAPI_BASE}/pokemon/{pokemon_name.lower()}", timeout=10)
        if response.status_code == 200:
            return response.json()
    except Exception:
        pass
    return None


def render():
    inject_stat_css()
    st.header("🧑‍💻 Gerenciar Meu Time Pokémon")
    st.write(f"Bem-vindo, **{st.session_state.user['username']}**! Monte seu time de até 6 Pokémon.")

    team = get_user_team(st.session_state.user["id"])

    st.subheader("Seu Time Atual")
    if team:
        cols = st.columns(min(len(team), 3))
        for idx, pokemon in enumerate(team):
            with cols[idx % 3]:
                if pokemon["sprite_url"]:
                    st.image(pokemon["sprite_url"], width=120)
                st.write(f"**{pokemon['pokemon_name'].capitalize()}**")
                if pokemon["stats"]:
                    stats_html = ""
                    for stat in pokemon["stats"]:
                        label = stat['stat']['name'].capitalize()
                        val = stat['base_stat']
                        is_hp = (stat['stat']['name'] == 'hp')
                        stats_html += render_stat_row(val, label, is_hp, bar_width=160)
                    st.markdown(stats_html, unsafe_allow_html=True)
                if st.button(f"Remover", key=f"remove_{pokemon['pokemon_name']}"):
                    remove_team_pokemon(st.session_state.user["id"], pokemon["pokemon_name"])
                    st.rerun()
    else:
        st.info("Seu time está vazio. Adicione Pokémon abaixo!")

    st.markdown("---")
    st.subheader("Adicionar Pokémon ao Time")

    if len(team) >= 6:
        st.warning("Seu time já tem 6 Pokémon. Remova um para adicionar outro.")
        return

    col1, col2 = st.columns([3, 1])
    with col1:
        pokemon_input = st.text_input("Nome ou ID do Pokémon", placeholder="Ex: pikachu, charizard, 150")
    with col2:
        search_btn = st.button("Buscar", type="primary")

    if search_btn and pokemon_input:
        data = fetch_pokemon_data(pokemon_input)
        if data:
            st.session_state["team_preview"] = data
            st.rerun()
        else:
            st.error("Pokémon não encontrado.")

    if "team_preview" in st.session_state:
        data = st.session_state["team_preview"]
        sprite = data["sprites"]["front_default"] or data["sprites"]["front_shiny"]
        stats = data["stats"]

        col1, col2 = st.columns([1, 2])
        with col1:
            if sprite:
                st.image(sprite, width=150)
        with col2:
            st.write(f"### {data['name'].capitalize()} (ID: {data['id']})")
            st.write(f"**Tipos:** {', '.join([t['type']['name'].capitalize() for t in data['types']])}")
            st.write("**Estatísticas Base (Nível 100):**")
            stats_html = ""
            for stat in stats:
                label = stat['stat']['name'].capitalize()
                val = stat['base_stat']
                is_hp = (stat['stat']['name'] == 'hp')
                stats_html += render_stat_row(val, label, is_hp, bar_width=160)
            st.markdown(stats_html, unsafe_allow_html=True)

        if st.button("✅ Adicionar ao Time", type="primary"):
            if save_team_pokemon(st.session_state.user["id"], data["name"], sprite, stats):
                st.success(f"{data['name'].capitalize()} adicionado ao time!")
                del st.session_state["team_preview"]
                st.rerun()
            else:
                st.error("Não foi possível adicionar (time cheio ou erro).")

        if st.button("Cancelar"):
            del st.session_state["team_preview"]
            st.rerun()

    if team:
        st.markdown("---")
        if st.button("🗑️ Limpar Time Completo", type="secondary"):
            clear_user_team(st.session_state.user["id"])
            st.success("Time limpo!")
            st.rerun()