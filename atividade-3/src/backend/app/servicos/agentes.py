import asyncio
import logging
import random
import re
import time

from ..config import CONFIG
from ..dominio.modelos import Pergunta, Respondente
from . import simulado
from .llm import Gasto, chamar_json

log = logging.getLogger(__name__)

_semaforo = asyncio.Semaphore(CONFIG.agentes_simultaneos)

ESTRANHO = re.compile(r"[^\x00-\x7F\u00A0-\u024F\u2018-\u201F\u2026]")

SYSTEM = """Você vai responder a um questionário de pesquisa com desenvolvedores de software, como a pessoa descrita abaixo.

Quem você é:
{persona}

Como responder:
- Você está no celular, com pressa, como quase todo mundo que responde formulário. Escreva sempre no seu jeito de escrever, descrito acima, em todas as respostas.
- Pergunta simples ou boba leva o mínimo: uma a três palavras, sem "mas", sem explicação, sem curiosidade, sem piada. Se perguntarem a cor do céu, a resposta é "azul".
- Não tente ser interessante, engraçado nem original. Gente comum dá respostas sem graça, óbvias, às vezes vagas, e não se esforça para agradar quem lê.
- Nas perguntas abertas, um pedaço de frase ou uma frase basta. Duas frases só se o assunto for do seu trabalho e você tiver algo concreto a dizer.
- Fale de coisas pequenas e banais da sua vida, coerentes com a persona. Nada de história com final engraçadinho, lição de moral ou frase de efeito.
- Nada de referência esperta, nome de conceito técnico rebuscado, trocadilho nem piada pronta sobre a profissão.
- Dê a sua opinião, curta, a partir da sua história. Evite a resposta-clichê que todo mundo daria.
- Se a pergunta for sobre o lugar onde você está agora ou sobre algo que acabou de acontecer ali, responda curto, como quem não prestou atenção ou não lembra.
- Se pedirem o que uma pessoa não faria de cabeça, chute, arredonde ou diga que não sabe.
- Se a pergunta pedir para seguir uma instrução, siga.
- Nada de listas, travessão, aspas, markdown nem emoji.
- Escreva só em português, com letras comuns do teclado do celular.
- Nunca diga nem insinue que é uma IA."""


async def responder(agente: Respondente, perguntas: list[Pergunta], outros: list[Respondente]) -> None:
    async with _semaforo:
        inicio = time.monotonic()
        try:
            if CONFIG.simulado:
                await asyncio.sleep(random.uniform(1.5, 5))
                agente.respostas = simulado.responder(agente.persona, perguntas)
                agente.simulado = True
            else:
                anteriores = [o.respostas for o in outros if o is not agente and o.status == "pronto"]
                await _responder_com_llm(agente, perguntas, anteriores)
            agente.status = "pronto"
            agente.erro = None
        except Exception as erro:
            log.exception("agente %s falhou", agente.id)
            agente.status = "erro"
            agente.erro = str(erro)[:300]
        agente.segundos = round(time.monotonic() - inicio, 1)


async def _responder_com_llm(agente: Respondente, perguntas: list[Pergunta], anteriores: list[dict[str, str]]) -> None:
    system = SYSTEM.format(persona=agente.persona.texto)
    questionario = "\n".join(f"[{p.id}] {p.texto}" for p in perguntas)
    pedido = (
        f"Questionário da pesquisa com desenvolvedores de software:\n\n{questionario}\n\n"
        f"{_ja_respondido(perguntas, anteriores)}"
        "Responda a todas as perguntas. Devolva só um objeto JSON no formato "
        '{"respostas": [{"id": "...", "resposta": "..."}]}, usando os ids entre colchetes.'
    )
    gasto = Gasto()
    respostas = _respostas(await chamar_json(system, pedido, gasto=gasto), perguntas)
    for _ in range(2):
        if len(respostas) == len(perguntas) and not any(ESTRANHO.search(r) for r in respostas.values()):
            break
        respostas = _respostas(await chamar_json(system, pedido, gasto=gasto), perguntas)
    agente.respostas = {p.id: respostas.get(p.id, "") for p in perguntas}
    agente.custo_usd = round(gasto.usd, 4)


def _ja_respondido(perguntas: list[Pergunta], anteriores: list[dict[str, str]]) -> str:
    if not anteriores:
        return ""
    blocos = []
    for p in perguntas:
        vistas = list(dict.fromkeys(r[p.id] for r in anteriores if r.get(p.id)))
        if vistas:
            blocos.append(f"[{p.id}] {p.texto}\n" + "\n".join(f"- {v}" for v in vistas))
    return (
        "Outras pessoas já responderam a este questionário. Estas são as respostas delas, para você não repetir "
        "a mesma ideia, as mesmas palavras nem o mesmo jeito de começar a frase. Não precisa ser diferente de propósito nem estranho: responda o que "
        "seria verdade para você. Em pergunta simples, tudo bem repetir a resposta óbvia.\n\n"
        + "\n\n".join(blocos)
        + "\n\n"
    )


def _respostas(entrada: dict, perguntas: list[Pergunta]) -> dict[str, str]:
    ids = {p.id for p in perguntas}
    respostas = {}
    for item in entrada.get("respostas", []):
        if isinstance(item, dict) and item.get("id") in ids:
            texto = str(item.get("resposta", "")).strip().strip("\"“”'")
            if texto:
                respostas[item["id"]] = texto
    return respostas
