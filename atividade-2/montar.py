"""Fase E da Entrega 2 — monta os artefatos.

Produz em `entrega/`: 500-ferramentas.{jsonl,csv,md} com nome, url, descricao,
categoria e imagem.

SOBRE A DESCRIÇÃO
-----------------
Três frases, nesta ordem: (a) o que entra e o que sai, (b) onde encaixa no
trabalho de quem usa, (c) qual é o limite. Proibido adjetivo de propaganda.

Na Entrega 2 a alínea (a) tem uma vantagem que a Entrega 1 não tinha: existe
COMANDO DE INSTALAÇÃO concreto. "pip install mesa" diz mais sobre o que entra
do que qualquer frase.

O campo `descricao_origem` marca `redigida` (escrita à mão a partir do README,
em `descricoes/*.jsonl`) ou `composta` (montada de fatos verificados, seca, sem
leitura humana). O contador aparece ao fim da execução: se a maioria estiver
composta, o documento ainda não está pronto por mais que exista.

A imagem sai do avatar da organização no GitHub ou do favicon do registro —
nenhum serviço de terceiros gera ícone aqui.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
from datetime import datetime
from pathlib import Path
from urllib.parse import urlsplit

RAIZ = Path(__file__).parent
DADOS = RAIZ / "dados"
SAIDA = RAIZ / "entrega"
DESCRICOES = RAIZ / "descricoes"

ROTULO_FACETA = {
    "abm_framework": "Framework de modelagem baseada em agentes",
    "multiagente_llm": "Orquestração multiagente com LLM",
    "ambiente_rl": "Ambiente de aprendizado por reforço",
    "memoria_estado": "Memória e estado de agente",
    "observabilidade_sdk": "Observabilidade e trace como SDK",
    "avaliacao_bench": "Avaliação e benchmark de agentes",
    "npc_jogos": "IA de jogo e NPC",
    "simulacao_social": "Simulação social e de redes",
    "economia_mercado": "Simulação de mercado e negociação",
    "sandbox_execucao": "Sandbox e execução de código",
    "curadoria": "Vindo de lista curada",
    "modelo": "Modelo pronto para chamar",
    "pacote_python": "Pacote Python",
}

FAVICONS = {
    "npmjs.com": "https://static-production.npmjs.com/favicon.ico",
    "crates.io": "https://crates.io/favicon.ico",
    "pypi.org": "https://pypi.org/static/images/favicon.35549fe8.ico",
    "nuget.org": "https://www.nuget.org/favicon.ico",
    "rubygems.org": "https://rubygems.org/favicon.ico",
    "packagist.org": "https://packagist.org/favicon.ico",
    "huggingface.co": "https://huggingface.co/favicon.ico",
}


# --- classificação por texto ------------------------------------------------
# A faceta só vem preenchida em parte das fontes: registro de pacote não tem
# campo de categoria, e a busca por tópico do GitHub grava o tópico cru. Sem
# isto, 398 das 500 saíam como "Não classificado" — e categoria é um dos cinco
# campos que o sistema de entrega pede.
#
# A classificação é por PRIORIDADE, não por maior contagem: uma biblioteca de
# simulação social que também emite trace é, antes de tudo, simulação social.
# A ordem abaixo é a do recorte do aluno, do núcleo do tema para a periferia.
CLASSIFICADORES = [
    ("abm_framework", re.compile(
        r"agent[- ]based (model|modeling|modelling|simulation)|\babm\b|mesa|netlogo|"
        r"cellular automata|discrete[- ]event simulation|simpy", re.I)),
    ("simulacao_social", re.compile(
        r"social simulation|opinion dynamic|social network simulation|epidemic|"
        r"contagion|society of agents|artificial society|crowd simulation", re.I)),
    ("ambiente_rl", re.compile(
        r"pettingzoo|gym(nasium)?\b|reinforcement learning environment|\bmarl\b|"
        r"self[- ]play|multi[- ]agent reinforcement|policy training|rollout", re.I)),
    ("npc_jogos", re.compile(
        r"\bnpcs?\b|behavio(u)?r tree|\bgoap\b|game ai|utility ai|pathfinding|"
        r"dialogue (engine|system)|godot|unity|unreal", re.I)),
    ("economia_mercado", re.compile(
        r"market simulation|order book|auction|trading (simulator|agents)|"
        r"backtest|game theory|nash|supply chain", re.I)),
    ("memoria_estado", re.compile(
        r"agent memory|episodic memory|long[- ]term memory|vector (store|memory)|"
        r"state persistence|checkpoint|knowledge graph memory", re.I)),
    ("observabilidade_sdk", re.compile(
        r"tracing|trace|span|opentelemetry|observability|telemetry|replay|"
        r"instrument|monitor(ing)? (llm|agent)", re.I)),
    ("avaliacao_bench", re.compile(
        r"benchmark|eval(uation)? (framework|harness|suite)|leaderboard|"
        r"scoring|test harness|assert.*agent", re.I)),
    ("sandbox_execucao", re.compile(
        r"sandbox|isolat(ed|ion)|container|firecracker|wasm|code execution|"
        r"interpreter", re.I)),
    ("multiagente_llm", re.compile(
        r"multi[- ]?agent|multiagent|agent orchestration|agentic workflow|"
        r"crew|swarm|autonomous agents?|llm agents?|agent framework|"
        r"agent runtime|tool calling", re.I)),
]


def classificar(c: dict) -> str:
    faceta = c.get("faceta") or ""
    if faceta in ROTULO_FACETA and faceta not in ("curadoria", "pacote_python"):
        return faceta
    alvo = " ".join([c.get("nome", ""), c.get("descricao", ""),
                     (c.get("readme") or "")[:1500]])
    for nome, rx in CLASSIFICADORES:
        if rx.search(alvo):
            return nome
    return faceta or ""


def imagem_de(url: str) -> str:
    m = re.search(r"github\.com/([\w.\-]+)", url or "")
    if m:
        return f"https://github.com/{m.group(1)}.png?size=120"
    host = urlsplit(url).netloc.replace("www.", "")
    for chave, ico in FAVICONS.items():
        if host.endswith(chave):
            return ico
    return f"https://{host}/favicon.ico" if host else ""


def carregar_redigidas() -> dict[str, str]:
    fora: dict[str, str] = {}
    if not DESCRICOES.exists():
        return fora
    for arq in sorted(DESCRICOES.glob("*.jsonl")):
        for linha in arq.read_text(encoding="utf-8").splitlines():
            if not linha.strip():
                continue
            try:
                d = json.loads(linha)
            except json.JSONDecodeError:
                continue
            if d.get("url_coletada") and d.get("descricao"):
                fora[d["url_coletada"]] = d["descricao"].strip()
    return fora


def compor(c: dict) -> str:
    """Descrição mecânica a partir de fato verificado. Não inventa."""
    d = c.get("detalhe") or {}
    ev = c.get("evidencia") or {}
    s = c.get("sinais") or {}
    desc = (c.get("descricao") or "").strip()

    inst = s.get("instalacao") or ev.get("prova_instalacao") or ""
    a = (desc.rstrip(".") + ".") if desc else "Não consegui apurar o que entra e o que sai."
    if inst:
        a += f" Instala-se com `{inst}`."

    tem = []
    if ev.get("P1"):
        tem.append("o texto menciona vários agentes interagindo")
    if ev.get("P2"):
        tem.append("menciona hook, trace, replay ou serialização de estado")
    if ev.get("P3"):
        tem.append("menciona ambiente, regra ou cenário definidos por código")
    if ev.get("P4"):
        tem.append("menciona semente, métrica ou exportação de resultado")
    b = ("Encaixa no fluxo de quem programa simulação com agentes: " + "; ".join(tem) + ".") \
        if tem else "Onde encaixa: não consegui apurar pelo texto do projeto."

    lim = []
    lic = ev.get("licenca") or ""
    lim.append(f"licença {lic}" if lic else "licença não declarada")
    if d.get("versao"):
        lim.append(f"versão {d['versao']} na coleta")
    if d.get("downloads"):
        lim.append(f"{d['downloads']} downloads registrados")
    if ev.get("suspeita_involucro"):
        lim.append("há sinal de ser casca fina sobre uma API de modelo, o que precisa de conferência")
    if not ev.get("tem_readme"):
        lim.append("sem README utilizável, então o que a biblioteca faz não pôde ser confirmado")
    return f"{a} {b} Limite: {'; '.join(lim)}."


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--quantos", type=int, default=500)
    args = p.parse_args()

    SAIDA.mkdir(parents=True, exist_ok=True)
    itens = [json.loads(l) for l in
             (DADOS / "para_descrever.jsonl").read_text(encoding="utf-8").splitlines()
             if l.strip()][: args.quantos]
    redigidas = carregar_redigidas()

    linhas, n_red = [], 0
    for c in itens:
        desc = redigidas.get(c["url_coletada"])
        origem = "redigida" if desc else "composta"
        n_red += 1 if desc else 0
        linhas.append({
            "nome": (c.get("nome") or "").strip(),
            "url": c["url"],
            "descricao": " ".join((desc or compor(c)).split()),
            "categoria": ROTULO_FACETA.get(classificar(c), "Não classificado"),
            "imagem": imagem_de(c["url"]),
            "descricao_origem": origem,
            "fonte_da_varredura": c.get("fonte"),
            "licenca": (c.get("evidencia") or {}).get("licenca"),
            "instalacao": (c.get("sinais") or {}).get("instalacao")
                          or (c.get("evidencia") or {}).get("prova_instalacao"),
            "nota": c.get("nota"),
        })

    with (SAIDA / "500-ferramentas.jsonl").open("w", encoding="utf-8") as f:
        for l in linhas:
            f.write(json.dumps(l, ensure_ascii=False) + "\n")
    with (SAIDA / "500-ferramentas.csv").open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(linhas[0].keys()) if linhas else
                           ["nome", "url", "descricao", "categoria", "imagem"])
        w.writeheader(); w.writerows(linhas)

    md = ["# As 500 — Entrega 2 (Ferramentas de Desenvolvimento)", "",
          f"Gerado em {datetime.now().astimezone().isoformat(timespec='seconds')} · "
          f"{len(linhas)} itens · {n_red} com descrição redigida, "
          f"{len(linhas) - n_red} compostas automaticamente.", ""]
    por_cat: dict[str, list[dict]] = {}
    for l in linhas:
        por_cat.setdefault(l["categoria"], []).append(l)
    for cat in sorted(por_cat):
        md += [f"## {cat} ({len(por_cat[cat])})", ""]
        for l in por_cat[cat]:
            md.append(f"- **[{l['nome']}]({l['url']})** — {l['descricao']}")
        md.append("")
    (SAIDA / "500-ferramentas.md").write_text("\n".join(md) + "\n", encoding="utf-8")

    print(f"{len(linhas)} itens em entrega/500-ferramentas.{{jsonl,csv,md}}")
    print(f"  redigida à mão: {n_red}")
    print(f"  composta automaticamente: {len(linhas) - n_red}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
