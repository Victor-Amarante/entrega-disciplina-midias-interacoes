"""Hugging Face: Spaces, Models e Papers (API oficial, sem chave).

Spaces são a parte mais legítima desta fonte para a Entrega 1: um Space é um
aplicativo rodando, com URL que abre no navegador. Models e Papers entram como
lead — um modelo não é ferramenta que se usa, é peça de Entrega 2 —, mas o
`cardData` frequentemente aponta para a demo hospedada.

Paginação por cursor: a API devolve o cabeçalho `Link` com rel="next".
Aqui usamos o modo simples com `limit` + `search`, que já satura o assunto.
"""

from __future__ import annotations

from urllib.parse import urlencode

from ..consultas import TERMOS_CURTOS_HF, todas
from . import Contexto

NOME = "huggingface"
METODO = (
    "API oficial, sem chave. **Spaces**: `api/spaces?search=` com 44 termos CURTOS — a "
    "busca do HF casa substring do identificador, não frase, e o vocabulário frasal "
    "rendia 3 itens em 41 consultas. **Papers**: `api/papers/search?q=` com os 41 termos "
    "frasais, que aí funcionam. Na verificação, cada Space é reconsultado em "
    "`api/spaces/<id>`, que devolve `runtime.stage` (RUNNING / SLEEPING / erro de build) "
    "— sinal de vida melhor do que um GET na página, que responde 200 até para Space quebrado."
)
VIES = (
    "Só existe o que é aberto e hospedado na própria HF. Todo produto comercial "
    "fechado — que é a maioria do que 'se abre e usa' — é invisível aqui. "
    "Spaces morrem: muitos ficam em 'Sleeping' ou com build quebrado e a API não "
    "diferencia isso de um app vivo. Enviesado para demo de pesquisa em Gradio."
)

API = "https://huggingface.co/api"


def _varrer_spaces(ctx: Contexto, faceta: str, termo: str) -> None:
    url = f"{API}/spaces?" + urlencode({"search": termo, "limit": 100, "full": "true",
                                        "sort": "likes", "direction": -1})
    r = ctx.cliente.get(url)
    if r.status != 200:
        ctx.log.evento("fonte_falhou", {"fonte": NOME, "consulta": termo, "status": r.status})
        return
    for s in r.json():
        ident = s.get("id") or ""
        if not ident:
            continue
        ctx.log.item(NOME + ":space", termo, s)
        cartao = s.get("cardData") or {}
        ctx.deposito.adicionar(
            nome=cartao.get("title") or ident,
            url=f"https://huggingface.co/spaces/{ident}",
            fonte=NOME + ":space", consulta=termo,
            descricao_fonte=(cartao.get("short_description") or ""),
            sinais={"faceta": faceta, "tipo": "space", "likes": s.get("likes"),
                    "sdk": s.get("sdk"), "estado": (s.get("runtime") or {}).get("stage"),
                    "atualizado": s.get("lastModified")},
        )


def _varrer_papers(ctx: Contexto, faceta: str, termo: str) -> None:
    url = f"{API}/papers/search?" + urlencode({"q": termo})
    r = ctx.cliente.get(url)
    if r.status != 200:
        return
    for p in r.json():
        paper = p.get("paper") or {}
        pid = paper.get("id")
        if not pid:
            continue
        ctx.log.item(NOME + ":paper", termo, p)
        ctx.deposito.adicionar(
            nome=paper.get("title") or pid,
            url=f"https://huggingface.co/papers/{pid}",
            fonte=NOME + ":paper", consulta=termo,
            descricao_fonte=" ".join((paper.get("summary") or "").split())[:600],
            sinais={"faceta": faceta, "tipo": "paper", "upvotes": paper.get("upvotes"),
                    "data": paper.get("publishedAt")},
        )


def varrer(ctx: Contexto) -> None:
    # Spaces: termos CURTOS (a busca é por substring do id — ver consultas.py).
    for termo in TERMOS_CURTOS_HF:
        if not ctx.estado.concluido(NOME + ":space", termo, 0):
            _varrer_spaces(ctx, "sandbox_ambiente", termo)
            ctx.estado.marcar(NOME + ":space", termo, 0)
    # Papers: aceita frase, então usa o vocabulário facetado normal.
    for faceta, termo in todas():
        if not ctx.estado.concluido(NOME + ":paper", termo, 0):
            _varrer_papers(ctx, faceta, termo)
            ctx.estado.marcar(NOME + ":paper", termo, 0)
