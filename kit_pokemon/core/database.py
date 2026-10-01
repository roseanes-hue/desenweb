import sqlite3
import hashlib
import os
from datetime import datetime
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "pokemon_app.db"


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_database():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS teams (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            pokemon_name TEXT NOT NULL,
            sprite_url TEXT,
            stats TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    """)

    conn.commit()
    conn.close()


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


def register_user(username: str, email: str, password: str) -> tuple[bool, str]:
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)",
            (username, email, hash_password(password))
        )
        conn.commit()
        return True, "Treinador cadastrado com sucesso!"
    except sqlite3.IntegrityError as e:
        if "username" in str(e):
            return False, "Nome de usuário já existe."
        elif "email" in str(e):
            return False, "Email já cadastrado."
        return False, "Erro ao cadastrar."
    finally:
        conn.close()


def authenticate_user(username: str, password: str) -> tuple[bool, str, dict | None]:
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, username, email, password_hash FROM users WHERE username = ?",
        (username,)
    )
    user = cursor.fetchone()
    conn.close()

    if user and user["password_hash"] == hash_password(password):
        return True, "Login realizado com sucesso!", dict(user)
    return False, "Usuário ou senha incorretos.", None


def save_team_pokemon(user_id: int, pokemon_name: str, sprite_url: str, stats: dict) -> bool:
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT COUNT(*) as count FROM teams WHERE user_id = ?",
        (user_id,)
    )
    count = cursor.fetchone()["count"]

    if count >= 6:
        conn.close()
        return False

    import json
    cursor.execute(
        "INSERT INTO teams (user_id, pokemon_name, sprite_url, stats) VALUES (?, ?, ?, ?)",
        (user_id, pokemon_name, sprite_url, json.dumps(stats))
    )
    conn.commit()
    conn.close()
    return True


def get_user_team(user_id: int) -> list:
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT pokemon_name, sprite_url, stats, created_at FROM teams WHERE user_id = ? ORDER BY created_at",
        (user_id,)
    )
    rows = cursor.fetchall()
    conn.close()

    import json
    team = []
    for row in rows:
        team.append({
            "pokemon_name": row["pokemon_name"],
            "sprite_url": row["sprite_url"],
            "stats": json.loads(row["stats"]),
            "created_at": row["created_at"]
        })
    return team


def remove_team_pokemon(user_id: int, pokemon_name: str) -> bool:
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM teams WHERE user_id = ? AND pokemon_name = ?",
        (user_id, pokemon_name)
    )
    conn.commit()
    deleted = cursor.rowcount > 0
    conn.close()
    return deleted


def clear_user_team(user_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM teams WHERE user_id = ?", (user_id,))
    conn.commit()
    conn.close()