"""Hugging Face: MODELOS (API oficial, sem chave).

Inversão em relação à Entrega 1: lá o Space (aplicativo rodando) era o alvo e o
modelo foi descartado por ser "peça de Entrega 2". Aqui é o contrário — modelo
se instala e se chama do código, e portanto é exatamente o objeto desta unidade.

A busca do HF casa SUBSTRING do identificador, não frase. Isso foi medido na
Entrega 1, quando o vocabulário frasal rendeu 3 itens em 41 consultas. Por isso
aqui só entram termos curtos.
"""

from __future__ import annotations

from urllib.parse import urlencode

from ..consultas import TERMOS_CURTOS
from . import Contexto

NOME = "huggingface"
METODO = (
    "`huggingface.co/api/models?search=<termo>&full=true`, sem chave, com os 50 termos "
    "CURTOS do vocabulário e ordenação por downloads. A escolha por termo curto não é "
    "estilo: o parâmetro `search` do HF casa substring do identificador do modelo, e frase "
    "longa devolve quase nada — medido na Entrega 1. De cada modelo saem downloads, "
    "curtidas, biblioteca de origem, tarefa, licença declarada nas tags e data de "
    "atualização."
)
VIES = (
    "Só modelo hospedado na própria Hugging Face: peso fechado de laboratório comercial não "
    "aparece. Modelo não é biblioteca de simulação — é peça que uma simulação chama —, então "
    "esta fonte tende a trazer o INSUMO do tema e não o tema. A ordenação por download "
    "concentra tudo nos mesmos modelos genéricos de uso geral, e a busca por substring traz "
    "muito homônimo: 'agent' casa com qualquer coisa que tenha a palavra no nome do "
    "repositório, inclusive fine-tune sem relação com agentes."
)

API = "https://huggingface.co/api/models"


def varrer(ctx: Contexto) -> None:
    for termo in TERMOS_CURTOS:
        if ctx.estado.concluido(NOME, termo, 0):
            continue
        url = API + "?" + urlencode({"search": termo, "limit": 100, "full": "true",
                                     "sort": "downloads", "direction": -1})
        r = ctx.cliente.get(url)
        if r.status != 200:
            ctx.log.evento("fonte_falhou", {"fonte": NOME, "consulta": termo,
                                            "status": r.status})
            ctx.estado.marcar(NOME, termo, 0)
            continue
        for m in r.json():
            ident = m.get("id")
            if not ident:
                continue
            cartao = m.get("cardData") or {}
            ctx.log.item(NOME, termo, {k: m.get(k) for k in
                                       ("id", "downloads", "likes", "library_name",
                                        "pipeline_tag", "tags", "lastModified")})
            ctx.deposito.adicionar(
                nome=ident, url=f"https://huggingface.co/{ident}",
                fonte=NOME, consulta=termo,
                descricao_fonte=(cartao.get("short_description") or ""),
                sinais={"faceta": "modelo", "downloads": m.get("downloads"),
                        "likes": m.get("likes"),
                        "biblioteca": m.get("library_name"),
                        "tarefa": m.get("pipeline_tag"),
                        "licenca": cartao.get("license"),
                        "atualizado": m.get("lastModified"),
                        "instalacao": f"huggingface_hub / transformers: {ident}"},
            )
        ctx.estado.marcar(NOME, termo, 0)
