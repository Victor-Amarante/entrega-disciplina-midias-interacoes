"""GitHub Search API (autenticada por token).

Truque que faz esta fonte valer para a Entrega 1: o campo `homepage` do
repositório costuma apontar para o app hospedado. Quando ele existe, é ELE que
entra como candidato de inspiração; o repositório fica como sinal. Quando não
existe, o item entra marcado como `so_repo=True` — e aí é candidato de
Entrega 2, não desta.

Limites reais medidos na sondagem: 30 requisições/minuto na API de busca com
token (10/min sem token), e no máximo 1000 resultados por consulta
(10 páginas de 100).
"""

from __future__ import annotations

from urllib.parse import urlencode

from ..consultas import CONSULTAS_GITHUB
from . import Contexto

# Qual faceta do vocabulário cada consulta do GitHub representa. Sem isto o
# candidato chega ao documento das 500 sem categoria.
FACETA_DA_CONSULTA = {
    "generative agents simulation": "sociedade_simulada",
    "multi agent simulation llm": "sociedade_simulada",
    "agent based model web": "abm_classico",
    "ai town": "sociedade_simulada",
    "agent sandbox llm": "sandbox_ambiente",
    "npc ai llm game": "npc_jogos",
    "agent observability trace": "observabilidade_replay",
    "social simulation agents": "sociedade_simulada",
}

NOME = "github"
METODO = (
    "Search API autenticada por token pessoal (30 requisições/minuto contra 10 sem token). "
    "8 consultas × até 5 páginas de 100, ordenadas por estrelas; a API limita a 1000 "
    "resultados por consulta. O truque que faz esta fonte servir à Entrega 1: colhe o campo "
    "`homepage` do repositório, que costuma apontar para o app hospedado. Sem homepage, o "
    "item é marcado `so_repo` e reprovado no critério E1."
)
VIES = (
    "Só código aberto e só o que está no GitHub. Mede popularidade de "
    "desenvolvedor (estrela), não utilidade para quem usa: repositório de tutorial "
    "com 30 mil estrelas empata com ferramenta real. Repositório arquivado e "
    "abandonado aparece igual a projeto ativo se não olhar a data. "
    "Por natureza puxa para Entrega 2, não para Entrega 1."
)

BASE = "https://api.github.com/search/repositories"
POR_PAGINA = 100
MAX_PAGINAS = 10  # limite duro da API: 1000 resultados por consulta


def varrer(ctx: Contexto) -> None:
    if not ctx.token_github:
        ctx.log.evento("fonte_pulada", {"fonte": NOME, "motivo": "sem GITHUB_TOKEN"})
        return
    cabecalhos = {
        "Authorization": f"Bearer {ctx.token_github}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    for termo in CONSULTAS_GITHUB:
        for pagina in range(1, min(ctx.limite_paginas, MAX_PAGINAS) + 1):
            if ctx.estado.concluido(NOME, termo, pagina):
                continue
            url = BASE + "?" + urlencode({
                "q": termo, "per_page": POR_PAGINA, "page": pagina, "sort": "stars",
            })
            r = ctx.cliente.get(url, headers=cabecalhos)
            if r.status != 200:
                ctx.log.evento("fonte_falhou", {"fonte": NOME, "consulta": termo,
                                                "pagina": pagina, "status": r.status})
                break
            itens = r.json().get("items", [])
            for repo in itens:
                ctx.log.item(NOME, termo, {k: repo.get(k) for k in
                                           ("full_name", "html_url", "homepage", "description",
                                            "stargazers_count", "pushed_at", "archived",
                                            "topics", "license")})
                site = (repo.get("homepage") or "").strip()
                sinais = {
                    "faceta": FACETA_DA_CONSULTA.get(termo, "sandbox_ambiente"),
                    "estrelas": repo.get("stargazers_count"),
                    "ultimo_push": repo.get("pushed_at"),
                    "arquivado": repo.get("archived"),
                    "topicos": repo.get("topics"),
                    "repo": repo.get("html_url"),
                    "so_repo": not bool(site),
                }
                ctx.deposito.adicionar(
                    nome=repo.get("full_name") or "",
                    url=site or repo.get("html_url") or "",
                    fonte=NOME, consulta=termo,
                    descricao_fonte=repo.get("description") or "",
                    sinais=sinais,
                )
            ctx.estado.marcar(NOME, termo, pagina)
            if len(itens) < POR_PAGINA:
                break
