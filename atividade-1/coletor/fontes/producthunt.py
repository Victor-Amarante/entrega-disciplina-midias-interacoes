"""Product Hunt: apenas o feed Atom público.

A API GraphQL (api.producthunt.com/v2/api/graphql) exige token de
desenvolvedor, que o aluno não tem. O que sobra é https://www.producthunt.com/feed,
que devolveu exatamente 50 entradas na sondagem — só os lançamentos recentes,
sem busca, sem filtro por tópico e sem histórico.

Ou seja: esta fonte NÃO cobre o tema da varredura. Ela entra como amostra de
controle — serve para o aluno ver o que o mercado está lançando hoje e perceber
o contraste com o que as fontes temáticas trouxeram. Tratar as 50 entradas como
"varredura do Product Hunt" seria mentira, e o relatório de fontes diz isso.
"""

from __future__ import annotations

import feedparser

from . import Contexto

NOME = "producthunt"
VIES = (
    "Sem token, só o feed dos ~50 lançamentos mais recentes: não há busca nem "
    "histórico, então o tema da varredura não é coberto — o que vier é do dia. "
    "Mesmo com token, o Product Hunt premia lançamento com boa campanha de marketing: "
    "quem tem comunidade sobe, ferramenta sem equipe de divulgação não aparece. "
    "É a fonte mais fraca deste conjunto e está aqui como amostra de contraste."
)

METODO = (
    "Apenas o feed Atom público `producthunt.com/feed`, que devolveu exatamente 50 entradas: "
    "só os lançamentos recentes, sem busca, sem filtro por tópico e sem histórico. A API "
    "GraphQL, que teria busca de verdade, exige token de desenvolvedor que não foi obtido. "
    "Tratar essas 50 entradas como 'varredura do Product Hunt' seria falso."
)

FEED = "https://www.producthunt.com/feed"


def varrer(ctx: Contexto) -> None:
    if ctx.estado.concluido(NOME, "feed", 0):
        return
    r = ctx.cliente.get(FEED)
    if r.status != 200:
        ctx.log.evento("fonte_falhou", {"fonte": NOME, "consulta": FEED, "status": r.status})
        return
    feed = feedparser.parse(r.texto)
    for e in feed.entries:
        ctx.log.item(NOME, "feed", {"title": e.get("title"), "link": e.get("link"),
                                    "updated": e.get("updated")})
        ctx.deposito.adicionar(
            nome=e.get("title") or "", url=e.get("link") or "", fonte=NOME, consulta="feed",
            descricao_fonte=" ".join((e.get("summary") or "").split())[:400],
            sinais={"faceta": "amostra_de_contraste", "data": e.get("updated")},
        )
    ctx.estado.marcar(NOME, "feed", 0)
