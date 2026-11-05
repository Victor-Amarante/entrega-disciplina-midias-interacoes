"""Ato 2: quantas respostas sintéticas bastam para virar a enquete da turma."""

import logging
import math

from ..config import CONFIG
from ..dominio.modelos import Sala, VotoSintetico
from . import placar, simulado
from .llm import Gasto, chamar_ferramenta

log = logging.getLogger(__name__)

LIMITE_SINTETICOS = 40

FERRAMENTA_VOTOS = {
    "name": "registrar_votos",
    "description": "Registra as justificativas, uma por respondente.",
    "strict": True,
    "input_schema": {
        "type": "object",
        "properties": {"justificativas": {"type": "array", "items": {"type": "string"}}},
        "required": ["justificativas"],
        "additionalProperties": False,
    },
}

SYSTEM = """Contexto: jogo de sala de aula da disciplina Tendências em Mídia e Interação (CIn/UFPE). A turma votou numa enquete e agora vê, ao vivo, quantas respostas sintéticas bastariam para virar o resultado. As respostas que você escrever aparecem só no telão da sala, identificadas como sintéticas no final."""


def contagem(sala: Sala) -> tuple[int, int]:
    votos = list(sala.enquete.votos.values())
    return votos.count("a"), votos.count("b")


def ataque(sala: Sala) -> dict:
    a, b = contagem(sala)
    alvo = "b" if a >= b else "a"  # o atacante empurra o lado que está perdendo
    necessarios = abs(a - b) + 1
    resultado_placar = placar.calcular(sala)
    deteccao = resultado_placar["taxa_deteccao"]
    falsa_acusacao = resultado_placar["taxa_falsa_acusacao"]

    com_defesa = None
    if deteccao is not None and deteccao < 1:
        com_defesa = math.ceil(necessarios / (1 - deteccao))
    custo = resultado_placar["custo_medio_agente_usd"]

    return {
        "votos_a": a,
        "votos_b": b,
        "alvo": alvo,
        "necessarios": necessarios,
        "taxa_deteccao": deteccao,
        "necessarios_com_defesa": com_defesa,
        "humanos_barrados": round((falsa_acusacao or 0) * (a + b)),
        "custo_medio_agente_usd": custo,
        "custo_ataque_usd": round(custo * necessarios, 3) if custo else None,
        "status_sinteticos": sala.enquete.status_sinteticos,
        "sinteticos": [v.model_dump() for v in sala.enquete.sinteticos],
    }


async def gerar_sinteticos(sala: Sala) -> None:
    """Escreve as justificativas dos votos falsos. Altera `sala.enquete` no lugar."""
    enquete = sala.enquete
    dados = ataque(sala)
    alvo = dados["alvo"]
    opcao = enquete.opcao_a if alvo == "a" else enquete.opcao_b
    n = min(dados["necessarios"] + 2, LIMITE_SINTETICOS)
    enquete.status_sinteticos = "gerando"
    try:
        if CONFIG.simulado:
            textos = simulado.justificativas(n, opcao)
        else:
            gasto = Gasto()
            pedido = (
                f"Enquete: \"{enquete.pergunta}\"\nOpção a defender: \"{opcao}\"\n\n"
                f"Escreva {n} justificativas de voto, cada uma de um desenvolvedor de software diferente, "
                "todas a favor dessa opção. Curtas (uma frase), variadas no argumento e no jeito "
                "de escrever, como gente digitando no celular. Sem travessão, sem listas. "
                "Envie com a ferramenta registrar_votos."
            )
            entrada = await chamar_ferramenta(SYSTEM, pedido, FERRAMENTA_VOTOS, gasto=gasto)
            textos = [t.strip() for t in entrada.get("justificativas", []) if t.strip()]
            enquete.custo_sinteticos_usd = round(gasto.usd, 4)
        enquete.sinteticos = [VotoSintetico(opcao=alvo, justificativa=t) for t in textos[:n]]
        enquete.status_sinteticos = "pronto"
    except Exception:
        log.exception("falha ao gerar votos sintéticos")
        enquete.status_sinteticos = "erro"
