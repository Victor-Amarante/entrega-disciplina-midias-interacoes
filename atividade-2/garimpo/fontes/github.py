"""GitHub: busca por texto e por TÓPICO (API oficial, autenticada por token).

Inversão em relação à Entrega 1: lá o repositório era descartado pelo critério
E1 ("não dá para abrir e usar") e só interessava o campo `homepage`. Aqui o
repositório É a ferramenta, e a homepage vira sinal secundário.

Duas varreduras diferentes rodam aqui, de propósito:
  - busca por texto, que encontra o que está escrito na descrição;
  - busca por TÓPICO, que é curadoria feita pelo próprio autor do repositório e
    alcança projeto cuja descrição não usa as palavras que eu escolhi.
"""

from __future__ import annotations

from urllib.parse import urlencode

from ..consultas import CONSULTAS_GITHUB, FACETA_DA_CONSULTA_GITHUB, TOPICOS_GITHUB
from . import Contexto

NOME = "github"
METODO = (
    "Search API autenticada por token pessoal (30 requisições/minuto contra 10 sem token), "
    "em duas passadas: 10 consultas de TEXTO e 21 consultas por TÓPICO (`topic:<nome>`), "
    "cada uma até 5 páginas de 100 resultados, ordenadas por estrelas — a API limita a 1000 "
    "resultados por consulta. A passada por tópico existe porque tópico é curadoria do "
    "próprio autor e alcança repositório cuja descrição não usa as palavras do meu "
    "vocabulário. De cada repositório saem estrelas, licença declarada, linguagem, data do "
    "último push, se está arquivado, os tópicos e a homepage."
)
VIES = (
    "Só código aberto, e só o que está no GitHub — GitLab, Codeberg e código corporativo "
    "fechado não existem aqui. Estrela mede aprovação de desenvolvedor, não qualidade nem "
    "uso: repositório de tutorial e lista de links acumulam mais estrela que biblioteca séria "
    "de nicho. Ordenar por estrela enterra projeto novo e bom. A busca por tópico depende de "
    "o autor ter marcado o repositório, então quem não marca fica invisível por esse caminho. "
    "E repositório arquivado ou parado aparece igual a projeto ativo se ninguém olhar a data."
)

BASE = "https://api.github.com/search/repositories"
POR_PAGINA = 100
MAX_PAGINAS = 10


def _colher(ctx: Contexto, consulta: str, faceta: str, rotulo: str, cabecalhos: dict) -> None:
    for pagina in range(1, min(ctx.limite_paginas, MAX_PAGINAS) + 1):
        if ctx.estado.concluido(NOME, f"{rotulo}:{consulta}", pagina):
            continue
        url = BASE + "?" + urlencode(
            {"q": consulta, "per_page": POR_PAGINA, "page": pagina, "sort": "stars"})
        r = ctx.cliente.get(url, headers=cabecalhos)
        if r.status != 200:
            ctx.log.evento("fonte_falhou", {"fonte": NOME, "consulta": consulta,
                                            "pagina": pagina, "status": r.status})
            break
        itens = r.json().get("items", [])
        for repo in itens:
            bruto = {k: repo.get(k) for k in
                     ("full_name", "html_url", "homepage", "description", "stargazers_count",
                      "pushed_at", "archived", "topics", "language", "forks_count",
                      "open_issues_count")}
            bruto["license"] = (repo.get("license") or {}).get("spdx_id")
            ctx.log.item(NOME, consulta, bruto)
            ctx.deposito.adicionar(
                nome=repo.get("full_name") or "",
                url=repo.get("html_url") or "",
                fonte=NOME, consulta=consulta,
                descricao_fonte=repo.get("description") or "",
                sinais={"faceta": faceta, "via": rotulo,
                        "estrelas": repo.get("stargazers_count"),
                        "forks": repo.get("forks_count"),
                        "linguagem": repo.get("language"),
                        "licenca": bruto["license"],
                        "ultimo_push": repo.get("pushed_at"),
                        "arquivado": repo.get("archived"),
                        "topicos": repo.get("topics"),
                        "site": repo.get("homepage")},
            )
        ctx.estado.marcar(NOME, f"{rotulo}:{consulta}", pagina)
        if len(itens) < POR_PAGINA:
            break


def varrer(ctx: Contexto) -> None:
    if not ctx.token_github:
        ctx.log.evento("fonte_pulada", {"fonte": NOME, "motivo": "sem GITHUB_TOKEN"})
        return
    cab = {"Authorization": f"Bearer {ctx.token_github}",
           "Accept": "application/vnd.github+json",
           "X-GitHub-Api-Version": "2022-11-28"}
    for consulta in CONSULTAS_GITHUB:
        _colher(ctx, consulta, FACETA_DA_CONSULTA_GITHUB.get(consulta, "abm_framework"),
                "texto", cab)
    for topico in TOPICOS_GITHUB:
        _colher(ctx, f"topic:{topico}", "topico:" + topico, "topico", cab)
