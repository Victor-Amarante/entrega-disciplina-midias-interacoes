"""Hacker News via API do Algolia (sem chave, sem cadastro).

Paginação: `page` de 0 a nbPages-1, `hitsPerPage` até 1000 (usamos 100 para não
pedir respostas gigantes). O item interessante é `url` — o link externo que a
pessoa postou —, não a página da discussão.
"""

from __future__ import annotations

from urllib.parse import urlencode

from ..consultas import todas
from . import Contexto

NOME = "hn"
METODO = (
    "API de busca do Algolia (`hn.algolia.com/api/v1/search`), sem chave e sem cadastro. "
    "41 termos frasais do vocabulário, até 5 páginas de 100 resultados cada, filtrando "
    "`tags=story`. O item colhido é a URL EXTERNA que a pessoa postou, não a página da "
    "discussão. Descarta 24 domínios de agregador e rede social, que dominam qualquer "
    "busca do HN sem serem ferramenta."
)
VIES = (
    "Bolha do Vale do Silício e anglófona. Premia lançamento sobre maturidade: "
    "ferramenta boa de 2021 que nunca foi postada simplesmente não existe aqui. "
    "O mesmo produto reaparece em vários posts, e post com muito voto costuma ser "
    "polêmica, não qualidade. Não indexa nada que não tenha sido submetido por um humano."
)

BASE = "https://hn.algolia.com/api/v1/search"
# Domínios que são discussão/agregador, não ferramenta. Entram como ruído em
# quase toda busca do HN.
LIXO = {
    "news.ycombinator.com", "twitter.com", "x.com", "medium.com", "substack.com",
    "youtube.com", "youtu.be", "reddit.com", "linkedin.com", "nytimes.com",
    "theverge.com", "techcrunch.com", "wired.com", "arstechnica.com",
}


def varrer(ctx: Contexto) -> None:
    for faceta, termo in todas():
        for pagina in range(ctx.limite_paginas):
            if ctx.estado.concluido(NOME, termo, pagina):
                continue
            url = BASE + "?" + urlencode({
                "query": termo, "tags": "story", "hitsPerPage": 100, "page": pagina,
            })
            r = ctx.cliente.get(url)
            if r.status != 200:
                ctx.log.evento("fonte_falhou", {"fonte": NOME, "consulta": termo,
                                                "pagina": pagina, "status": r.status})
                break
            dados = r.json()
            hits = dados.get("hits", [])
            for h in hits:
                alvo = h.get("url") or ""
                if not alvo:
                    continue
                ctx.log.item(NOME, termo, h)
                if any(d in alvo for d in LIXO):
                    continue
                ctx.deposito.adicionar(
                    nome=h.get("title") or "",
                    url=alvo,
                    fonte=NOME,
                    consulta=termo,
                    descricao_fonte="",  # HN não dá descrição; só título do post
                    sinais={"faceta": faceta, "pontos": h.get("points"),
                            "comentarios": h.get("num_comments"),
                            "data": h.get("created_at"),
                            "hn": f"https://news.ycombinator.com/item?id={h.get('objectID')}"},
                )
            ctx.estado.marcar(NOME, termo, pagina)
            if pagina + 1 >= dados.get("nbPages", 0):
                break
