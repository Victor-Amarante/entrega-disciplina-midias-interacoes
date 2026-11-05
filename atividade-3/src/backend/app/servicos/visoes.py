"""O que cada tela recebe. O celular do participante nunca vê quem é agente antes do placar."""

from ..config import CONFIG
from ..dominio.modelos import FASES, Participante, Sala
from . import enquete, jogo, placar

FASES_COM_RESULTADO = ("placar", "enquete", "ataque")


def do_participante(sala: Sala, eu: Participante) -> dict:
    fase = sala.fase
    visao: dict = {
        "codigo": sala.codigo,
        "fase": fase,
        "apelido": eu.apelido,
        "participantes": len(sala.participantes),
    }

    if fase == "armadilhas":
        visao["minhas_armadilhas"] = [
            {"id": p.id, "texto": p.texto, "tipo": p.tipo}
            for p in sala.perguntas if p.autor_id == eu.id
        ]
        visao["limite_armadilhas"] = jogo.LIMITE_ARMADILHAS_POR_PESSOA
        visao["armadilhas_encerradas"] = bool(sala.ordem_perguntas)

    if fase == "respostas":
        meu = sala.respondentes.get(f"h-{eu.id}")
        visao["perguntas"] = [{"id": p.id, "texto": p.texto} for p in sala.perguntas_em_ordem()]
        visao["minhas_respostas"] = meu.respostas if meu else {}

    if fase in ("cacada", *FASES_COM_RESULTADO):
        visao["cartoes"] = _cartoes(sala, eu, revelar=fase in FASES_COM_RESULTADO)

    if fase in FASES_COM_RESULTADO:
        visao["meu_resultado"] = placar.resultado_do_juiz(sala, eu.id)

    if fase in ("enquete", "ataque"):
        e = sala.enquete
        visao["enquete"] = {
            "pergunta": e.pergunta,
            "opcao_a": e.opcao_a,
            "opcao_b": e.opcao_b,
            "meu_voto": e.votos.get(eu.id),
        }
    return visao


def _cartoes(sala: Sala, eu: Participante, revelar: bool) -> list[dict]:
    ids = jogo.cartoes_do_juiz(sala, eu.id) if sala.fase == "cacada" else sala.atribuicoes.get(eu.id, [])
    meus = {j.respondente_id: j for j in sala.julgamentos if j.juiz_id == eu.id}
    perguntas = sala.perguntas_em_ordem()
    cartoes = []
    for rid in ids:
        r = sala.respondentes[rid]
        julgamento = meus.get(rid)
        cartao = {
            "id": rid,
            "rotulo": r.rotulo,
            "respostas": [
                {"pergunta_id": p.id, "pergunta": p.texto, "resposta": r.respostas.get(p.id, "")}
                for p in perguntas
            ],
            "meu_veredito": julgamento.veredito if julgamento else None,
            "minha_pista": julgamento.pista_id if julgamento else None,
        }
        if revelar:
            cartao["verdade"] = "maquina" if r.tipo == "agente" else "humano"
            if r.persona:
                cartao["persona"] = r.persona.nome
                cartao["com_busca"] = r.com_busca
        cartoes.append(cartao)
    return cartoes


def do_painel(sala: Sala) -> dict:
    apelidos = {p.id: p.apelido for p in sala.participantes.values()}
    humanos = [r for r in sala.respondentes.values() if r.tipo == "humano"]
    juizes = {j.juiz_id for j in sala.julgamentos}
    concluidos = sum(
        1 for pid, lista in sala.atribuicoes.items()
        if len({j.respondente_id for j in sala.julgamentos if j.juiz_id == pid}) >= len(lista)
    )
    a, b = enquete.contagem(sala)

    visao: dict = {
        "codigo": sala.codigo,
        "fase": sala.fase,
        "fases": FASES,
        "config": sala.config.model_dump(),
        "simulado": CONFIG.simulado,
        "modelo": CONFIG.modelo,
        "participantes": [{"id": p.id, "apelido": p.apelido} for p in sala.participantes.values()],
        "perguntas": [
            {
                "id": p.id,
                "texto": p.texto,
                "tipo": p.tipo,
                "autor": apelidos.get(p.autor_id, "?") if p.autor_id else None,
                "selecionada": p.selecionada,
                "fixa": p.fixa,
                "no_questionario": p.id in sala.ordem_perguntas,
            }
            for p in sala.perguntas
        ],
        "questionario_fechado": bool(sala.ordem_perguntas),
        "respostas_humanas": len(humanos),
        "agentes": [
            {
                "id": r.id,
                "nome": r.persona.nome if r.persona else "",
                "com_busca": r.com_busca,
                "status": r.status,
                "erro": r.erro,
                "segundos": r.segundos,
                "custo_usd": r.custo_usd,
            }
            for r in sala.agentes()
        ],
        "cacada": {
            "julgamentos": len(sala.julgamentos),
            "juizes": len(juizes),
            "juizes_concluidos": concluidos,
            "cartoes_no_jogo": sum(1 for r in sala.respondentes.values() if r.rotulo),
        },
        "enquete": {
            "pergunta": sala.enquete.pergunta,
            "opcao_a": sala.enquete.opcao_a,
            "opcao_b": sala.enquete.opcao_b,
            "votos": a + b,
        },
    }
    if sala.fase in FASES_COM_RESULTADO:
        visao["placar"] = placar.calcular(sala)
    if sala.fase == "ataque":
        visao["ataque"] = enquete.ataque(sala)
    return visao
