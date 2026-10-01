import os
import json
from pathlib import Path

try:
    import openai
except ImportError:
    openai = None


def _load_env():
    env_path = Path(__file__).resolve().parent.parent.parent / ".env"
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
    api_key = vars_.get("OPENAI_API_KEY")
    return api_key is not None and api_key != ""


def chat_completion(messages, model="groq-llama3", temperature=0.7, max_tokens=500, base_url=None):
    if not is_configured():
        return {"error": "OpenAI/Groq not configured. Set OPENAI_API_KEY in .env"}

    if openai is None:
        return {"error": "openai package not installed"}

    vars_ = _get_vars()
    provider = vars_.get("OPENAI_PROVIDER", "groq")
    target_base = base_url or vars_.get("OPENAI_BASE_URL") or (
        "https://api.groq.com/openai/v1" if provider == "groq" else "https://api.openai.com/v1"
    )

    if openai:
        openai.api_key = vars_["OPENAI_API_KEY"]
        openai.base_url = target_base

    try:
        response = openai.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        return {
            "content": response.choices[0].message.content,
            "model": response.model,
            "usage": dict(response.usage),
        }
    except Exception as e:
        return {"error": str(e)}