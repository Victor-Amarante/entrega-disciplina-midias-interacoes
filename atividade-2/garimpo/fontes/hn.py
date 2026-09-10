"""Hacker News via API do Algolia (sem chave, sem cadastro).

Reaproveita a estratégia da Entrega 1, com UMA inversão: lá os links para
`github.com` eram ruído a descartar, porque repositório não é aplicativo. Aqui
o link de repositório é justamente o alvo, então o filtro de lixo mantém
GitHub e continua descartando agregador, rede social e imprensa.
"""

from __future__ import annotations

from urllib.parse import urlencode

from ..consultas import todas
from . import Contexto

NOME = "hn"
METODO = (
    "API de busca do Algolia (`hn.algolia.com/api/v1/search`), sem chave, com as 35 frases "
    "do vocabulário, até 5 páginas de 100 resultados por consulta, filtrando `tags=story`. "
    "O item colhido é a URL externa que a pessoa postou, não a página da discussão. "
    "Diferença em relação à Entrega 1: lá `github.com` entrava na lista de lixo porque "
    "repositório não era o alvo; aqui é o alvo, e só continuam descartados agregador, rede "
    "social e imprensa."
)
VIES = (
    "Bolha do Vale do Silício e anglófona. Premia lançamento sobre maturidade: biblioteca "
    "boa que nunca foi postada simplesmente não existe aqui, e uma mesma ferramenta reaparece "
    "em vários posts. Post com muito voto costuma indicar polêmica, não qualidade. Nada é "
    "indexado sem que um humano tenha submetido, então a cobertura é do que a comunidade "
    "resolveu comentar, não do que existe."
)

BASE = "https://hn.algolia.com/api/v1/search"
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
            url = BASE + "?" + urlencode({"query": termo, "tags": "story",
                                          "hitsPerPage": 100, "page": pagina})
            r = ctx.cliente.get(url)
            if r.status != 200:
                ctx.log.evento("fonte_falhou", {"fonte": NOME, "consulta": termo,
                                                "pagina": pagina, "status": r.status})
                break
            dados = r.json()
            for h in dados.get("hits", []):
                alvo = h.get("url") or ""
                if not alvo:
                    continue
                ctx.log.item(NOME, termo, h)
                if any(d in alvo for d in LIXO):
                    continue
                ctx.deposito.adicionar(
                    nome=h.get("title") or "", url=alvo, fonte=NOME, consulta=termo,
                    descricao_fonte="",
                    sinais={"faceta": faceta, "pontos": h.get("points"),
                            "comentarios": h.get("num_comments"),
                            "data": h.get("created_at"),
                            "hn": f"https://news.ycombinator.com/item?id={h.get('objectID')}"},
                )
            ctx.estado.marcar(NOME, termo, pagina)
            if pagina + 1 >= dados.get("nbPages", 0):
                break
