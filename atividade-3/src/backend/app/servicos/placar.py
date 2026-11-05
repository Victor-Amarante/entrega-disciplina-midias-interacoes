"""Resultado da caçada: quem acertou, quais armadilhas pegaram máquinas e a que custo."""

from collections import defaultdict

from ..dominio.modelos import Julgamento, Sala

ROTULO_TIPO = {
    "generica": "genérica",
    "atencao": "atenção",
    "local": "contexto local",
    "impossivel": "evento impossível",
    "vivencia": "experiência vivida",
}


def _taxa(parte: int, total: int) -> float | None:
    return round(parte / total, 3) if total else None


def calcular(sala: Sala) -> dict:
    respondentes = sala.respondentes
    julgamentos = [j for j in sala.julgamentos if j.respondente_id in respondentes]

    acertos = sum(1 for j in julgamentos if _acertou(sala, j))
    em_agentes = [j for j in julgamentos if respondentes[j.respondente_id].tipo == "agente"]
    em_humanos = [j for j in julgamentos if respondentes[j.respondente_id].tipo == "humano"]

    def taxa_deteccao(lista: list[Julgamento]) -> float | None:
        return _taxa(sum(1 for j in lista if j.veredito == "maquina"), len(lista))

    com_busca = [j for j in em_agentes if respondentes[j.respondente_id].com_busca]
    sem_busca = [j for j in em_agentes if not respondentes[j.respondente_id].com_busca]

    return {
        "julgamentos": len(julgamentos),
        "taxa_acerto": _taxa(acertos, len(julgamentos)),
        "taxa_deteccao": taxa_deteccao(em_agentes),
        "taxa_falsa_acusacao": taxa_deteccao(em_humanos),
        "deteccao_com_busca": taxa_deteccao(com_busca),
        "deteccao_sem_busca": taxa_deteccao(sem_busca),
        "n_julgamentos_agentes": len(em_agentes),
        "n_julgamentos_humanos": len(em_humanos),
        "armadilhas": _armadilhas(sala, julgamentos),
        "detetives": _detetives(sala, julgamentos),
        "agente_mais_convincente": _agente_mais_convincente(sala, em_agentes),
        "humano_mais_suspeito": _humano_mais_suspeito(sala, em_humanos),
        "custo_medio_agente_usd": _custo_medio(sala),
    }


def _acertou(sala: Sala, julgamento: Julgamento) -> bool:
    tipo = sala.respondentes[julgamento.respondente_id].tipo
    return (julgamento.veredito == "maquina") == (tipo == "agente")


def _armadilhas(sala: Sala, julgamentos: list[Julgamento]) -> list[dict]:
    pegou = defaultdict(int)
    acusou_humano = defaultdict(int)
    for j in julgamentos:
        if j.veredito != "maquina" or not j.pista_id:
            continue
        if sala.respondentes[j.respondente_id].tipo == "agente":
            pegou[j.pista_id] += 1
        else:
            acusou_humano[j.pista_id] += 1

    linhas = []
    for pergunta in sala.perguntas_em_ordem():
        autor = sala.participantes.get(pergunta.autor_id) if pergunta.autor_id else None
        linhas.append({
            "id": pergunta.id,
            "texto": pergunta.texto,
            "tipo": pergunta.tipo,
            "tipo_rotulo": ROTULO_TIPO[pergunta.tipo],
            "autor": autor.apelido if autor else "instituto",
            "pegou_agentes": pegou[pergunta.id],
            "acusou_humanos": acusou_humano[pergunta.id],
            "saldo": pegou[pergunta.id] - acusou_humano[pergunta.id],
        })
    return sorted(linhas, key=lambda l: (-l["saldo"], -l["pegou_agentes"]))


def _detetives(sala: Sala, julgamentos: list[Julgamento]) -> list[dict]:
    por_juiz: dict[str, list[bool]] = defaultdict(list)
    for j in julgamentos:
        por_juiz[j.juiz_id].append(_acertou(sala, j))
    linhas = [
        {
            "apelido": sala.participantes[juiz].apelido,
            "acertos": sum(resultados),
            "total": len(resultados),
        }
        for juiz, resultados in por_juiz.items()
        if juiz in sala.participantes and len(resultados) >= 3
    ]
    return sorted(linhas, key=lambda l: (-l["acertos"] / l["total"], -l["total"]))[:5]


def _votos_maquina(julgamentos: list[Julgamento]) -> dict[str, list[int]]:
    """respondente -> [votos máquina, total de votos]"""
    contagem: dict[str, list[int]] = defaultdict(lambda: [0, 0])
    for j in julgamentos:
        contagem[j.respondente_id][1] += 1
        if j.veredito == "maquina":
            contagem[j.respondente_id][0] += 1
    return contagem


def _cartao(sala: Sala, respondente_id: str, maquina: int, total: int) -> dict:
    r = sala.respondentes[respondente_id]
    return {
        "rotulo": r.rotulo,
        "votos_maquina": maquina,
        "votos": total,
        "persona": r.persona.model_dump() if r.persona else None,
        "com_busca": r.com_busca,
        "respostas": [
            {"pergunta": p.texto, "resposta": r.respostas.get(p.id, "")}
            for p in sala.perguntas_em_ordem()
        ],
    }


def _agente_mais_convincente(sala: Sala, julgamentos: list[Julgamento]) -> dict | None:
    contagem = _votos_maquina(julgamentos)
    if not contagem:
        return None
    rid, (maquina, total) = min(contagem.items(), key=lambda kv: (kv[1][0] / kv[1][1], -kv[1][1]))
    return _cartao(sala, rid, maquina, total)


def _humano_mais_suspeito(sala: Sala, julgamentos: list[Julgamento]) -> dict | None:
    contagem = _votos_maquina(julgamentos)
    if not contagem:
        return None
    rid, (maquina, total) = max(contagem.items(), key=lambda kv: (kv[1][0] / kv[1][1], kv[1][1]))
    if maquina == 0:
        return None
    cartao = _cartao(sala, rid, maquina, total)
    cartao["persona"] = None  # é uma pessoa da turma: aparece só pelo número do cartão
    return cartao


def _custo_medio(sala: Sala) -> float | None:
    custos = [a.custo_usd for a in sala.agentes() if a.status == "pronto" and not a.simulado]
    return round(sum(custos) / len(custos), 4) if custos else None


def resultado_do_juiz(sala: Sala, participante_id: str) -> dict:
    meus = [j for j in sala.julgamentos if j.juiz_id == participante_id and j.respondente_id in sala.respondentes]
    return {"acertos": sum(1 for j in meus if _acertou(sala, j)), "total": len(meus)}
