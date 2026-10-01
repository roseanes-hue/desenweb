import sqlite3
import hashlib
import os
import secrets
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
            password_hash TEXT NOT NULL,
            is_verified INTEGER DEFAULT 0,
            verification_code TEXT
        )
    """)

    cursor.execute("PRAGMA table_info(users)")
    columns = [row[1] for row in cursor.fetchall()]
    if "is_verified" not in columns:
        cursor.execute("ALTER TABLE users ADD COLUMN is_verified INTEGER DEFAULT 0")
    if "verification_code" not in columns:
        cursor.execute("ALTER TABLE users ADD COLUMN verification_code TEXT")

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


def _generate_verification_code() -> str:
    return str(secrets.randbelow(1000000)).zfill(6)


def register_user(username: str, email: str, password: str) -> tuple[bool, str, str | None]:
    conn = get_connection()
    cursor = conn.cursor()

    verification_code = _generate_verification_code()

    try:
        cursor.execute(
            "INSERT INTO users (username, email, password_hash, verification_code, is_verified) VALUES (?, ?, ?, ?, 0)",
            (username, email, hash_password(password), verification_code)
        )
        conn.commit()
        return True, "Cadastro realizado! Verifique seu e-mail.", verification_code
    except sqlite3.IntegrityError as e:
        if "username" in str(e):
            return False, "Nome de usuário já existe.", None
        elif "email" in str(e):
            return False, "Email já cadastrado.", None
        return False, "Erro ao cadastrar.", None
    finally:
        conn.close()


def authenticate_user(username: str, password: str) -> tuple[bool, str, dict | None]:
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, username, email, password_hash, is_verified FROM users WHERE username = ?",
        (username,)
    )
    user = cursor.fetchone()
    conn.close()

    if user and user["password_hash"] == hash_password(password):
        if not user["is_verified"]:
            return False, "E-mail não verificado. Verifique sua caixa de entrada.", None
        return True, "Login realizado com sucesso!", dict(user)
    return False, "Usuário ou senha incorretos.", None


def verify_email_code(username: str, code: str) -> tuple[bool, str]:
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT verification_code, is_verified FROM users WHERE username = ?",
        (username,)
    )
    user = cursor.fetchone()

    if not user:
        conn.close()
        return False, "Usuário não encontrado."

    if user["is_verified"]:
        conn.close()
        return True, "E-mail já verificado."

    if user["verification_code"] != code:
        conn.close()
        return False, "Código inválido."

    cursor.execute(
        "UPDATE users SET is_verified = 1, verification_code = NULL WHERE username = ?",
        (username,)
    )
    conn.commit()
    conn.close()
    return True, "E-mail verificado com sucesso!"


def resend_verification_code(username: str) -> tuple[bool, str, str | None]:
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, is_verified FROM users WHERE username = ?",
        (username,)
    )
    user = cursor.fetchone()

    if not user:
        conn.close()
        return False, "Usuário não encontrado.", None

    if user["is_verified"]:
        conn.close()
        return True, "E-mail já verificado.", None

    new_code = _generate_verification_code()
    cursor.execute(
        "UPDATE users SET verification_code = ? WHERE username = ?",
        (new_code, username)
    )
    conn.commit()
    conn.close()
    return True, "Novo código enviado!", new_code


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