from .pokeapi_client import get_pokemon, get_pokemon_list
from .type_chart import ALL_TYPES, calculate_effectiveness
from .evaluator import offensive_coverage, count_covered_types, defensive_synergy, shared_weakness_count, tank_index

POPULAR_POKEMON = [
    "pikachu", "charizard", "blastoise", "venusaur", "gyarados",
    "dragonite", "alakazam", "machamp", "gengar", "onix",
    "lapras", "snorlax", "arcanine", "vaporeon", "jolteon",
    "flareon", "starmie", "nidoking", "clefable", "slowbro",
    "raichu", "ninetales", "persian", "primeape", "poliwrath",
    "kadabra", "magneton", "shellder", "haunter", "drowzee",
    "hypno", "kingler", "electrode", "exeggcute", "marowak",
    "hitmonlee", "hitmonchan", "lickitung", "weezing", "rhyhorn",
    "chansey", "tangela", "kangaskhan", "seadra", "seaking",
    "starmie", "mr-mime", "scyther", "jynx", "electabuzz",
    "magmar", "tauros", "gyarados", "lapras", "ditto",
    "eevee", "vaporeon", "jolteon", "flareon", "porygon",
    "omastar", "kabutops", "aerodactyl", "snorlax", "articuno",
    "zapdos", "moltres", "dragonite", "mewtwo", "mew",
]


def _coverage_gain(new_types, current_team_types):
    if not current_team_types:
        before = offensive_coverage([["normal"]])
        after = offensive_coverage(current_team_types + [new_types])
    else:
        before = offensive_coverage(current_team_types)
        after = offensive_coverage(current_team_types + [new_types])
    before_covered = count_covered_types(before)
    after_covered = count_covered_types(after)
    return after_covered - before_covered


def _synergy_penalty(new_types, current_team_types):
    if not current_team_types:
        return 0
    combined = current_team_types + [new_types]
    synergy = defensive_synergy(combined)
    return shared_weakness_count(synergy)


def _score_pokemon(pokemon, current_team_types):
    new_types = pokemon["types"]
    cov_gain = _coverage_gain(new_types, current_team_types)
    syn_penalty = _synergy_penalty(new_types, current_team_types)
    tank = tank_index(pokemon) / 255.0
    return cov_gain * 10 - syn_penalty * 5 + tank * 2


def build_team(locked=None, type_filter=None, max_members=6):
    locked = locked or []
    if len(locked) >= max_members:
        return locked[:max_members]

    team = []
    used_ids = set()

    for name in locked:
        pokemon = get_pokemon(name)
        if pokemon and pokemon["id"] not in used_ids:
            team.append(pokemon)
            used_ids.add(pokemon["id"])

    if type_filter:
        type_filter = [t.lower() for t in type_filter]

    while len(team) < max_members:
        best_pokemon = None
        best_score = float("-inf")

        for name in POPULAR_POKEMON:
            pokemon = get_pokemon(name)
            if not pokemon:
                continue
            if pokemon["id"] in used_ids:
                continue
            if type_filter:
                if not any(t in type_filter for t in pokemon["types"]):
                    continue

            current_types = [p["types"] for p in team] if team else [["normal"]]
            score = _score_pokemon(pokemon, current_types)

            if score > best_score:
                best_score = score
                best_pokemon = pokemon

        if best_pokemon is None:
            break

        team.append(best_pokemon)
        used_ids.add(best_pokemon["id"])

    return team
