"""arXiv via API oficial (sem chave).

Duas coisas saem daqui, e a segunda é a que importa para a Entrega 1:
  1. o próprio paper (link /abs/ — lead, não ferramenta);
  2. as URLs de projeto/demo que os autores colam no resumo (project page,
     github.io, site do experimento). É por aí que "sociedade simulada de
     agentes" vira algo que se abre no navegador.

A API pede no mínimo 3 s entre requisições; quem ignora leva 429 — comprovado
na sondagem. O intervalo é forçado no executar.py.
"""

from __future__ import annotations

import re
from urllib.parse import urlencode

import feedparser

from ..consultas import todas
from . import Contexto

NOME = "arxiv"
METODO = (
    "API oficial `export.arxiv.org/api/query`, 41 termos entre aspas, até 2 páginas de 100. "
    "Além do paper, extrai por expressão regular as URLs de projeto/demo que os autores colam "
    "no resumo, ignorando domínios de publicação — é por aí que trabalho de pesquisa vira "
    "algo que se abre no navegador. "
    "**RESULTADO REAL: praticamente nada.** 65 requisições, 39 respostas 429, 25 falhas de "
    "rede e 1 sucesso, mesmo com 12 s entre chamadas (a documentação pede 3 s). O IP ficou "
    "limitado e a fonte foi abandonada. O adaptador funciona; o servidor é que não deixou."
)
VIES = (
    "Só mostra o que virou publicação. Protótipo comercial, app fechado e produto "
    "de empresa não aparecem nunca. A data diz quando o paper saiu, não se o projeto "
    "está vivo — muita coisa aqui é código que rodou uma vez para a figura 4. "
    "Enviesado para inglês e para instituição com verba de publicação."
)

BASE = "http://export.arxiv.org/api/query"
POR_PAGINA = 100
_URL_NO_RESUMO = re.compile(r"https?://[^\s<>\"'\)\]},]+")
# Domínios que aparecem no resumo mas não são o projeto.
IGNORAR = ("arxiv.org", "doi.org", "creativecommons.org", "acm.org", "ieee.org",
           "springer.com", "openreview.net", "semanticscholar.org")


def varrer(ctx: Contexto) -> None:
    for faceta, termo in todas():
        for pagina in range(ctx.limite_paginas):
            if ctx.estado.concluido(NOME, termo, pagina):
                continue
            url = BASE + "?" + urlencode({
                "search_query": f'all:"{termo}"',
                "start": pagina * POR_PAGINA,
                "max_results": POR_PAGINA,
                "sortBy": "relevance",
            })
            r = ctx.cliente.get(url)
            if r.status != 200:
                ctx.log.evento("fonte_falhou", {"fonte": NOME, "consulta": termo,
                                                "pagina": pagina, "status": r.status})
                break
            feed = feedparser.parse(r.texto)
            if not feed.entries:
                ctx.estado.marcar(NOME, termo, pagina)
                break
            for e in feed.entries:
                bruto = {"id": e.get("id"), "title": e.get("title"),
                         "published": e.get("published"), "summary": e.get("summary", "")[:2000]}
                ctx.log.item(NOME, termo, bruto)
                titulo = " ".join((e.get("title") or "").split())
                # 1) o paper
                ctx.deposito.adicionar(
                    nome=titulo, url=e.get("id") or "", fonte=NOME, consulta=termo,
                    descricao_fonte=" ".join((e.get("summary") or "").split())[:600],
                    sinais={"faceta": faceta, "tipo": "paper", "data": e.get("published")},
                )
                # 2) as URLs de projeto escondidas no resumo
                for achado in _URL_NO_RESUMO.findall(e.get("summary") or ""):
                    achado = achado.rstrip(".,;")
                    if any(d in achado for d in IGNORAR):
                        continue
                    ctx.deposito.adicionar(
                        nome=titulo, url=achado, fonte=NOME + ":projeto", consulta=termo,
                        descricao_fonte=" ".join((e.get("summary") or "").split())[:600],
                        sinais={"faceta": faceta, "tipo": "projeto_do_paper",
                                "paper": e.get("id"), "data": e.get("published")},
                    )
            ctx.estado.marcar(NOME, termo, pagina)
            if len(feed.entries) < POR_PAGINA:
                break
