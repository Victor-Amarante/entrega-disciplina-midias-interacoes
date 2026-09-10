"""Registros de pacote: npm, crates.io, NuGet, Packagist e RubyGems.

É a fonte mais legítima da Entrega 2: aqui, por construção, tudo é instalável.
Um item deste adaptador já nasce satisfazendo o critério eliminatório E1 do
aluno ("não dá para instalar ou importar"), porque estar no registro É o
empacotamento.

Cada registro tem uma API pública de busca, sem chave, verificada por sondagem
antes de este arquivo ser escrito. As formas de resposta diferem, então há um
extrator por registro e um laço só.

Contagem de download vem de graça em todos eles — e é justamente o desempate
escolhido pelo aluno, num instrumento melhor que a estrela do GitHub: download
mede uso, estrela mede aprovação.
"""

from __future__ import annotations

from urllib.parse import quote, urlencode

from ..consultas import TERMOS_CURTOS
from . import Contexto

NOME = "registros"
METODO = (
    "Uma API pública de busca por registro, sem chave, todas conferidas por sondagem antes "
    "de o adaptador existir: npm (`registry.npmjs.org/-/v1/search`, paginação por `from`), "
    "crates.io (`/api/v1/crates`, paginação por `page`), NuGet "
    "(`azuresearch-usnc.nuget.org/query`, paginação por `skip`), Packagist "
    "(`/search.json`) e RubyGems (`/api/v1/search.json`). São varridos 50 TERMOS CURTOS, "
    "não frases: registro casa substring de nome, descrição e palavra-chave, e frase longa "
    "devolve quase nada — lição medida na Entrega 1, quando a busca do Hugging Face rendeu "
    "3 itens em 41 consultas frasais. De cada pacote saem nome, descrição do autor, "
    "contagem de download, versão, licença quando declarada e link do repositório."
)
VIES = (
    "Só enxerga o que foi EMPACOTADO E PUBLICADO. Código de pesquisa que fica no GitHub sem "
    "release — que é a maior parte do que existe sobre simulação de agentes — é invisível "
    "aqui. Cada registro carrega o viés da sua linguagem: crates.io só tem Rust, NuGet só "
    ".NET, e por isso o Python, que domina simulação científica, aparece sub-representado, "
    "já que o PyPI não pôde ser varrido. A busca ordena por relevância textual e por "
    "popularidade, então pacote novo e bom afunda, e nome genérico ('agents', 'simulation') "
    "traz muito homônimo de outro domínio. Contagem de download infla com dependência "
    "transitiva e com CI: número alto mede quantas máquinas baixaram, não quantas pessoas usaram."
)

TIMEOUT_PAGINAS = 5


def _npm(ctx: Contexto, termo: str, pagina: int) -> int:
    tam = 100
    url = ("https://registry.npmjs.org/-/v1/search?"
           + urlencode({"text": termo, "size": tam, "from": pagina * tam}))
    r = ctx.cliente.get(url)
    if r.status != 200:
        ctx.log.evento("fonte_falhou", {"fonte": "npm", "consulta": termo,
                                        "pagina": pagina, "status": r.status})
        return 0
    objetos = r.json().get("objects", [])
    for o in objetos:
        p = o.get("package") or {}
        nome = p.get("name")
        if not nome:
            continue
        ctx.log.item("npm", termo, {k: p.get(k) for k in
                                    ("name", "version", "description", "keywords", "date", "links")}
                     | {"downloads": o.get("downloads")})
        ctx.deposito.adicionar(
            nome=nome, url=f"https://www.npmjs.com/package/{nome}",
            fonte="npm", consulta=termo,
            descricao_fonte=p.get("description") or "",
            sinais={"registro": "npm", "versao": p.get("version"),
                    "downloads_semana": (o.get("downloads") or {}).get("weekly"),
                    "palavras_chave": p.get("keywords"),
                    "publicado": p.get("date"),
                    "repositorio": (p.get("links") or {}).get("repository"),
                    "instalacao": f"npm install {nome}"},
        )
    return len(objetos)


def _crates(ctx: Contexto, termo: str, pagina: int) -> int:
    url = ("https://crates.io/api/v1/crates?"
           + urlencode({"q": termo, "per_page": 100, "page": pagina + 1}))
    r = ctx.cliente.get(url)
    if r.status != 200:
        ctx.log.evento("fonte_falhou", {"fonte": "crates", "consulta": termo,
                                        "pagina": pagina, "status": r.status})
        return 0
    itens = r.json().get("crates", [])
    for cr in itens:
        nome = cr.get("name")
        if not nome:
            continue
        ctx.log.item("crates", termo, {k: cr.get(k) for k in
                                       ("name", "description", "downloads", "recent_downloads",
                                        "repository", "max_version", "updated_at", "keywords")})
        ctx.deposito.adicionar(
            nome=nome, url=f"https://crates.io/crates/{nome}",
            fonte="crates", consulta=termo,
            descricao_fonte=cr.get("description") or "",
            sinais={"registro": "crates.io", "versao": cr.get("max_version"),
                    "downloads": cr.get("downloads"),
                    "downloads_recentes": cr.get("recent_downloads"),
                    "atualizado": cr.get("updated_at"),
                    "repositorio": cr.get("repository"),
                    "instalacao": f"cargo add {nome}"},
        )
    return len(itens)


def _nuget(ctx: Contexto, termo: str, pagina: int) -> int:
    tam = 100
    url = ("https://azuresearch-usnc.nuget.org/query?"
           + urlencode({"q": termo, "take": tam, "skip": pagina * tam}))
    r = ctx.cliente.get(url)
    if r.status != 200:
        ctx.log.evento("fonte_falhou", {"fonte": "nuget", "consulta": termo,
                                        "pagina": pagina, "status": r.status})
        return 0
    itens = r.json().get("data", [])
    for n in itens:
        ident = n.get("id")
        if not ident:
            continue
        ctx.log.item("nuget", termo, {k: n.get(k) for k in
                                      ("id", "description", "totalDownloads", "version",
                                       "projectUrl", "licenseUrl", "tags", "authors")})
        ctx.deposito.adicionar(
            nome=ident, url=f"https://www.nuget.org/packages/{ident}",
            fonte="nuget", consulta=termo,
            descricao_fonte=n.get("description") or "",
            sinais={"registro": "nuget", "versao": n.get("version"),
                    "downloads": n.get("totalDownloads"),
                    "licenca_url": n.get("licenseUrl"),
                    "repositorio": n.get("projectUrl"),
                    "palavras_chave": n.get("tags"),
                    "instalacao": f"dotnet add package {ident}"},
        )
    return len(itens)


def _packagist(ctx: Contexto, termo: str, pagina: int) -> int:
    url = ("https://packagist.org/search.json?"
           + urlencode({"q": termo, "per_page": 100, "page": pagina + 1}))
    r = ctx.cliente.get(url)
    if r.status != 200:
        ctx.log.evento("fonte_falhou", {"fonte": "packagist", "consulta": termo,
                                        "pagina": pagina, "status": r.status})
        return 0
    itens = r.json().get("results", [])
    for p in itens:
        nome = p.get("name")
        if not nome:
            continue
        ctx.log.item("packagist", termo, {k: p.get(k) for k in
                                          ("name", "description", "downloads", "favers",
                                           "repository", "url")})
        ctx.deposito.adicionar(
            nome=nome, url=p.get("url") or f"https://packagist.org/packages/{nome}",
            fonte="packagist", consulta=termo,
            descricao_fonte=p.get("description") or "",
            sinais={"registro": "packagist", "downloads": p.get("downloads"),
                    "favoritos": p.get("favers"),
                    "repositorio": p.get("repository"),
                    "instalacao": f"composer require {nome}"},
        )
    return len(itens)


def _rubygems(ctx: Contexto, termo: str, pagina: int) -> int:
    url = ("https://rubygems.org/api/v1/search.json?"
           + urlencode({"query": termo, "page": pagina + 1}))
    r = ctx.cliente.get(url)
    if r.status != 200:
        ctx.log.evento("fonte_falhou", {"fonte": "rubygems", "consulta": termo,
                                        "pagina": pagina, "status": r.status})
        return 0
    itens = r.json()
    if not isinstance(itens, list):
        return 0
    for g in itens:
        nome = g.get("name")
        if not nome:
            continue
        ctx.log.item("rubygems", termo, {k: g.get(k) for k in
                                         ("name", "info", "downloads", "version",
                                          "licenses", "source_code_uri", "homepage_uri")})
        ctx.deposito.adicionar(
            nome=nome, url=f"https://rubygems.org/gems/{nome}",
            fonte="rubygems", consulta=termo,
            descricao_fonte=g.get("info") or "",
            sinais={"registro": "rubygems", "versao": g.get("version"),
                    "downloads": g.get("downloads"),
                    "licencas": g.get("licenses"),
                    "repositorio": g.get("source_code_uri") or g.get("homepage_uri"),
                    "instalacao": f"gem install {nome}"},
        )
    return len(itens)


EXTRATORES = {
    "npm": (_npm, 100),
    "crates": (_crates, 100),
    "nuget": (_nuget, 100),
    "packagist": (_packagist, 100),
    "rubygems": (_rubygems, 30),
}


def varrer(ctx: Contexto) -> None:
    for registro, (fn, por_pagina) in EXTRATORES.items():
        for termo in TERMOS_CURTOS:
            for pagina in range(min(ctx.limite_paginas, TIMEOUT_PAGINAS)):
                chave = f"{registro}:{termo}"
                if ctx.estado.concluido(NOME, chave, pagina):
                    continue
                n = fn(ctx, termo, pagina)
                ctx.estado.marcar(NOME, chave, pagina)
                if n < por_pagina:
                    break
