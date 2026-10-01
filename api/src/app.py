import os
from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv

# Carrega variáveis de ambiente do arquivo .env da pasta api
caminho_env = Path(__file__).resolve().parent.parent / '.env'
load_dotenv(dotenv_path=caminho_env)

from .rotas.lead_rotas import router as lead_router

app = FastAPI(title="API Landing Page Lead Capture - Python")

# Configuração de CORS mais segura
origem_permitida = os.getenv("ORIGEM_PERMITIDA", "").strip()
origens = [o.strip() for o in origem_permitida.split(",") if o.strip()] if origem_permitida else []

app.add_middleware(
    CORSMiddleware,
    allow_origins=origens,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
    expose_headers=["X-Request-ID"],
)

# Registra rotas da API
app.include_router(lead_router, prefix="/api")

# Middleware de segurança - adiciona headers de proteção
@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Content-Security-Policy"] = "default-src 'self'"
    return response

@app.get("/api/health")
def health_check():
    return {"sucesso": True, "mensagem": "API funcionando!"}

# Servir arquivos estáticos do frontend (dist ou raiz do frontend)
caminho_dist = Path(__file__).resolve().parent.parent.parent / 'frontend' / 'dist'
caminho_frontend = Path(__file__).resolve().parent.parent.parent / 'frontend'
pasta_estatica = caminho_dist if caminho_dist.exists() else caminho_frontend

if pasta_estatica.exists():
    app.mount("/static", StaticFiles(directory=str(pasta_estatica)), name="static")

@app.get("/{full_path:path}")
async def servir_frontend_ou_fallback(request: Request, full_path: str):
    # Se a requisição for para a API, deixa o FastAPI responder 404 caso a rota não exista
    if full_path.startswith("api"):
        return FileResponse(status_code=404, path="")

    # Tenta entregar o arquivo solicitado (ex: assets, css, js, imagens)
    caminho_arquivo = pasta_estatica / full_path
    if full_path and caminho_arquivo.is_file():
        return FileResponse(caminho_arquivo)

    # Fallback para a Landing Page SPA (index.html)
    index_path = pasta_estatica / "index.html"
    if index_path.is_file():
        return FileResponse(index_path)

    return {"erro": "Página não encontrada"}
