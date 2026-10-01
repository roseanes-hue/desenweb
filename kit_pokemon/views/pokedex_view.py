import streamlit as st
from core.pokeapi_client import get_pokemon, get_pokemon_list
from core import render_stat_row, inject_stat_css

STAT_LABELS = {
    "hp": "HP",
    "attack": "Ataque",
    "defense": "Defesa",
    "special-attack": "Atq. Esp.",
    "special-defense": "Def. Esp.",
    "speed": "Velocidade",
}


def render():
    inject_stat_css()
    st.header("🔍 Pokédex")
    st.write("Busque por qualquer Pokémon por nome ou número da Pokédex.")

    col1, col2 = st.columns([3, 1])
    with col1:
        search = st.text_input("Nome ou ID do Pokémon", placeholder="Ex: pikachu ou 25")
    with col2:
        st.write("")
        st.write("")
        buscar = st.button("🔍 Buscar", use_container_width=True)

    if buscar and search:
        with st.spinner("Buscando na PokéAPI..."):
            pokemon = get_pokemon(search)

        if pokemon is None:
            st.error(f"❌ Pokémon '{search}' não encontrado. Verifique o nome ou ID.")
            return

        st.session_state.last_pokemon = pokemon

    pokemon = st.session_state.get("last_pokemon")
    if pokemon is None:
        return

    col_img, col_info = st.columns([1, 2])

    with col_img:
        if pokemon["sprite_default"]:
            st.image(pokemon["sprite_default"], width=200, caption=pokemon["name"].title())
        if pokemon["sprite_shiny"]:
            with st.expander("✨ Versão Shiny"):
                st.image(pokemon["sprite_shiny"], width=200, caption="Shiny")

    with col_info:
        st.subheader(f"#{pokemon['id']} {pokemon['name'].title()}")

        types_html = " ".join(
            [f"`{t.upper()}`" for t in pokemon["types"]]
        )
        st.markdown(f"**Tipos:** {types_html}")

        col_h, col_w = st.columns(2)
        with col_h:
            st.metric("Altura", f"{pokemon['height']} m")
        with col_w:
            st.metric("Peso", f"{pokemon['weight']} kg")

        st.markdown("---")
        st.markdown("### 📊 Estatísticas Base (Nível 100)")
        st.caption("Base | Barra (máx 180) | Mín | Máx")
        for key, label in STAT_LABELS.items():
            val = pokemon["stats"].get(key, 0)
            is_hp = (key == "hp")
            st.markdown(render_stat_row(val, label, is_hp), unsafe_allow_html=True)

    with st.expander("📋 Dados Completos (JSON)"):
        st.json(pokemon)