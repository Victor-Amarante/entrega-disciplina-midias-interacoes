"""Diretórios de ferramentas de IA, varridos pelo sitemap.

Sitemap em vez de raspagem de páginas de listagem: é a via que o próprio site
publica para ser percorrido, custa 3 requisições em vez de 300, e não depende de
seletor de HTML que quebra na próxima reforma do layout.

Estado de cada diretório testado (medido, não suposto):
  futuretools.io   -> sitemap aberto, ~3000 URLs de ferramenta em tools-1..3.xml
  aixploria.com    -> sitemap índice por mês, ~48 meses
  theresanaiforthat.com -> 403 (proteção Cloudflare). NÃO varrido.
  toolify.ai            -> 403 (proteção Cloudflare). NÃO varrido.

Os dois últimos ficam registrados como fonte tentada-e-falha: essa informação
entra no relatório de fontes, porque um buraco conhecido vale mais do que um
buraco silencioso.
"""

from __future__ import annotations

import re

from . import Contexto

NOME = "diretorios"
METODO = (
    "Sitemap XML em vez de raspar páginas de listagem: é a via que o próprio site publica "
    "para ser percorrido, custa 3 requisições em vez de 300 e não depende de seletor de HTML "
    "que quebra na próxima reforma de layout. futuretools: `tools-1..3.xml` (~3.000 URLs). "
    "aixploria: índice mensal com 48 sub-sitemaps. O nome sai do slug da URL; a descrição "
    "não vem no sitemap e só aparece no enriquecimento."
)
VIES = (
    "Diretório vive de tráfego e de listagem paga, então infla wrapper genérico de "
    "GPT e SaaS de marketing, e quase nunca remove link morto. Ordena por quem paga "
    "ou por quem submeteu, nunca por qualidade. Praticamente não tem ferramenta de "
    "pesquisa, acadêmica ou de nicho técnico — o que é exatamente onde simulação de "
    "agentes vive. Cobertura enviesada para produto comercial em inglês. "
    "Além disso, dois dos maiores (theresanaiforthat, toolify) bloqueiam coleta "
    "automatizada com Cloudflare: o recorte comercial que sobra é o dos sites que "
    "deixam passar, não o do mercado."
)

_LOC = re.compile(r"<loc>\s*(.*?)\s*</loc>", re.S)

SITEMAPS: list[tuple[str, str, str]] = [
    # (rótulo, url do sitemap, filtro de caminho que identifica página de ferramenta)
    ("futuretools", "https://futuretools.io/sitemaps/tools-1.xml", "/tools/"),
    ("futuretools", "https://futuretools.io/sitemaps/tools-2.xml", "/tools/"),
    ("futuretools", "https://futuretools.io/sitemaps/tools-3.xml", "/tools/"),
]

INDICES: list[tuple[str, str, str]] = [
    # (rótulo, sitemap índice, filtro dos sub-sitemaps a seguir)
    ("aixploria", "https://www.aixploria.com/en/sitemap.xml", "sitemap-posttype-post"),
]

BLOQUEADOS = [
    ("theresanaiforthat", "https://theresanaiforthat.com/sitemap.xml"),
    ("toolify", "https://www.toolify.ai/sitemap.xml"),
]


def _nome_do_slug(url: str) -> str:
    """O sitemap só dá URL. O nome sai do slug — e o sufixo aleatório do
    futuretools (`-baa3b119`) é removido para não virar parte do nome."""
    slug = url.rstrip("/").rsplit("/", 1)[-1]
    slug = re.sub(r"-[0-9a-f]{6,}$", "", slug)
    return slug.replace("-", " ").replace("_", " ").strip().title()


def _colher(ctx: Contexto, rotulo: str, sitemap: str, filtro: str) -> int:
    r = ctx.cliente.get(sitemap)
    if r.status != 200:
        ctx.log.evento("fonte_falhou", {"fonte": NOME, "consulta": sitemap, "status": r.status})
        return 0
    n = 0
    for loc in _LOC.findall(r.texto):
        if filtro and filtro not in loc:
            continue
        ctx.log.item(NOME, sitemap, {"loc": loc, "diretorio": rotulo})
        ctx.deposito.adicionar(
            nome=_nome_do_slug(loc), url=loc, fonte=f"{NOME}:{rotulo}", consulta=sitemap,
            descricao_fonte="",  # sitemap não traz descrição; vem no enriquecimento
            sinais={"faceta": "amplo_comercial", "via": "sitemap", "diretorio": rotulo},
        )
        n += 1
    return n


def varrer(ctx: Contexto) -> None:
    for rotulo, sitemap, filtro in SITEMAPS:
        if ctx.estado.concluido(NOME, sitemap, 0):
            continue
        _colher(ctx, rotulo, sitemap, filtro)
        ctx.estado.marcar(NOME, sitemap, 0)

    for rotulo, indice, filtro_sub in INDICES:
        r = ctx.cliente.get(indice)
        if r.status != 200:
            ctx.log.evento("fonte_falhou", {"fonte": NOME, "consulta": indice, "status": r.status})
            continue
        subs = [s for s in _LOC.findall(r.texto) if filtro_sub in s]
        for sub in subs[: ctx.limite_paginas * 10]:
            if ctx.estado.concluido(NOME, sub, 0):
                continue
            _colher(ctx, rotulo, sub, "")
            ctx.estado.marcar(NOME, sub, 0)

    # Registra explicitamente o que não deu para varrer.
    for rotulo, url in BLOQUEADOS:
        ctx.log.evento("fonte_bloqueada", {
            "fonte": f"{NOME}:{rotulo}", "url": url,
            "motivo": "403 de proteção anti-bot (Cloudflare) no sitemap",
            "decisao": "não contornado — coleta não burla bloqueio de servidor",
        })
