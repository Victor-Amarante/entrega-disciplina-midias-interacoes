"""Fase D — repontuar sobre o TEXTO REAL da página e montar a fila das 500.

Diferença crucial em relação a `peneirar.py`: lá a pontuação olhava o nome, a
URL e a descrição que a FONTE deu (quando dava). Aqui ela olha o que está
escrito na página da própria ferramenta, buscada e verificada em
`enriquecer.py`. É a diferença entre "o slug tem a palavra agent" e "a página
diz o que a coisa faz".

Os critérios continuam sendo os de Victor:
  E1 não se abre e usa · E2 agente único · E3 paywall antes de ver
  P1 múltiplos agentes · P2 ver por dentro · P3 configurável · P4 analisável

E continua valendo o limite honesto: E2 e E3 são SUSPEITAS marcadas por regex
sobre o texto real, não vereditos. O veredito final é leitura humana (ou
julgamento em lote assistido) sobre os campos que este script deixa prontos.

Saídas:
  dados/ranqueado.jsonl        — tudo, ordenado, com nota e evidência
  dados/para_descrever.jsonl   — os N do topo, com o texto da página junto,
                                 prontos para virar as três frases exigidas
  dados/relatorio_julgamento.md

Uso:
    uv run python atividade-1/julgar.py
    uv run python atividade-1/julgar.py --desempate raridade --quantos 500
"""

from __future__ import annotations

import argparse
import collections
import json
from datetime import datetime
from pathlib import Path

import sys

RAIZ = Path(__file__).parent
sys.path.insert(0, str(RAIZ))
DADOS = RAIZ / "dados"

from peneirar import (  # noqa: E402
    P1_MULTIAGENTE, P2_VER_POR_DENTRO, P3_CONFIGURAVEL, P4_ANALISAVEL,
    S_AGENTE_UNICO, S_PAYWALL, PESOS, chave_desempate,
)

# Sinais de página que não é ferramenta nenhuma — só aparecem depois de abrir.
MORTA = ("404", "not found", "page not found", "this space is sleeping",
         "domain is for sale", "buy this domain", "coming soon",
         "account suspended", "site cannot be reached", "runtime error",
         "build error", "configuration error")


def texto_real(c: dict) -> str:
    p = c.get("pagina") or {}
    return " ".join([c.get("nome", ""), p.get("titulo", ""), p.get("meta", ""),
                     p.get("corpo", "")])


def julgar(c: dict) -> dict:
    t = texto_real(c)
    tl = t.lower()
    ev = {
        "P1": bool(P1_MULTIAGENTE.search(t)),
        "P2": bool(P2_VER_POR_DENTRO.search(t)),
        "P3": bool(P3_CONFIGURAVEL.search(t)),
        "P4": bool(P4_ANALISAVEL.search(t)),
    }
    nota = sum(PESOS[k] for k, v in ev.items() if v)

    ver = c.get("verificacao") or {}
    ev["link_vivo"] = bool(ver.get("vivo"))
    ev["status"] = ver.get("status")
    ev["pagina_morta"] = any(m in tl[:1500] for m in MORTA)
    ev["texto_curto"] = len((c.get("pagina") or {}).get("corpo", "")) < 200
    ev["suspeita_agente_unico"] = bool(S_AGENTE_UNICO.search(t))
    ev["suspeita_paywall"] = bool(S_PAYWALL.search(t))

    # Link morto não é eliminatório para o Victor (ele escolheu NÃO reprovar por
    # isso), mas página que não carregou não dá evidência de nada — então ela
    # não pode competir de igual para igual com quem foi verificado. Penalidade,
    # não eliminação: a decisão dele fica preservada e o ranking fica honesto.
    if not ev["link_vivo"] or ev["pagina_morta"]:
        nota -= 4.0
    if ev["texto_curto"]:
        nota -= 1.5
    if ev["suspeita_agente_unico"]:
        nota -= 2.0   # é critério eliminatório dele; aqui vira empurrão para baixo
    if ev["suspeita_paywall"]:
        nota -= 1.0

    c["nota"] = round(nota, 2)
    c["evidencia"] = ev
    return c


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--desempate", default="popularidade",
                   choices=["popularidade", "raridade", "vida", "faceta"])
    p.add_argument("--quantos", type=int, default=500)
    args = p.parse_args()

    # `enriquecidos.jsonl` é histórico e só cresce: guarda tudo que já foi
    # aberto, inclusive itens que uma versão POSTERIOR da peneira passou a
    # reprovar. Quem manda é a pré-seleção atual — senão um critério novo do
    # aluno não teria efeito nenhum sobre o que já foi enriquecido.
    validos = set()
    pre = DADOS / "preselecao.jsonl"
    if pre.exists():
        for l in pre.read_text(encoding="utf-8").splitlines():
            if l.strip():
                validos.add(json.loads(l)["url"])

    itens, descartados = [], 0
    for l in (DADOS / "enriquecidos.jsonl").read_text(encoding="utf-8").splitlines():
        if l.strip():
            try:
                d = json.loads(l)
            except json.JSONDecodeError:
                continue
            if validos and d["url"] not in validos:
                descartados += 1
                continue
            itens.append(d)
    if descartados:
        print(f"{descartados} itens enriquecidos foram descartados por não passarem "
              f"mais na peneira atual")
    itens = [julgar(c) for c in itens]
    itens.sort(key=lambda c: (c["nota"], chave_desempate(c, args.desempate)), reverse=True)

    (DADOS / "ranqueado.jsonl").write_text(
        "\n".join(json.dumps(c, ensure_ascii=False) for c in itens) + "\n", encoding="utf-8")

    topo = itens[: args.quantos]
    with (DADOS / "para_descrever.jsonl").open("w", encoding="utf-8") as f:
        for c in topo:
            f.write(json.dumps({
                "nome": c["nome"],
                "url": c.get("url_ferramenta") or c["verificacao"].get("url_final") or c["url"],
                "url_coletada": c["url"],
                "fonte": c["fonte"],
                "faceta": (c.get("sinais") or {}).get("faceta"),
                "nota": c["nota"],
                "evidencia": c["evidencia"],
                "sinais": c.get("sinais"),
                "titulo_pagina": (c.get("pagina") or {}).get("titulo", ""),
                "meta_pagina": (c.get("pagina") or {}).get("meta", ""),
                "corpo_pagina": (c.get("pagina") or {}).get("corpo", "")[:1400],
            }, ensure_ascii=False) + "\n")

    # ---------------------------------------------------------- relatório
    vivos = sum(1 for c in itens if c["evidencia"]["link_vivo"])
    mortas = sum(1 for c in itens if c["evidencia"]["pagina_morta"])
    por_fonte = collections.Counter(c["fonte"] for c in topo)
    susp_ag = sum(1 for c in topo if c["evidencia"]["suspeita_agente_unico"])
    susp_pw = sum(1 for c in topo if c["evidencia"]["suspeita_paywall"])

    # Taxa on-tema dos diretórios: a amostra que justifica descartar 7.776 anúncios.
    dir_itens = [c for c in itens if c["fonte"].startswith("diretorios")]
    dir_tema = sum(1 for c in dir_itens if c["evidencia"]["P1"])

    L = [
        "# Relatório do julgamento sobre o texto real das páginas",
        "",
        f"Gerado em {datetime.now().astimezone().isoformat(timespec='seconds')}",
        f"Desempate: **{args.desempate}** · Fila para descrição: **{len(topo)}**",
        "",
        f"- itens enriquecidos e julgados: **{len(itens)}**",
        f"- com link vivo (200 + conteúdo): **{vivos}** ({100*vivos/max(len(itens),1):.1f}%)",
        f"- páginas que carregaram mas são 404/parked/sleeping: **{mortas}**",
        "",
        "## Amostra dos diretórios comerciais",
        "",
        f"Abertos e lidos: **{len(dir_itens)}** anúncios de futuretools + aixploria.",
        f"Com sinal de multiagente no texto real da página: **{dir_tema}** "
        f"({100*dir_tema/max(len(dir_itens),1):.1f}%).",
        "",
        "Essa taxa é o que justifica não ter enriquecido os 7.776 anúncios varridos:",
        "a amostra mede a densidade do tema no catálogo comercial de IA.",
        "",
        "## Composição da fila das 500",
        "", "| fonte | itens |", "|---|---|",
        *[f"| {f} | {n} |" for f, n in por_fonte.most_common()],
        "",
        "## Suspeitas marcadas na fila (E2 e E3)",
        "",
        f"- suspeita de agente único / wrapper de LLM: **{susp_ag}**",
        f"- suspeita de paywall antes de ver: **{susp_pw}**",
        "",
        "Regex não decide isso — decide quem lê. Estes números dizem quantos itens",
        "da fila precisam de conferência humana antes de entrar nas 50.",
        "",
        "## Faixa de nota na fila",
        "",
        f"- maior: {topo[0]['nota'] if topo else '-'}",
        f"- menor: {topo[-1]['nota'] if topo else '-'}",
        f"- itens com nota negativa na fila: "
        f"**{sum(1 for c in topo if c['nota'] < 0)}** "
        "(se este número for alto, a fila está sendo preenchida com sobra, não com mérito)",
    ]
    (DADOS / "relatorio_julgamento.md").write_text("\n".join(L) + "\n", encoding="utf-8")

    print(f"julgados {len(itens)} | vivos {vivos} | fila {len(topo)}")
    print(f"diretórios: {dir_tema}/{len(dir_itens)} com sinal de multiagente no texto real")
    print(f"suspeitas na fila — agente único: {susp_ag} | paywall: {susp_pw}")
    print(f"relatório: {DADOS / 'relatorio_julgamento.md'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
