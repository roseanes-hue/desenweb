import requests
import json
import os

BASE_URL = "https://pokeapi.co/api/v2"
CACHE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "cache")


def _ensure_cache_dir():
    os.makedirs(CACHE_DIR, exist_ok=True)


def _cache_path(name_or_id):
    return os.path.join(CACHE_DIR, f"{str(name_or_id).lower()}.json")


def _read_cache(name_or_id):
    path = _cache_path(name_or_id)
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return None


def _write_cache(name_or_id, data):
    _ensure_cache_dir()
    path = _cache_path(name_or_id)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def get_pokemon(name_or_id):
    name_or_id = str(name_or_id).lower().strip()
    cached = _read_cache(name_or_id)
    if cached:
        return cached

    try:
        resp = requests.get(f"{BASE_URL}/pokemon/{name_or_id}", timeout=10)
        resp.raise_for_status()
        raw = resp.json()
    except requests.RequestException:
        return None

    stats = {s["stat"]["name"]: s["base_stat"] for s in raw.get("stats", [])}
    types = [t["type"]["name"] for t in raw.get("types", [])]

    pokemon = {
        "id": raw["id"],
        "name": raw["name"],
        "types": types,
        "stats": stats,
        "hp": stats.get("hp", 0),
        "attack": stats.get("attack", 0),
        "defense": stats.get("defense", 0),
        "sp_attack": stats.get("special-attack", 0),
        "sp_defense": stats.get("special-defense", 0),
        "speed": stats.get("speed", 0),
        "sprite_default": raw.get("sprites", {}).get("front_default", ""),
        "sprite_shiny": raw.get("sprites", {}).get("front_shiny", ""),
        "height": raw.get("height", 0) / 10,
        "weight": raw.get("weight", 0) / 10,
    }

    _write_cache(name_or_id, pokemon)
    return pokemon


def get_pokemon_list(limit=1025, offset=0):
    cache_key = f"_list_{offset}_{limit}"
    cached = _read_cache(cache_key)
    if cached:
        return cached

    try:
        resp = requests.get(
            f"{BASE_URL}/pokemon",
            params={"limit": limit, "offset": offset},
            timeout=10,
        )
        resp.raise_for_status()
        data = resp.json()
    except requests.RequestException:
        return []

    results = [{"id": p["url"].split("/")[-2], "name": p["name"]} for p in data.get("results", [])]
    _write_cache(cache_key, results)
    return results
