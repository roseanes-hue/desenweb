from .type_chart import ALL_TYPES, calculate_effectiveness


def offensive_coverage(team_types):
    coverage = {}
    for atk_type in ALL_TYPES:
        best = 0.0
        for def_types in team_types:
            mult = calculate_effectiveness(atk_type, def_types)
            if mult > best:
                best = mult
        coverage[atk_type] = best
    return coverage


def count_covered_types(coverage, threshold=1.0):
    return sum(1 for m in coverage.values() if m >= threshold)


def defensive_synergy(team_types):
    all_weak = []
    all_resist = []
    all_immune = []
    for def_types in team_types:
        for atk_type in ALL_TYPES:
            mult = calculate_effectiveness(atk_type, def_types)
            if mult > 1:
                all_weak.append(atk_type)
            elif 0 < mult < 1:
                all_resist.append(atk_type)
            elif mult == 0:
                all_immune.append(atk_type)
    weak_counts = {t: all_weak.count(t) for t in ALL_TYPES}
    resist_counts = {t: all_resist.count(t) for t in ALL_TYPES}
    immune_counts = {t: all_immune.count(t) for t in ALL_TYPES}
    return {
        "weaknesses": weak_counts,
        "resistances": resist_counts,
        "immunities": immune_counts,
    }


def shared_weakness_count(synergy):
    return sum(1 for v in synergy["weaknesses"].values() if v >= 2)


def tank_index(pokemon):
    return pokemon.get("hp", 0) + pokemon.get("defense", 0) + pokemon.get("sp_defense", 0)


def evaluate_team(pokemons):
    if not pokemons:
        return {"score": 0, "details": {}}

    team_types = [p["types"] for p in pokemons]
    coverage = offensive_coverage(team_types)
    covered = count_covered_types(coverage)
    synergy = defensive_synergy(team_types)
    shared_weak = shared_weakness_count(synergy)
    avg_tank = sum(tank_index(p) for p in pokemons) / len(pokemons)

    coverage_score = (covered / len(ALL_TYPES)) * 40
    synergy_score = max(0, 30 - shared_weak * 5)
    tank_score = min(30, avg_tank / 5)

    total = coverage_score + synergy_score + tank_score

    return {
        "score": round(total, 1),
        "details": {
            "coverage_score": round(coverage_score, 1),
            "synergy_score": round(synergy_score, 1),
            "tank_score": round(tank_score, 1),
            "types_covered": covered,
            "total_types": len(ALL_TYPES),
            "shared_weaknesses": shared_weak,
            "avg_tank_index": round(avg_tank, 1),
            "coverage": coverage,
            "synergy": synergy,
        },
    }
