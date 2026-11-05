"""Configuração lida do ambiente. Tudo tem valor padrão para rodar localmente."""

import os
from dataclasses import dataclass, field
from pathlib import Path

from dotenv import load_dotenv

RAIZ_BACKEND = Path(__file__).resolve().parent.parent

# A chave da API pode vir de backend/.env (fora do git) ou do ambiente.
load_dotenv(RAIZ_BACKEND / ".env")

# Preço em US$ por milhão de tokens (entrada, saída). Usado só para mostrar o
# custo de cada respondente sintético na tela; não precisa ser exato.
PRECOS = {
    "claude-opus-5-5": (4.0, 20.0),
    "claude-sonnet-5-5": (2.0, 10.0),
    "claude-haiku-5-5": (0.10, 0.50),
}
PRECO_BUSCA = 0.01  # US$ por busca na web


@dataclass(frozen=True)
class Config:
    modelo: str = os.getenv("MODELO", "claude-haiku-5-5")
    # Respondente de pesquisa não precisa pensar muito, e a aula tem pressa.
    esforco: str = os.getenv("ESFORCO", "low")
    agentes_simultaneos: int = int(os.getenv("AGENTES_SIMULTANEOS", "6"))
    # Sem chave da API, os agentes respondem com frases prontas (bom para testar a interface).
    simulado: bool = os.getenv("MODO_SIMULADO") == "1" or not os.getenv("ANTHROPIC_API_KEY")
    pasta_dados: Path = Path(os.getenv("PASTA_DADOS", RAIZ_BACKEND / "dados"))
    pasta_estatica: Path = Path(
        os.getenv("PASTA_ESTATICA", RAIZ_BACKEND.parent / "frontend" / "out")
    )
    cors_origens: list[str] = field(
        default_factory=lambda: os.getenv("CORS_ORIGENS", "*").split(",")
    )


CONFIG = Config()
