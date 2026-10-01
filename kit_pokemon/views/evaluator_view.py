import streamlit as st
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from core.evaluator import evaluate_team
from core.type_chart import ALL_TYPES


def render():
    st.header("📊 Avaliador de Times Pokémon")
    st.write(
        "Informe 6 Pokémon (por nome ou ID) para avaliar a cobertura de tipos, "
        "sinergia defensiva e índice de tanque do seu time."
    )

    st.markdown("---")
    st.subheader("� Pokémon do Time")

    cols = st.columns(6)
    pokemon_names = []
    for i in range(6):
        with cols[i]:
            name = st.text_input(f"Pokémon {i+1}", key=f"eval_{i}", placeholder="Ex: charizard")
            pokemon_names.append(name.strip())

    st.markdown("---")
    evaluate_btn = st.button("� avaliar Time", type="primary", use_container_width=True)

    if evaluate_btn:
        # Filtrar nomes vazios
        names_filtered = [n for n in pokemon_names if n.strip()]
        if len(names_filtered) < 6:
            st.error(f"❏ Por favor, informe exatamente 6 Pokémon. Atualmente: {len(names_filtered)}")
        else:
            with st.spinner("Buscando dados e avaliando time..."):
                team = []
                seen_ids = set()
                error_flag = False
                for name in names_filtered:
                    pokemon = get_pokemon(name)
                    if not pokemon:
                        st.error(f"❌ Pokémon '{name}' não encontrado na PokéAPI.")
                        error_flag = True
                        break
                    if pokemon["id"] in seen_ids:
                        st.error(f"⚠️ Pokémon '{name}' já foi adicionado. Por favor, use nomes diferentes.")
                        error_flag = True
                        break
                    seen_ids.add(pokemon["id"])
                    team.append(pokemon)

                if error_flag:
                    return

                if len(team) == 6:
                    eval_result = evaluate_team(team)
                    details = eval_result["details"]

                    st.subheader("📈 Resultado da Avaliação")

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
                        st.markdown("#### Fraquezas compartilhadas (2+ membros)")
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


def get_pokemon(name_or_id):
    from core.pokeapi_client import get_pokemon as _get_pokemon
    return _get_pokemon(name_or_id)