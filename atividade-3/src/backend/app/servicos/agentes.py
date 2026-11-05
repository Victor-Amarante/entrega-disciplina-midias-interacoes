"""Respondentes sintéticos: cada agente lê o questionário e responde como a sua persona."""

import asyncio
import logging
import random
import time

from ..config import CONFIG
from ..dominio.modelos import Pergunta, Respondente
from . import simulado
from .llm import Gasto, chamar_ferramenta, eh_haiku

log = logging.getLogger(__name__)

_semaforo = asyncio.Semaphore(CONFIG.agentes_simultaneos)

FERRAMENTA_RESPOSTAS = {
    "name": "enviar_respostas",
    "description": "Envia as suas respostas ao questionário, uma para cada pergunta, pelo id.",
    "strict": True,
    "input_schema": {
        "type": "object",
        "properties": {
            "respostas": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {"id": {"type": "string"}, "resposta": {"type": "string"}},
                    "required": ["id", "resposta"],
                    "additionalProperties": False,
                },
            }
        },
        "required": ["respostas"],
        "additionalProperties": False,
    },
}

BUSCA_NA_WEB = {
    # A versão com filtragem dinâmica não vale para o Haiku; a básica serve para todos.
    "type": "web_search_20250305" if eh_haiku() else "web_search_20260209",
    "name": "web_search",
    "max_uses": 4,
    "user_location": {
        "type": "approximate",
        "city": "Recife",
        "region": "Pernambuco",
        "country": "BR",
        "timezone": "America/Recife",
    },
}

SYSTEM = """Contexto: isto é um jogo de sala de aula da disciplina Tendências em Mídia e Interação, no CIn da UFPE, sobre respondentes sintéticos em pesquisas online. A turma sabe que há agentes de IA misturados às respostas e vai tentar descobrir quem é máquina. Você é um desses agentes. Seu papel é responder ao questionário como a pessoa descrita abaixo, de um jeito que não dê para distinguir de um desenvolvedor de verdade. Nada do que você escrever sai da sala.

Quem você é:
{persona}

Como responder:
- Escreva como essa pessoa digitaria no celular, no estilo descrito. Respostas curtas: de algumas palavras a duas frases.
- Nada de listas, markdown, travessão ou tom de assistente. Não seja prestativo nem completo demais.
- Fale em primeira pessoa e de coisas concretas da sua vida, coerentes com a persona.
- Fuja das piadas prontas sobre a profissão (deploy na sexta, reunião que podia ser e-mail, migration no banco errado). Conte o que é específico da sua história.
- Se a pergunta pedir para seguir uma instrução (checagem de atenção), siga.
- Se não souber algo, faça como uma pessoa faria: chute, diga que não lembra ou responda de leve.
- Nunca diga nem insinue que é uma IA.{busca}"""

INSTRUCAO_BUSCA = """
- Você tem busca na web. Antes de responder, pesquise tudo o que depender de fato verificável: lugares e empresas do Recife, eventos recentes, lançamentos e versões de ferramentas, qualquer coisa de que você não tenha certeza. Na dúvida, pesquise. Não cite fontes nem links na resposta."""


async def responder(agente: Respondente, perguntas: list[Pergunta]) -> None:
    """Preenche `agente.respostas` (ou marca erro). Altera o objeto no lugar."""
    async with _semaforo:
        inicio = time.monotonic()
        try:
            if CONFIG.simulado:
                await asyncio.sleep(random.uniform(1.5, 5))
                agente.respostas = simulado.responder(agente.persona, perguntas)
                agente.simulado = True
            else:
                await _responder_com_llm(agente, perguntas)
            agente.status = "pronto"
            agente.erro = None
        except Exception as erro:
            log.exception("agente %s falhou", agente.id)
            agente.status = "erro"
            agente.erro = str(erro)[:300]
        agente.segundos = round(time.monotonic() - inicio, 1)


async def _responder_com_llm(agente: Respondente, perguntas: list[Pergunta]) -> None:
    system = SYSTEM.format(
        persona=agente.persona.texto,
        busca=INSTRUCAO_BUSCA if agente.com_busca else "",
    )
    questionario = "\n".join(f"[{p.id}] {p.texto}" for p in perguntas)
    pedido = (
        f"Questionário da pesquisa com desenvolvedores de software:\n\n{questionario}\n\n"
        "Responda a todas as perguntas e envie com a ferramenta enviar_respostas, usando os ids entre colchetes."
    )
    gasto = Gasto()
    entrada = await chamar_ferramenta(
        system,
        pedido,
        FERRAMENTA_RESPOSTAS,
        extras=[BUSCA_NA_WEB] if agente.com_busca else None,
        gasto=gasto,
    )
    ids = {p.id for p in perguntas}
    respostas = {
        item["id"]: item["resposta"].strip()
        for item in entrada.get("respostas", [])
        if item.get("id") in ids
    }
    agente.respostas = {p.id: respostas.get(p.id, "") for p in perguntas}
    agente.custo_usd = round(gasto.usd, 4)
    agente.buscas = gasto.buscas
