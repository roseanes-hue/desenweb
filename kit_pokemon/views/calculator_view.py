import streamlit as st
from core.type_chart import ALL_TYPES, calculate_effectiveness, get_defensive_multipliers

TYPE_COLORS = {
    "normal": "#A8A878", "fire": "#F08030", "water": "#6890F0",
    "electric": "#F8D030", "grass": "#78C850", "ice": "#98D8D8",
    "fighting": "#C03028", "poison": "#A040A0", "ground": "#E0C068",
    "flying": "#A890F0", "psychic": "#F85888", "bug": "#A8B820",
    "rock": "#B8A038", "ghost": "#705898", "dragon": "#7038F8",
    "dark": "#705848", "steel": "#B8B8D0", "fairy": "#EE99AC",
}


def _mult_label(mult):
    if mult >= 2:
        return f"**{mult}x** 🔴 Super efetivo"
    elif mult > 1:
        return f"**{mult}x** 🟠"
    elif mult == 1:
        return f"**{mult}x** ⚪ Normal"
    elif mult > 0:
        return f"**{mult}x** 🔵 Pouco efetivo"
    else:
        return f"**{mult}x** ⚫ Sem efeito"


def render():
    st.header("⚔️ Calculadora de Tipos")
    st.write("Calcule a efetividade de tipos entre atacante e defensor.")

    tab_atk, tab_def = st.tabs(["Atacante → Defensor", "Defensor ← Atacantes"])

    with tab_atk:
        st.subheader("Calcular efetividade de ataque")
        col1, col2 = st.columns(2)
        with col1:
            atk_type = st.selectbox("Tipo Atacante", ALL_TYPES, key="atk_type")
        with col2:
            def_types = st.multiselect("Tipo(s) Defensor(es)", ALL_TYPES, key="def_types")

        if st.button("Calcular", key="calc_atk"):
            if not def_types:
                st.warning("Selecione pelo menos um tipo defensor.")
            else:
                mult = calculate_effectiveness(atk_type, def_types)
                st.success(f"**{atk_type.upper()}** atacando **{'/'.join(t.upper() for t in def_types)}**")
                st.markdown(f"### Multiplicador: {mult}x")
                st.markdown(_mult_label(mult))

    with tab_def:
        st.subheader("Ver fraquezas e resistências de um Pokémon")
        def_type = st.multiselect("Tipo(s) do Pokémon Defensor", ALL_TYPES, key="def_type_mult")

        if st.button("Analisar", key="calc_def"):
            if not def_type:
                st.warning("Selecione pelo menos um tipo.")
            else:
                multipliers = get_defensive_multipliers(def_type)
                st.markdown(f"### Defendendo como **{'/'.join(t.upper() for t in def_type)}**")

                super_eff = [(t, m) for t, m in multipliers.items() if m > 1]
                not_eff = [(t, m) for t, m in multipliers.items() if 0 < m < 1]
                no_eff = [(t, m) for t, m in multipliers.items() if m == 0]

                if super_eff:
                    st.markdown("#### 🔴 Super efetivo contra (Fraquezas)")
                    for t, m in sorted(super_eff, key=lambda x: -x[1]):
                        st.markdown(f"- **{t.upper()}**: {m}x")

                if not_eff:
                    st.markdown("#### 🔵 Pouco efetivo (Resistências)")
                    for t, m in sorted(not_eff, key=lambda x: x[1]):
                        st.markdown(f"- **{t.upper()}**: {m}x")

                if no_eff:
                    st.markdown("#### ⚫ Sem efeito (Imunidades)")
                    for t, m in no_eff:
                        st.markdown(f"- **{t.upper()}**: {m}x")

                if not super_eff and not not_eff and not no_eff:
                    st.info("Nenhuma fraqueza, resistência ou imunidade encontrada.")

                st.markdown("---")
                st.markdown("#### 📊 Tabela Completa")
                for t in ALL_TYPES:
                    m = multipliers[t]
                    bar_len = int(m * 10)
                    bar = "█" * bar_len + "░" * (20 - bar_len)
                    color = "red" if m > 1 else ("blue" if m < 1 else "gray")
                    st.markdown(f":{color}[{t.upper():12s}] {bar} {m}x")
