import os
from dataclasses import dataclass, field
from pathlib import Path

from dotenv import load_dotenv

RAIZ_BACKEND = Path(__file__).resolve().parent.parent

load_dotenv(RAIZ_BACKEND / ".env")

PRECOS = {
    "abliterated-model": (1.0, 3.0),
    "abliterated-model-large-flash": (1.0, 2.0),
    "abliterated-model-large-v2": (3.0, 5.0),
}


@dataclass(frozen=True)
class Config:
    modelo: str = os.getenv("ABLIT_MODELO", "abliterated-model-large-v2")
    api_url: str = os.getenv("ABLIT_URL", "https://api.abliteration.ai/v1")
    api_chave: str = os.getenv("ABLITERATION_API_KEY", "")
    temperatura: float = float(os.getenv("ABLIT_TEMPERATURA", "1"))
    esforco: str = os.getenv("ESFORCO", "low")
    agentes_simultaneos: int = int(os.getenv("AGENTES_SIMULTANEOS", "6"))
    simulado: bool = os.getenv("MODO_SIMULADO") == "1" or not os.getenv("ABLITERATION_API_KEY")
    pasta_dados: Path = Path(os.getenv("PASTA_DADOS", RAIZ_BACKEND / "dados"))
    pasta_estatica: Path = Path(
        os.getenv("PASTA_ESTATICA", RAIZ_BACKEND.parent / "frontend" / "out")
    )
    cors_origens: list[str] = field(
        default_factory=lambda: os.getenv("CORS_ORIGENS", "*").split(",")
    )


CONFIG = Config()
