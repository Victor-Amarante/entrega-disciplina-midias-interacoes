"""Ponto de entrada: `uv run uvicorn app.main:app --reload`."""

import logging
from contextlib import asynccontextmanager

from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from .api import host, participante
from .armazenamento import Armazem
from .config import CONFIG

logging.basicConfig(level=logging.INFO)


@asynccontextmanager
async def ciclo_de_vida(app: FastAPI):
    app.state.armazem = Armazem(CONFIG.pasta_dados)
    app.state.armazem.carregar()
    if CONFIG.simulado:
        logging.warning("MODO SIMULADO: sem ANTHROPIC_API_KEY, os agentes usam respostas prontas.")
    yield


app = FastAPI(title="Caça ao respondente sintético", lifespan=ciclo_de_vida)
app.add_middleware(
    CORSMiddleware,
    allow_origins=CONFIG.cors_origens,
    allow_methods=["*"],
    allow_headers=["*"],
)

api = APIRouter(prefix="/api")
api.include_router(host.rotas)
api.include_router(participante.rotas)


@api.get("/saude")
async def saude():
    return {"ok": True, "simulado": CONFIG.simulado, "modelo": CONFIG.modelo}


app.include_router(api)

# Em produção o frontend (Next exportado como site estático) é servido daqui,
# para o experimento inteiro caber num link só.
if CONFIG.pasta_estatica.is_dir():
    app.mount("/", StaticFiles(directory=CONFIG.pasta_estatica, html=True), name="site")
