import asyncio
import json
import re
from dataclasses import dataclass

import httpx2

from ..config import CONFIG, PRECOS

_cliente: httpx2.AsyncClient | None = None


def cliente() -> httpx2.AsyncClient:
    global _cliente
    if _cliente is None:
        _cliente = httpx2.AsyncClient(
            base_url=CONFIG.api_url,
            headers={"Authorization": f"Bearer {CONFIG.api_chave}"},
            timeout=180.0,
        )
    return _cliente


@dataclass
class Gasto:
    usd: float = 0.0

    def somar(self, usage: dict) -> None:
        preco_entrada, preco_saida = PRECOS.get(CONFIG.modelo, PRECOS["abliterated-model-large-v2"])
        em_cache = (usage.get("prompt_tokens_details") or {}).get("cached_tokens") or 0
        entrada = (usage.get("prompt_tokens", 0) - em_cache) + em_cache * 0.1
        self.usd += (entrada * preco_entrada + usage.get("completion_tokens", 0) * preco_saida) / 1_000_000


def _objeto_json(texto: str) -> dict:
    texto = re.sub(r"<think>.*?</think>", "", texto, flags=re.S)
    inicio, fim = texto.find("{"), texto.rfind("}")
    if inicio < 0 or fim < inicio:
        raise ValueError("sem objeto JSON")
    return json.loads(texto[inicio : fim + 1])


async def chamar_json(system: str, pedido: str, gasto: Gasto | None = None) -> dict:
    gasto = gasto if gasto is not None else Gasto()
    corpo = {
        "model": CONFIG.modelo,
        "messages": [{"role": "system", "content": system}, {"role": "user", "content": pedido}],
        "response_format": {"type": "json_object"},
        "temperature": CONFIG.temperatura,
        "top_p": 1,
        "reasoning_effort": CONFIG.esforco,
        "include_reasoning": True,
        "max_tokens": 16000,
    }
    erro = "o modelo não devolveu JSON"
    for tentativa in range(3):
        resposta = await cliente().post("/chat/completions", json=corpo)
        if resposta.status_code == 429 or resposta.status_code >= 500:
            erro = f"API do modelo: HTTP {resposta.status_code}"
            await asyncio.sleep(2 * (tentativa + 1))
            continue
        if resposta.status_code >= 400:
            raise RuntimeError(f"API do modelo: HTTP {resposta.status_code} {resposta.text[:200]}")
        dados = resposta.json()
        gasto.somar(dados.get("usage") or {})
        texto = dados["choices"][0]["message"].get("content") or ""
        try:
            return _objeto_json(texto)
        except ValueError:
            continue
    raise RuntimeError(erro)
