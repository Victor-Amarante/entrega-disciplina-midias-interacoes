"""Sondagem: bate UMA vez em cada fonte candidata e relata o que voltou.

Roda antes de escrever qualquer adaptador. Serve para não construir em cima de
suposição: se a API não existe, ou exige chave, ou devolve 403, é melhor
descobrir agora do que no meio da varredura.

Uso:  uv run python atividade-1/sondagem.py
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

import httpx

RAIZ = Path(__file__).parent
for linha in (RAIZ / ".env").read_text().splitlines() if (RAIZ / ".env").exists() else []:
    if "=" in linha and not linha.startswith("#"):
        k, v = linha.split("=", 1)
        os.environ.setdefault(k.strip(), v.strip())

UA = "cin0055-coletor-atividade1/1.0 (+trabalho academico CIn/UFPE)"
TOKEN = os.environ.get("GITHUB_TOKEN", "")

ALVOS: list[tuple[str, str, dict]] = [
    ("hn_algolia",
     "https://hn.algolia.com/api/v1/search?query=multi-agent+simulation&tags=story&hitsPerPage=3", {}),
    ("arxiv",
     "http://export.arxiv.org/api/query?search_query=all:%22generative+agents%22&max_results=3", {}),
    ("hf_spaces",
     "https://huggingface.co/api/spaces?search=agent+simulation&limit=3&full=true", {}),
    ("hf_models",
     "https://huggingface.co/api/models?search=agent&limit=3", {}),
    ("hf_papers",
     "https://huggingface.co/api/daily_papers?limit=3", {}),
    ("github_search",
     "https://api.github.com/search/repositories?q=multi-agent+simulation&per_page=3",
     {"Authorization": f"Bearer {TOKEN}", "Accept": "application/vnd.github+json"} if TOKEN else {}),
    ("producthunt_rss", "https://www.producthunt.com/feed", {}),
    ("producthunt_api_sem_chave",
     "https://api.producthunt.com/v2/api/graphql", {}),
    ("reddit_json",
     "https://www.reddit.com/r/LLMDevs/search.json?q=simulation&restrict_sr=1&limit=3", {}),
    ("reddit_rss",
     "https://www.reddit.com/r/MachineLearning/search.rss?q=agent+simulation&restrict_sr=1", {}),
    ("itchio_html", "https://itch.io/games/tag-artificial-intelligence", {}),
    ("itchio_robots", "https://itch.io/robots.txt", {}),
    ("taaft_robots", "https://theresanaiforthat.com/robots.txt", {}),
    ("aixploria_robots", "https://www.aixploria.com/en/robots.txt", {}),
    ("futuretools_robots", "https://www.futuretools.io/robots.txt", {}),
    ("toolify_robots", "https://www.toolify.ai/robots.txt", {}),
    ("jina_reader", "https://r.jina.ai/https://example.com", {}),
    ("lobsters_json", "https://lobste.rs/search.json?q=agent&what=stories", {}),
]


def resumo(nome: str, texto: str) -> str:
    t = texto.strip()
    if not t:
        return "(vazio)"
    if t.startswith("{") or t.startswith("["):
        try:
            d = json.loads(t)
        except Exception:
            return "json inválido: " + t[:120].replace("\n", " ")
        if isinstance(d, list):
            chaves = sorted(d[0].keys())[:8] if d and isinstance(d[0], dict) else []
            return f"lista[{len(d)}] chaves={chaves}"
        if isinstance(d, dict):
            miolo = ""
            for k in ("hits", "items", "data", "children"):
                if k in d and isinstance(d[k], list):
                    miolo = f" {k}=[{len(d[k])}]"
                    break
                if k in d and isinstance(d.get(k), dict) and isinstance(d[k].get("children"), list):
                    miolo = f" {k}.children=[{len(d[k]['children'])}]"
                    break
            return f"dict chaves={sorted(d.keys())[:8]}{miolo}"
    return t[:160].replace("\n", " ⏎ ")


def main() -> None:
    cliente = httpx.Client(headers={"User-Agent": UA}, timeout=30.0, follow_redirects=True)
    largura = max(len(n) for n, _, _ in ALVOS)
    for nome, url, headers in ALVOS:
        try:
            r = cliente.get(url, headers=headers)
            marca = "ok " if r.status_code == 200 else "!! "
            print(f"{marca}{nome:<{largura}}  {r.status_code}  {resumo(nome, r.text)}")
            if nome == "github_search" and "X-RateLimit-Limit" in r.headers:
                print(f"   {'':<{largura}}  cota github: {r.headers['X-RateLimit-Remaining']}"
                      f"/{r.headers['X-RateLimit-Limit']} por hora")
        except Exception as e:
            print(f"XX {nome:<{largura}}  ---  {type(e).__name__}: {e}")
    cliente.close()


if __name__ == "__main__":
    sys.exit(main())
