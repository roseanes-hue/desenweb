import streamlit as st
from core.team_builder import build_team
from core.evaluator import evaluate_team
from core.type_chart import ALL_TYPES
from core import render_stat_row, inject_stat_css


def render():
    inject_stat_css()
    st.header("🧠 Montador de Times Pokémon")
    st.write("Monte um time otimizado com o Algoritmo Guloso ou defina posições travadas.")

    st.subheader("🔒 Posições Travadas (Opcional)")
    st.write("Defina Pokémon que **devem** estar no time. O algoritmo completará as vagas restantes.")

    locked = []
    cols = st.columns(6)
    for i in range(6):
        with cols[i]:
            name = st.text_input(f"Slot {i+1}", key=f"locked_{i}", placeholder="Ex: pikachu")
            if name.strip():
                locked.append(name.strip())

    st.subheader("🎯 Filtro por Tipo (Opcional)")
    type_filter = st.multiselect(
        "Filtrar candidatos por tipo",
        ALL_TYPES,
        key="type_filter",
    )

    st.markdown("---")

    col1, col2 = st.columns([1, 3])
    with col1:
        build_btn = st.button("⚡ Montar Time", type="primary", use_container_width=True)

    if build_btn:
        with st.spinner("Montando time com Algoritmo Guloso..."):
            team = build_team(
                locked=locked if locked else None,
                type_filter=type_filter if type_filter else None,
                max_members=6,
            )

        if not team:
            st.error("❌ Não foi possível montar um time. Verifique os Pokémon informados.")
            return

        st.session_state.built_team = team

    team = st.session_state.get("built_team")
    if team is None:
        return

    st.subheader(f"⚔️ Time Montado ({len(team)} membros)")

    for i, pokemon in enumerate(team):
        with st.expander(f"#{pokemon['id']} {pokemon['name'].title()} — Tipos: {'/'.join(t.upper() for t in pokemon['types'])}", expanded=False):
            col_img, col_stats = st.columns([1, 2])
            with col_img:
                if pokemon["sprite_default"]:
                    st.image(pokemon["sprite_default"], width=150)
            with col_stats:
                stats_html = ""
                for key, label in [("hp", "HP"), ("attack", "ATK"), ("defense", "DEF"),
                                    ("special-attack", "SP.ATK"), ("special-defense", "SP.DEF"), ("speed", "SPD")]:
                    val = pokemon["stats"].get(key, 0)
                    is_hp = (key == "hp")
                    stats_html += render_stat_row(val, label, is_hp, bar_width=160)
                st.markdown(stats_html, unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("📊 Relatório de Avaliação")

    eval_result = evaluate_team(team)
    details = eval_result["details"]

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Pontuação Total", f"{eval_result['score']}/100")
    with col2:
        st.metric("Tipos Cobertos", f"{details['types_covered']}/{details['total_types']}")
    with col3:
        st.metric("Fraquezas Compartilhadas", details["shared_weaknesses"])
    with col4:
        st.metric("Índice Tanque Médio", details["avg_tank_index"])

    with st.expander("🗺️ Cobertura Ofensiva"):
        coverage = details["coverage"]
        for t in ALL_TYPES:
            m = coverage[t]
            bar_len = int(m * 10)
            bar = "█" * bar_len + "░" * (20 - bar_len)
            if m >= 2:
                color = "red"
            elif m >= 1:
                color = "orange"
            else:
                color = "gray"
            st.markdown(f":{color}[{t.upper():12s}] {bar} {m}x")

    with st.expander("🛡️ Sinergia Defensiva"):
        synergy = details["synergy"]
        st.markdown("#### Fraquezas compartilhadas")
        for t in ALL_TYPES:
            count = synergy["weaknesses"].get(t, 0)
            if count >= 2:
                st.markdown(f"- **{t.upper()}**: {count} membros vulneráveis")

        st.markdown("#### Resistências")
        for t in ALL_TYPES:
            count = synergy["resistances"].get(t, 0)
            if count >= 2:
                st.markdown(f"- **{t.upper()}**: {count} membros resistentes")

        st.markdown("#### Imunidades")
        for t in ALL_TYPES:
            count = synergy["immunities"].get(t, 0)
            if count > 0:
                st.markdown(f"- **{t.upper()}**: {count} membros imunes")

    st.markdown("---")
    st.caption("Criado por Roseane Vilela de Sousa — Kit Pokémon em Python")