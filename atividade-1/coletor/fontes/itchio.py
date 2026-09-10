"""itch.io: páginas de navegação por tag.

Não existe API pública para browse, e o robots.txt proíbe `/search`. As páginas
`/games/tag-<tag>` não estão na lista de Disallow, então são a via permitida.
Seletores confirmados na página real: `div.game_cell` > `a.title`,
`div.game_text`, `div.game_author a`. 36 itens por página, paginação por
`?page=N`.

Isto aqui é a única fonte do conjunto que é raspagem de HTML de verdade. É
frágil por natureza: se o itch.io reformar o layout, `game_cell` some e o
adaptador para de colher sem dar erro. Por isso o executar.py avisa quando uma
página vem 200 mas com zero itens.
"""

from __future__ import annotations

from urllib.parse import urlencode

from selectolax.parser import HTMLParser

from ..consultas import TAGS_ITCHIO
from . import Contexto

NOME = "itchio"
METODO = (
    "Única raspagem de HTML de verdade do conjunto — não há API pública de navegação e o "
    "`robots.txt` proíbe `/search`. As páginas `/games/tag-<tag>` não estão na lista de "
    "Disallow, então são a via permitida: 8 tags × até 5 páginas de 36 itens, com os "
    "seletores `div.game_cell` > `a.title` / `div.game_text` / `div.game_author a`, "
    "conferidos na página real antes de escrever o adaptador. Frágil por natureza: se o "
    "layout mudar, o coletor emite `sem_itens` em vez de colher em silêncio."
)
VIES = (
    "É catálogo de jogo indie, não de ferramenta. Traz mundo simulado e experimento "
    "de comportamento emergente que nenhuma outra fonte tem, mas quase nada aqui é "
    "'ferramenta que se usa para trabalhar' — é obra para jogar. A ordenação padrão "
    "premia o que é popular e recente na plataforma, e jogo bom sem tag correta "
    "simplesmente não aparece, porque a navegação depende do autor ter marcado."
)

BASE = "https://itch.io/games/tag-{tag}"


def varrer(ctx: Contexto) -> None:
    for tag in TAGS_ITCHIO:
        for pagina in range(1, ctx.limite_paginas + 1):
            if ctx.estado.concluido(NOME, tag, pagina):
                continue
            url = BASE.format(tag=tag) + "?" + urlencode({"page": pagina})
            r = ctx.cliente.get(url)
            if r.status != 200:
                ctx.log.evento("fonte_falhou", {"fonte": NOME, "consulta": tag,
                                                "pagina": pagina, "status": r.status})
                break
            arvore = HTMLParser(r.texto)
            celulas = arvore.css("div.game_cell")
            if not celulas:
                # 200 com zero item = ou acabou a paginação, ou o seletor quebrou.
                ctx.log.evento("sem_itens", {"fonte": NOME, "consulta": tag,
                                             "pagina": pagina, "url": url,
                                             "aviso": "verificar se div.game_cell ainda existe"})
                ctx.estado.marcar(NOME, tag, pagina)
                break
            for cel in celulas:
                a = cel.css_first("a.title")
                if a is None:
                    continue
                alvo = a.attributes.get("href") or ""
                texto = cel.css_first("div.game_text")
                autor = cel.css_first("div.game_author a")
                bruto = {"href": alvo, "titulo": a.text(strip=True),
                         "texto": texto.text(strip=True) if texto else "",
                         "autor": autor.text(strip=True) if autor else ""}
                ctx.log.item(NOME, tag, bruto)
                ctx.deposito.adicionar(
                    nome=a.text(strip=True), url=alvo, fonte=NOME, consulta=f"tag:{tag}",
                    descricao_fonte=bruto["texto"],
                    sinais={"faceta": "npc_jogos", "tag": tag, "autor": bruto["autor"]},
                )
            ctx.estado.marcar(NOME, tag, pagina)
