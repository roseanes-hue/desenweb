import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from core.pokeapi_client import get_pokemon
from core.type_chart import ALL_TYPES, calculate_effectiveness, get_defensive_multipliers
from core.team_builder import build_team
from core.evaluator import evaluate_team


def menu_pokedex():
    print("\n=== 🔍 POKÉDEX ===")
    name = input("Nome ou ID do Pokémon: ").strip()
    if not name:
        return
    pokemon = get_pokemon(name)
    if not pokemon:
        print(f"❌ Pokémon '{name}' não encontrado.")
        return
    print(f"\n#{pokemon['id']} {pokemon['name'].title()}")
    print(f"Tipos: {'/'.join(t.upper() for t in pokemon['types'])}")
    print(f"Altura: {pokemon['height']}m | Peso: {pokemon['weight']}kg")
    print(f"HP: {pokemon['hp']} | ATK: {pokemon['attack']} | DEF: {pokemon['defense']}")
    print(f"SP.ATK: {pokemon['sp_attack']} | SP.DEF: {pokemon['sp_defense']} | SPD: {pokemon['speed']}")


def menu_calculator():
    print("\n=== ⚔️ CALCULADORA DE TIPOS ===")
    print("Tipos disponíveis:", ", ".join(ALL_TYPES))
    atk = input("Tipo atacante: ").strip().lower()
    defs = input("Tipo(s) defensor(es) (vírgula): ").strip().lower().split(",")
    defs = [d.strip() for d in defs if d.strip()]

    if atk not in ALL_TYPES:
        print("❌ Tipo atacante inválido.")
        return
    for d in defs:
        if d not in ALL_TYPES:
            print(f"❌ Tipo defensor inválido: {d}")
            return

    mult = calculate_effectiveness(atk, defs)
    print(f"\n{atk.upper()} atacando {'/'.join(d.upper() for d in defs)}: {mult}x")

    multipliers = get_defensive_multipliers(defs)
    super_eff = [(t, m) for t, m in multipliers.items() if m > 1]
    not_eff = [(t, m) for t, m in multipliers.items() if 0 < m < 1]
    no_eff = [(t, m) for t, m in multipliers.items() if m == 0]

    if super_eff:
        print("\n🔴 Fraquezas:")
        for t, m in sorted(super_eff, key=lambda x: -x[1]):
            print(f"  {t.upper()}: {m}x")
    if not_eff:
        print("\n🔵 Resistências:")
        for t, m in sorted(not_eff, key=lambda x: x[1]):
            print(f"  {t.upper()}: {m}x")
    if no_eff:
        print("\n⚫ Imunidades:")
        for t, m in no_eff:
            print(f"  {t.upper()}: {m}x")


def menu_builder():
    print("\n=== 🧠 MONTADOR DE TIMES ===")
    print("Digite os Pokémon para o time (vazio para parar, até 6).")
    team = []
    for i in range(6):
        name = input(f"Slot {i+1}: ").strip()
        if not name:
            break
        team.append(name)

    print("\nMontando time...")
    built = build_team(locked=team if team else None, max_members=6)

    if not built:
        print("❌ Não foi possível montar o time.")
        return

    print(f"\n⚔️ Time Montado ({len(built)} membros):")
    for p in built:
        print(f"  #{p['id']} {p['name'].title()} — {'/'.join(t.upper() for t in p['types'])}")

    eval_result = evaluate_team(built)
    d = eval_result["details"]
    print(f"\n📊 Avaliação:")
    print(f"  Pontuação: {eval_result['score']}/100")
    print(f"  Tipos cobertos: {d['types_covered']}/{d['total_types']}")
    print(f"  Fraquezas compartilhadas: {d['shared_weaknesses']}")
    print(f"  Índice tanque médio: {d['avg_tank_index']}")


def main():
    print("🎮 KIT POKÉMON EM PYTHON")
    print("Criado por Roseane Vilela de Sousa\n")

    while True:
        print("\n--- MENU PRINCIPAL ---")
        print("1. 🔍 Pokédex")
        print("2. ⚔️ Calculadora de Tipos")
        print("3. 🧠 Montador de Times")
        print("0. Sair")

        opcao = input("\nOpção: ").strip()

        if opcao == "1":
            menu_pokedex()
        elif opcao == "2":
            menu_calculator()
        elif opcao == "3":
            menu_builder()
        elif opcao == "0":
            print("👋 Até mais!")
            break
        else:
            print("❌ Opção inválida.")


if __name__ == "__main__":
    main()
