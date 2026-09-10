"""Reddit via RSS de busca por subreddit.

O caminho óbvio (`/search.json`) devolve 403 para requisição sem OAuth — medido
na sondagem. O feed `.rss` do MESMO endpoint responde 200. É a via documentada
e pública, então é a que usamos; não há burla de bloqueio aqui.

O que interessa não é o post, é o link externo que o post cita. O `content` do
feed vem em HTML e é dali que saem as URLs.
"""

from __future__ import annotations

import re
from urllib.parse import urlencode

import feedparser

from ..consultas import SUBREDDITS, todas
from . import Contexto

NOME = "reddit"

# ---------------------------------------------------------------------------
# FONTE DESATIVADA — decisão registrada, não bug.
#
# Medido: https://www.reddit.com/robots.txt responde, para User-agent: *,
# "Disallow: /". Ou seja, o Reddit proíbe coleta automatizada de TODO o site,
# inclusive dos feeds .rss. A via legítima é a API OAuth, que exige credencial
# de aplicativo que o aluno não tem.
#
# Não existe caminho educado aqui. O coletor obedece e não varre. A fonte fica
# no repositório, com o adaptador escrito e funcional, porque a ausência dela
# na lista final precisa ser explicável — e é: foi bloqueio de política, não
# falha técnica. Trocar DESATIVADA para False religa o adaptador.
# ---------------------------------------------------------------------------
DESATIVADA = True
MOTIVO_DESATIVACAO = (
    "reddit.com/robots.txt: 'User-agent: * / Disallow: /'. Coleta automatizada "
    "proibida pelo próprio site; a API oficial exige OAuth. Fonte não varrida."
)

METODO = (
    "NÃO VARRIDO. O adaptador está escrito e testado — usaria o feed `search.rss` por "
    "subreddit (o endpoint `.json` devolve 403 sem OAuth), 10 subreddits × 9 termos, "
    "extraindo os links externos citados no corpo dos posts. Ficou desativado ao ler o "
    "`robots.txt`, que proíbe coleta automatizada do site inteiro."
)
VIES = (
    "Mede o que dá assunto em fórum, não o que é bom: post engraçado e drama sobem, "
    "ferramenta útil e discreta some. Cada subreddit tem sua igreja "
    "(r/LocalLLaMA só enxerga modelo local, r/gamedev só enxerga jogo). "
    "A busca por RSS devolve poucos itens por consulta e não pagina de verdade, "
    "então esta fonte é rasa por construção — serve de complemento, não de base."
)

BASE = "https://www.reddit.com/r/{sub}/search.rss"
_LINK = re.compile(r'href="(https?://[^"]+)"')
IGNORAR = ("reddit.com", "redd.it", "redditstatic.com", "redditmedia.com", "imgur.com")


def varrer(ctx: Contexto) -> None:
    if DESATIVADA:
        ctx.log.evento("fonte_bloqueada", {"fonte": NOME, "url": "https://www.reddit.com/robots.txt",
                                           "motivo": MOTIVO_DESATIVACAO,
                                           "decisao": "não varrido — robots proíbe"})
        return
    # Reddit é raso: uma consulta por (subreddit, termo) explodiria em milhares de
    # requisições para pouco retorno. Usamos um termo por faceta.
    termos = []
    vistas = set()
    for faceta, termo in todas():
        if faceta not in vistas:
            termos.append((faceta, termo))
            vistas.add(faceta)

    for sub in SUBREDDITS:
        for faceta, termo in termos:
            if ctx.estado.concluido(NOME, f"{sub}:{termo}", 0):
                continue
            url = BASE.format(sub=sub) + "?" + urlencode({
                "q": termo, "restrict_sr": "on", "sort": "relevance", "t": "all",
            })
            r = ctx.cliente.get(url)
            if r.status != 200:
                ctx.log.evento("fonte_falhou", {"fonte": NOME, "consulta": f"{sub}:{termo}",
                                                "status": r.status})
                continue
            feed = feedparser.parse(r.texto)
            for e in feed.entries:
                ctx.log.item(NOME, f"{sub}:{termo}",
                             {"title": e.get("title"), "link": e.get("link"),
                              "updated": e.get("updated")})
                conteudo = ""
                if e.get("content"):
                    conteudo = e["content"][0].get("value", "")
                for achado in _LINK.findall(conteudo):
                    if any(d in achado for d in IGNORAR):
                        continue
                    ctx.deposito.adicionar(
                        nome=" ".join((e.get("title") or "").split()),
                        url=achado, fonte=NOME, consulta=f"{sub}:{termo}",
                        descricao_fonte="",
                        sinais={"faceta": faceta, "subreddit": sub,
                                "post": e.get("link"), "data": e.get("updated")},
                    )
            ctx.estado.marcar(NOME, f"{sub}:{termo}", 0)
