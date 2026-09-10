"""Fase B — peneira mecânica + pré-pontuação, com os critérios do aluno.

CRITÉRIOS DECLARADOS (escolhidos por Victor, não por mim):

  Eliminatórios
    E1  não se abre e usa (repositório/biblioteca/PDF puro, sem app)
    E2  agente único, sem interação entre agentes
    E3  paywall antes de ver qualquer coisa

  Positivos (somam)
    P1  múltiplos agentes se afetando
    P2  dá para ver por dentro (log, replay, timeline, visualização)
    P3  ambiente configurável por quem usa
    P4  produz resultado analisável (dado, métrica, exportação)

  Desempate: definido em --desempate (padrão: popularidade, escolha do aluno)

O QUE ESTE SCRIPT HONESTAMENTE NÃO FAZ
--------------------------------------
Só E1 é decidível por máquina, e mesmo assim por aproximação (a ausência de
`homepage` num repositório é um bom indício de "não tem app", não uma prova).
E2 e E3 exigem abrir a ferramenta: não dá para saber por regex se há agentes
interagindo ou se o paywall vem antes da demo. Aqui eles viram SUSPEITA
marcada, não eliminação — a eliminação de verdade acontece no julgamento em
lote sobre o texto real da página, depois do enriquecimento.

As regras P1..P4 também são só PROXY TEXTUAL. "multi-agent" no título não prova
que há agentes se afetando; prova que a palavra está lá. Por isso a pontuação
aqui serve para ORDENAR a fila de enriquecimento, não para decidir a lista.

Uso:
    uv run python atividade-1/peneirar.py
    uv run python atividade-1/peneirar.py --desempate raridade
    uv run python atividade-1/peneirar.py --pool 1500
"""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from datetime import datetime, timedelta, timezone
from pathlib import Path

RAIZ = Path(__file__).parent
DADOS = RAIZ / "dados"

# --- E1: o que, por construção, não é "algo que se abre e usa" ---------------
# Não é a ferramenta, é o texto sobre a ferramenta.
DOMINIOS_NAO_FERRAMENTA = {
    "arxiv.org", "semanticscholar.org", "openreview.net", "acm.org", "ieee.org",
    "springer.com", "sciencedirect.com", "nature.com", "biorxiv.org", "ssrn.com",
    "wikipedia.org", "medium.com", "substack.com", "dev.to", "hashnode.dev",
    "blogspot.com", "wordpress.com", "notion.so", "docs.google.com",
    "youtube.com", "youtu.be", "vimeo.com", "twitter.com", "x.com", "t.co",
    "linkedin.com", "facebook.com", "instagram.com", "tiktok.com",
    "pypi.org", "npmjs.com", "crates.io", "rubygems.org", "packagist.org",
    "readthedocs.io", "gitbook.io", "stackoverflow.com", "news.ycombinator.com",
    "amazon.com", "google.com", "apple.com", "microsoft.com",
}

# --- P1..P4: proxies textuais ------------------------------------------------
P1_MULTIAGENTE = re.compile(
    r"multi[- ]?agent|multiagent|agent society|societ(y|ies) of agents|"
    r"generative agents|agent population|swarm|crowd simul|colony|"
    r"npcs?\b|villagers?|inhabitants|agents interact|between agents|"
    r"agent[- ]based model|\babm\b|social simulation", re.I)
P2_VER_POR_DENTRO = re.compile(
    r"trace|replay|timeline|observab|telemetry|inspect|visuali[sz]|"
    r"dashboard|monitor|debug|step[- ]through|transcript|conversation log|"
    r"watch (them|the agents)", re.I)
P3_CONFIGURAVEL = re.compile(
    r"configur|customi[sz]|scenario|sandbox|playground|no[- ]code|"
    r"parameters?|rule[- ]?set|environment builder|editor|"
    r"design your own|build your own|persona|prompt the agents", re.I)
P4_ANALISAVEL = re.compile(
    r"metrics?|analytics?|export|csv|json output|benchmark|evaluat|"
    r"leaderboard|statistics|report|measure|results? data|experiment", re.I)

# --- E2/E3: suspeitas (marcam, não eliminam) --------------------------------
S_AGENTE_UNICO = re.compile(
    r"\bchatbot\b|ai assistant|copilot|writing assistant|your ai (friend|companion)|"
    r"chat with (an )?ai|single agent|prompt library|gpt wrapper", re.I)
S_PAYWALL = re.compile(
    r"request a demo|book a demo|contact sales|talk to sales|enterprise only|"
    r"start your free trial|pricing starts at", re.I)

PESOS = {"P1": 3.0, "P2": 2.0, "P3": 2.0, "P4": 1.5}


def texto_de(c: dict) -> str:
    partes = [c.get("nome", ""), c.get("descricao_fonte", ""), c.get("url", "")]
    sinais = c.get("sinais") or {}
    if isinstance(sinais.get("topicos"), list):
        partes.append(" ".join(sinais["topicos"]))
    for k in ("tag", "faceta", "sdk"):
        if sinais.get(k):
            partes.append(str(sinais[k]))
    return " ".join(p for p in partes if p)


def eliminar(c: dict) -> str | None:
    """Devolve o motivo da eliminação, ou None se sobrevive."""
    sinais = c.get("sinais") or {}
    dominio = c.get("dominio", "")
    if dominio in DOMINIOS_NAO_FERRAMENTA:
        return "E1: domínio é publicação/rede social/registro de pacote, não ferramenta"
    if sinais.get("tipo") == "paper":
        return "E1: é paper, não app"
    if sinais.get("so_repo") is True:
        return "E1: repositório sem homepage — nada para abrir e usar (é Entrega 2)"
    # O critério E1 vale pela URL, não pela fonte. A primeira versão só olhava
    # itens vindos da fonte `github`, e com isso 82 posts do Hacker News que
    # apontavam para github.com entraram na fila — repositório, exatamente o
    # que E1 reprova. Hospedagem de código é hospedagem de código, não importa
    # quem indicou. (`github.io` NÃO entra aqui: é página publicada, não repo.)
    if c.get("dominio") in ("github.com", "gitlab.com", "bitbucket.org",
                            "codeberg.org", "sourceforge.net", "gitee.com"):
        return "E1: link aponta para hospedagem de código, não para um app"
    if not c.get("url"):
        return "E1: sem URL"
    return None


def pontuar(c: dict) -> tuple[float, dict]:
    t = texto_de(c)
    detalhe = {
        "P1": bool(P1_MULTIAGENTE.search(t)),
        "P2": bool(P2_VER_POR_DENTRO.search(t)),
        "P3": bool(P3_CONFIGURAVEL.search(t)),
        "P4": bool(P4_ANALISAVEL.search(t)),
    }
    nota = sum(PESOS[k] for k, v in detalhe.items() if v)
    detalhe["suspeita_agente_unico"] = bool(S_AGENTE_UNICO.search(t))
    detalhe["suspeita_paywall"] = bool(S_PAYWALL.search(t))
    detalhe["sem_texto"] = len((c.get("descricao_fonte") or "").strip()) < 20
    return nota, detalhe


def chave_desempate(c: dict, modo: str):
    sinais = c.get("sinais") or {}
    if modo == "popularidade":
        return float(sinais.get("estrelas") or sinais.get("likes")
                     or sinais.get("pontos") or sinais.get("upvotes") or 0)
    if modo == "raridade":
        # menos fontes = mais raro; invertido para ordenar decrescente junto
        return -len(c.get("fontes_extras") or [])
    if modo == "vida":
        bruto = sinais.get("atualizado") or sinais.get("ultimo_push") or sinais.get("data") or ""
        try:
            return datetime.fromisoformat(str(bruto).replace("Z", "+00:00")).timestamp()
        except Exception:
            return 0.0
    if modo == "faceta":
        return 0.0  # tratado depois, precisa de estado global
    return 0.0


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--desempate", default="popularidade",
                   choices=["popularidade", "raridade", "vida", "faceta"])
    p.add_argument("--pool", type=int, default=1500,
                   help="quantos sobreviventes vão para o enriquecimento")
    args = p.parse_args()

    # Tolera linha final truncada: o arquivo pode estar sendo escrito por uma
    # varredura ainda em curso (append em JSONL), e uma linha pela metade não
    # deve derrubar a peneira inteira.
    candidatos = []
    for l in (DADOS / "candidatos.jsonl").read_text(encoding="utf-8").splitlines():
        if not l.strip():
            continue
        try:
            candidatos.append(json.loads(l))
        except json.JSONDecodeError:
            print("aviso: linha JSONL truncada ignorada (varredura em curso?)")

    mortos: list[tuple[dict, str]] = []
    vivos: list[dict] = []
    for c in candidatos:
        motivo = eliminar(c)
        if motivo:
            mortos.append((c, motivo))
        else:
            nota, det = pontuar(c)
            c["nota_proxy"] = nota
            c["proxy"] = det
            vivos.append(c)

    vivos.sort(key=lambda c: (c["nota_proxy"], chave_desempate(c, args.desempate)), reverse=True)

    # ---------------------------------------------------- seleção do pool
    #
    # Ranquear o conjunto inteiro por nota de proxy NÃO funciona, e isso foi
    # medido: na primeira tentativa o topo do pool virou repositório obscuro do
    # GitHub, porque todo README de agente escreve "multi-agent", "trace" e
    # "metrics" por hábito, e o regex não distingue hábito de substância.
    # A nota textual mede vocabulário, não qualidade.
    #
    # Então o pool é montado por COTA POR FONTE. Cada fonte entra com um teto,
    # ordenada pela sua própria nota. Isso impede que a convenção de escrita de
    # uma fonte sequestre a fila inteira, e mantém no pool as fontes que de
    # fato entregam coisa que se abre (Spaces, itch.io).
    #
    # A cota de `diretorios` é deliberadamente pequena e serve de AMOSTRA: dos
    # 7.776 anúncios varridos, só 2 casam com o tema pelo slug (0,03%). Se ao
    # abrir 300 ao acaso a taxa se confirmar, está medido que catálogo comercial
    # de IA não cobre simulação de agentes — e isso é um achado, não um buraco.
    COTAS = {
        "huggingface:space": 600,   # app que roda; a fonte mais Entrega-1 do conjunto
        "itchio": 400,              # mundo simulado, que nenhuma outra fonte tem
        "hn": 350,                  # link externo curado por gente
        "github": 300,              # só os que têm homepage; o resto morreu em E1
        "arxiv:projeto": 250,       # URL de projeto extraída do resumo do paper
        "arxiv": 0,                 # paper puro já morreu em E1
        "diretorios:futuretools": 150,
        "diretorios:aixploria": 150,
        "producthunt": 50,
        "huggingface:paper": 0,
    }
    por_fonte: dict[str, list[dict]] = {}
    for c in vivos:  # `vivos` já está ordenado por nota + desempate
        por_fonte.setdefault(c["fonte"], []).append(c)

    pool: list[dict] = []
    usado: dict[str, int] = {}
    for fonte, itens_fonte in por_fonte.items():
        cota = COTAS.get(fonte, 100)  # fonte nova entra com teto conservador
        escolhidos = itens_fonte[:cota]
        pool += escolhidos
        usado[fonte] = len(escolhidos)

    saida = DADOS / "preselecao.jsonl"
    with saida.open("w", encoding="utf-8") as f:
        for c in pool:
            f.write(json.dumps(c, ensure_ascii=False) + "\n")

    # ------------------------------------------------------- relatório da peneira
    por_motivo = Counter(m for _, m in mortos)
    por_fonte_viva = Counter(c["fonte"] for c in vivos)
    por_fonte_morta = Counter(c["fonte"] for c, _ in mortos)
    linhas = [
        "# Relatório da peneira mecânica",
        "",
        f"Gerado em {datetime.now(timezone.utc).astimezone().isoformat(timespec='seconds')}",
        f"Desempate aplicado: **{args.desempate}**",
        "",
        f"- candidatos brutos: **{len(candidatos)}**",
        f"- eliminados por regra mecânica: **{len(mortos)}**",
        f"- sobreviventes: **{len(vivos)}**",
        f"- enviados ao enriquecimento (pool): **{len(pool)}**",
        "",
        "## Cota por fonte no pool de enriquecimento",
        "",
        "O pool NÃO é o top-N por nota. Ranquear tudo junto pela nota de proxy foi",
        "tentado e falhou: o topo virou repositório obscuro do GitHub, porque todo",
        "README de agente escreve 'multi-agent', 'trace' e 'metrics' por hábito.",
        "A nota textual mede vocabulário, não substância. Daí a cota por fonte.",
        "",
        "| fonte | sobreviventes | entraram no pool |", "|---|---|---|",
        *[f"| {f} | {len(por_fonte.get(f, []))} | {usado.get(f, 0)} |"
          for f in sorted(por_fonte)],
        "",
        "## O que cada regra matou",
        "",
        "| motivo | quantos |", "|---|---|",
    ]
    linhas += [f"| {m} | {n} |" for m, n in por_motivo.most_common()]
    linhas += ["", "## Sobrevivência por fonte", "", "| fonte | sobreviveu | morreu |", "|---|---|---|"]
    for fonte in sorted(set(por_fonte_viva) | set(por_fonte_morta)):
        linhas.append(f"| {fonte} | {por_fonte_viva.get(fonte, 0)} | {por_fonte_morta.get(fonte, 0)} |")

    linhas += ["", "## Amostra do que o SEU critério derrubou",
               "", "Dez eliminados de maior popularidade — para você conferir se aceita a perda.", ""]
    mortos_pop = sorted(
        mortos, key=lambda x: float((x[0].get("sinais") or {}).get("estrelas") or 0), reverse=True)
    for c, m in mortos_pop[:10]:
        est = (c.get("sinais") or {}).get("estrelas")
        linhas.append(f"- **{c['nome']}** ({est} estrelas) — {c['url']}  \n  motivo: {m}")

    (DADOS / "relatorio_peneira.md").write_text("\n".join(linhas) + "\n", encoding="utf-8")

    print(f"brutos {len(candidatos)} | eliminados {len(mortos)} | vivos {len(vivos)} | pool {len(pool)}")
    print(f"relatório: {DADOS / 'relatorio_peneira.md'}")
    for m, n in por_motivo.most_common():
        print(f"  {n:>6}  {m}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
