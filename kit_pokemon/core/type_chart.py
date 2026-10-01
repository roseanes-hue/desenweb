import json
import os

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
_matrix = None

ALL_TYPES = [
    "normal", "fire", "water", "electric", "grass", "ice",
    "fighting", "poison", "ground", "flying", "psychic", "bug",
    "rock", "ghost", "dragon", "dark", "steel", "fairy",
]


def _load_matrix():
    global _matrix
    if _matrix is None:
        path = os.path.join(DATA_DIR, "type_matrix.json")
        with open(path, "r", encoding="utf-8") as f:
            _matrix = json.load(f)
    return _matrix


def calculate_effectiveness(attacker_type, defender_types):
    matrix = _load_matrix()
    attacker = attacker_type.lower()
    multiplier = 1.0
    for dtype in defender_types:
        dtype = dtype.lower()
        if attacker in matrix and dtype in matrix[attacker]:
            multiplier *= matrix[attacker][dtype]
    return multiplier


def get_defensive_multipliers(defender_types):
    matrix = _load_matrix()
    result = {}
    for attacker in ALL_TYPES:
        mult = 1.0
        for dtype in defender_types:
            dtype = dtype.lower()
            if attacker in matrix and dtype in matrix[attacker]:
                mult *= matrix[attacker][dtype]
        result[attacker] = mult
    return result


def get_weaknesses(defender_types):
    multipliers = get_defensive_multipliers(defender_types)
    return [t for t, m in multipliers.items() if m > 1]


def get_resistances(defender_types):
    multipliers = get_defensive_multipliers(defender_types)
    return [t for t, m in multipliers.items() if 0 < m < 1]


def get_immunities(defender_types):
    multipliers = get_defensive_multipliers(defender_types)
    return [t for t, m in multipliers.items() if m == 0]
