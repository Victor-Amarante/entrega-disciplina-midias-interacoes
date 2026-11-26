from collections import defaultdict

from ..dominio.modelos import Julgamento, Sala

ROTULO_TIPO = {
    "generica": "genérica",
    "atencao": "atenção",
    "local": "contexto local",
    "impossivel": "evento impossível",
    "vivencia": "experiência vivida",
    "invertida": "só máquina sabe",
    "sem_filtro": "sem filtro",
    "sala": "aqui na sala",
    "pegadinha": "pegadinha",
}


def _taxa(parte: int, total: int) -> float | None:
    return round(parte / total, 3) if total else None


def _validos(sala: Sala) -> list[Julgamento]:
    return [j for j in sala.julgamentos if j.respondente_id in sala.respondentes]


def taxa_acerto(sala: Sala) -> float | None:
    julgamentos = _validos(sala)
    return _taxa(sum(1 for j in julgamentos if _acertou(sala, j)), len(julgamentos))


def calcular(sala: Sala) -> dict:
    respondentes = sala.respondentes
    julgamentos = _validos(sala)

    acertos = sum(1 for j in julgamentos if _acertou(sala, j))
    em_agentes = [j for j in julgamentos if respondentes[j.respondente_id].tipo == "agente"]
    em_humanos = [j for j in julgamentos if respondentes[j.respondente_id].tipo == "humano"]

    def disseram_maquina(lista: list[Julgamento]) -> int:
        return sum(1 for j in lista if j.veredito == "maquina")

    def taxa_deteccao(lista: list[Julgamento]) -> float | None:
        return _taxa(disseram_maquina(lista), len(lista))

    pegos, acusados = disseram_maquina(em_agentes), disseram_maquina(em_humanos)

    resultado = {
        "julgamentos": len(julgamentos),
        "acertos": acertos,
        "taxa_acerto": _taxa(acertos, len(julgamentos)),
        "taxa_deteccao": taxa_deteccao(em_agentes),
        "taxa_falsa_acusacao": taxa_deteccao(em_humanos),
        "n_julgamentos_agentes": len(em_agentes),
        "n_julgamentos_humanos": len(em_humanos),
        "matriz": {
            "agentes_pegos": pegos,
            "agentes_passaram": len(em_agentes) - pegos,
            "humanos_acusados": acusados,
            "humanos_reconhecidos": len(em_humanos) - acusados,
        },
        "armadilhas": _armadilhas(sala, julgamentos),
        "agente_mais_convincente": _agente_mais_convincente(sala, em_agentes),
        "humano_mais_suspeito": _humano_mais_suspeito(sala, em_humanos),
        "custo_medio_agente_usd": _custo_medio(sala),
        "auditoria": _auditoria(sala, julgamentos),
    }
    resultado["leituras"] = _leituras(resultado)
    return resultado


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
    for numero, pergunta in enumerate(sala.perguntas_em_ordem(), start=1):
        autor = sala.participantes.get(pergunta.autor_id) if pergunta.autor_id else None
        linhas.append({
            "id": pergunta.id,
            "numero": numero,
            "texto": pergunta.texto,
            "tipo": pergunta.tipo,
            "tipo_rotulo": ROTULO_TIPO[pergunta.tipo],
            "autor": autor.apelido if autor else "instituto",
            "pegou_agentes": pegou[pergunta.id],
            "acusou_humanos": acusou_humano[pergunta.id],
            "saldo": pegou[pergunta.id] - acusou_humano[pergunta.id],
        })
    return sorted(linhas, key=lambda l: (-l["saldo"], -l["pegou_agentes"]))


def _votos_maquina(julgamentos: list[Julgamento]) -> dict[str, list[int]]:
    contagem: dict[str, list[int]] = defaultdict(lambda: [0, 0])
    for j in julgamentos:
        contagem[j.respondente_id][1] += 1
        if j.veredito == "maquina":
            contagem[j.respondente_id][0] += 1
    return contagem


def _cartao(sala: Sala, respondente_id: str, maquina: int, total: int) -> dict:
    r = sala.respondentes[respondente_id]
    return {
        "id": r.id,
        "rotulo": r.rotulo,
        "verdade": "maquina" if r.tipo == "agente" else "humano",
        "votos_maquina": maquina,
        "votos": total,
        "persona": r.persona.model_dump() if r.persona else None,
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
    cartao["persona"] = None
    return cartao


def _custo_medio(sala: Sala) -> float | None:
    custos = [a.custo_usd for a in sala.agentes() if a.status == "pronto" and not a.simulado]
    return round(sum(custos) / len(custos), 4) if custos else None


def _auditoria(sala: Sala, julgamentos: list[Julgamento]) -> dict:
    numero = {p.id: i for i, p in enumerate(sala.perguntas_em_ordem(), start=1)}
    contagem = _votos_maquina(julgamentos)
    em_jogo = sorted(
        (r for r in sala.respondentes.values() if r.rotulo),
        key=lambda r: (r.tipo != "agente", int(r.rotulo)),
    )
    cartoes = [_cartao(sala, r.id, *contagem.get(r.id, (0, 0))) for r in em_jogo]

    por_juiz: dict[str, dict[str, Julgamento]] = defaultdict(dict)
    for j in julgamentos:
        por_juiz[j.juiz_id][j.respondente_id] = j
    jogadores = []
    for pid, recebidos in sala.atribuicoes.items():
        if pid not in sala.participantes:
            continue
        vereditos = {
            rid: {"veredito": j.veredito, "acertou": _acertou(sala, j), "pista": numero.get(j.pista_id)}
            for rid, j in por_juiz[pid].items()
        }
        jogadores.append({
            "apelido": sala.participantes[pid].apelido,
            "cartoes": recebidos,
            "vereditos": vereditos,
            "acertos": sum(v["acertou"] for v in vereditos.values()),
            "total": len(vereditos),
        })
    jogadores.sort(key=lambda l: (-(l["acertos"] / l["total"]) if l["total"] else 1, -l["total"], l["apelido"].lower()))
    return {"cartoes": cartoes, "jogadores": jogadores}


def _pct(x: float) -> str:
    return f"{round(x * 100)}%"


def _vezes(n: int) -> str:
    return "1 vez" if n == 1 else f"{n} vezes"


def _leituras(r: dict) -> list[str]:
    n = r["julgamentos"]
    if not n:
        return []
    leituras = []

    acerto = f"{r['acertos']} de {n} vereditos certos ({_pct(r['taxa_acerto'])})"
    if r["taxa_acerto"] >= 0.75:
        leituras.append(f"A turma separou gente de máquina bem acima do acaso: {acerto}. Chutando, daria uns 50%.")
    elif r["taxa_acerto"] >= 0.6:
        leituras.append(f"A turma foi melhor que o acaso, mas sem folga: {acerto}. Chutando, daria uns 50%.")
    elif r["taxa_acerto"] > 0.4:
        leituras.append(f"Perto do acaso: {acerto}. Na prática, a turma não conseguiu separar gente de máquina.")
    else:
        leituras.append(f"Abaixo do acaso: {acerto}. A turma trocou gente por máquina mais vezes do que acertou.")

    m = r["matriz"]
    if r["n_julgamentos_humanos"]:
        if m["humanos_acusados"]:
            leituras.append(
                f"Humanos foram acusados de ser máquina {_vezes(m['humanos_acusados'])} "
                f"({_pct(r['taxa_falsa_acusacao'])} dos vereditos sobre humanos). Numa pesquisa de verdade, "
                "essas respostas seriam descartadas: é o custo de desconfiar."
            )
        else:
            leituras.append("Nenhum humano foi acusado de ser máquina.")

    armadilhas = r["armadilhas"]
    melhor = armadilhas[0] if armadilhas else None
    if melhor and melhor["pegou_agentes"] > melhor["acusou_humanos"]:
        leituras.append(
            f"A pergunta que mais entregou agentes foi a P{melhor['numero']} ({melhor['tipo_rotulo']}), "
            f"marcada como pista certa {_vezes(melhor['pegou_agentes'])}."
        )
    elif m["agentes_pegos"] and not any(a["pegou_agentes"] for a in armadilhas):
        leituras.append(
            "Os agentes foram pegos, mas ninguém apontou uma resposta como pista: "
            "a turma reconheceu pelo conjunto, não por uma pergunta."
        )
    confusa = next((a for a in armadilhas if a["acusou_humanos"] > a["pegou_agentes"]), None)
    if confusa:
        leituras.append(
            f"A P{confusa['numero']} confundiu mais do que ajudou: levou a acusar humanos "
            f"{_vezes(confusa['acusou_humanos'])} e a pegar agentes {_vezes(confusa['pegou_agentes'])}."
        )

    ag = r["agente_mais_convincente"]
    if ag and ag["votos"] >= 2 and ag["votos_maquina"] == 0:
        leituras.append(f"O agente #{ag['rotulo']} passou por humano em todos os {ag['votos']} vereditos que recebeu.")

    if n < 30:
        leituras.append(
            f"Com só {n} vereditos, cada um mexe uns {round(100 / n)} pontos na taxa de acerto: "
            "leia estes números como indício, não como prova."
        )
    return leituras


def resultado_do_juiz(sala: Sala, participante_id: str) -> dict:
    meus = [j for j in sala.julgamentos if j.juiz_id == participante_id and j.respondente_id in sala.respondentes]
    return {"acertos": sum(1 for j in meus if _acertou(sala, j)), "total": len(meus)}
