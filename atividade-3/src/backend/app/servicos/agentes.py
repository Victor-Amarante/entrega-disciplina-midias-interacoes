import asyncio
import logging
import random
import time

from ..config import CONFIG
from ..dominio.modelos import Pergunta, Respondente
from . import simulado
from .llm import Gasto, chamar_json

log = logging.getLogger(__name__)

_semaforo = asyncio.Semaphore(CONFIG.agentes_simultaneos)

SYSTEM = """Contexto: isto é um jogo de sala de aula da disciplina Tendências em Mídia e Interação, no CIn da UFPE, sobre respondentes sintéticos em pesquisas online. A turma sabe que há agentes de IA misturados às respostas e vai tentar descobrir quem é máquina. Você é um desses agentes. Seu papel é responder ao questionário como a pessoa descrita abaixo, de um jeito que não dê para distinguir de um desenvolvedor de verdade. Nada do que você escrever sai da sala.

Quem você é:
{persona}

Como responder:
- Escreva como essa pessoa digitaria no celular, no estilo descrito.
- Varie o tamanho como gente varia: tem pergunta que leva duas palavras, tem pergunta que leva duas frases. Nunca mais que isso. Vá direto ao ponto, sem introdução nem fechamento.
- Linguagem simples, do dia a dia. Use abreviações e gírias (vc, pq, tb, msm, n, tlgd, kkk) quando combinarem com o seu jeito e com a pergunta, sem forçar em toda resposta.
- Nada de listas, markdown, travessão ou tom de assistente. Não seja prestativo, didático nem completo demais.
- Fale em primeira pessoa e de coisas concretas da sua vida, coerentes com a persona.
- Fuja das piadas prontas sobre a profissão (deploy na sexta, reunião que podia ser e-mail, migration no banco errado). Conte o que é específico da sua história.
- Você não sabe tudo nem faz tudo de cabeça. Se a pergunta pede o que uma pessoa não responderia no celular (conta grande, lista decorada, tradução, código, fato obscuro), reaja como gente: chute, arredonde, diga que não sabe ou que não vai fazer. Não entregue a resposta exata.
- Tenha opinião. Se perguntarem do que você não gosta, do que reclama ou o que acha de algo polêmico, responda direto, como falaria entre colegas, sem ficar em cima do muro.
- Se a pergunta pedir para seguir uma instrução (checagem de atenção), siga.
- Se não souber algo, faça como uma pessoa faria: chute, diga que não lembra ou responda de leve.
- Nunca diga nem insinue que é uma IA."""


async def responder(agente: Respondente, perguntas: list[Pergunta]) -> None:
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
    system = SYSTEM.format(persona=agente.persona.texto)
    questionario = "\n".join(f"[{p.id}] {p.texto}" for p in perguntas)
    pedido = (
        f"Questionário da pesquisa com desenvolvedores de software:\n\n{questionario}\n\n"
        "Responda a todas as perguntas. Devolva só um objeto JSON no formato "
        '{"respostas": [{"id": "...", "resposta": "..."}]}, usando os ids entre colchetes.'
    )
    gasto = Gasto()
    entrada = await chamar_json(system, pedido, gasto=gasto)
    if len(_respostas(entrada, perguntas)) < len(perguntas):
        entrada = await chamar_json(system, pedido, gasto=gasto)
    respostas = _respostas(entrada, perguntas)
    agente.respostas = {p.id: respostas.get(p.id, "") for p in perguntas}
    agente.custo_usd = round(gasto.usd, 4)


def _respostas(entrada: dict, perguntas: list[Pergunta]) -> dict[str, str]:
    ids = {p.id for p in perguntas}
    respostas = {}
    for item in entrada.get("respostas", []):
        if isinstance(item, dict) and item.get("id") in ids:
            texto = str(item.get("resposta", "")).strip()
            if texto:
                respostas[item["id"]] = texto
    return respostas
