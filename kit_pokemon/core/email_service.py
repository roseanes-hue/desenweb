import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path


def _load_env():
    env_path = Path(__file__).resolve().parent.parent / ".env"
    variables = {}
    if env_path.exists():
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if "=" in line:
                    key, _, value = line.partition("=")
                    variables[key.strip()] = value.strip()
    return variables


_env_vars = None


def _get_vars():
    global _env_vars
    if _env_vars is None:
        _env_vars = _load_env()
    return _env_vars


def is_configured() -> bool:
    vars_ = _get_vars()
    return all(
        vars_.get(k)
        for k in ("SMTP_SERVER", "SMTP_PORT", "SMTP_EMAIL", "SMTP_PASSWORD")
    )


def send_verification_email(to_email: str, username: str, code: str) -> tuple[bool, str]:
    if not is_configured():
        return False, "SMTP não configurado. Configure .env com SMTP_SERVER, SMTP_PORT, SMTP_EMAIL, SMTP_PASSWORD."

    vars_ = _get_vars()
    smtp_server = vars_["SMTP_SERVER"]
    smtp_port = int(vars_["SMTP_PORT"])
    smtp_email = vars_["SMTP_EMAIL"]
    smtp_password = vars_["SMTP_PASSWORD"]

    subject = "Kit Pokémon - Código de Verificação"
    body = f"""
Olá, {username}!

Seu código de verificação para o Kit Pokémon é:

{code}

Digite este código na tela de verificação para ativar sua conta.

Se você não solicitou este cadastro, ignore este e-mail.

---
Kit Pokémon
Criado por Roseane Vilela de Sousa
"""

    msg = MIMEMultipart()
    msg["From"] = smtp_email
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain", "utf-8"))

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_email, smtp_password)
            server.send_message(msg)
        return True, "E-mail de verificação enviado!"
    except Exception as e:
        return False, f"Erro ao enviar e-mail: {e}"