"""Peneira mecânica da Entrega 2, com os critérios declarados por Victor.

CRITÉRIOS (escolhidos por ele, não por mim)

  Eliminatórios
    E1  não dá para instalar ou importar
    E3  sem licença aberta clara
    E4  invólucro fino sem substância própria

  RECUSADO de propósito: "projeto morto ou arquivado". Ele já havia recusado o
  equivalente na Entrega 1 para preservar os marcos de 2023 do próprio tema, e
  manteve a recusa aqui mesmo depois de eu argumentar que para BIBLIOTECA o
  cálculo inverte — app parado ainda abre, biblioteca parada quebra na primeira
  dependência incompatível. A decisão é dele; a consequência está no relatório.

  Positivos (somam)
    P1  modela múltiplos agentes se afetando        (peso 3,0)
    P2  expõe o estado por dentro                    (peso 2,0)
    P3  ambiente e regras definidos por código       (peso 2,0)
    P4  reprodutível e mensurável                    (peso 1,5)

  Desempate: downloads (escolha dele — em registro de pacote existe contagem de
  download, que mede uso, enquanto estrela mede aprovação).

O QUE ESTE SCRIPT HONESTAMENTE NÃO DECIDE
-----------------------------------------
E1 só é mecânico nos dois extremos: item vindo de registro de pacote passa por
construção (estar publicado É o empacotamento), e domínio que não hospeda
código reprova direto. No meio — repositório do GitHub — não dá para saber pela
API se existe pacote publicado; isso é decidido no enriquecimento, procurando
comando de instalação no README.

E3 é mecânico onde o dado existe (a busca do GitHub devolve a licença SPDX) e
fica para o enriquecimento onde não existe (npm e crates.io não trazem licença
na busca).

E4 não é decidível por máquina nenhuma: vira suspeita marcada e conferência na
leitura, igual ao E2/E3 da Entrega 1.

As regras P1..P4 são PROXY TEXTUAL — medem vocabulário, não substância. Servem
para ordenar a fila de enriquecimento, não para decidir a lista.

Uso:
    uv run python atividade-2/peneirar.py
    uv run python atividade-2/peneirar.py --desempate estrelas --pool 2000
"""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

RAIZ = Path(__file__).parent
DADOS = RAIZ / "dados"

# --- E1: domínio que, por construção, não entrega código instalável ---------
DOMINIOS_NAO_CODIGO = {
    "arxiv.org", "semanticscholar.org", "openreview.net", "acm.org", "ieee.org",
    "springer.com", "sciencedirect.com", "nature.com", "biorxiv.org", "ssrn.com",
    "wikipedia.org", "medium.com", "substack.com", "dev.to", "hashnode.dev",
    "blogspot.com", "wordpress.com", "notion.so", "docs.google.com",
    "youtube.com", "youtu.be", "vimeo.com", "twitter.com", "x.com", "t.co",
    "linkedin.com", "facebook.com", "instagram.com", "tiktok.com",
    "stackoverflow.com", "news.ycombinator.com", "reddit.com",
    "producthunt.com", "itch.io", "steampowered.com", "apps.apple.com",
    "play.google.com", "aixploria.com", "futuretools.io", "theresanaiforthat.com",
}

# Hospedagem de código e registros: aqui o item É instalável ou quase.
HOSPEDAGEM_CODIGO = ("github.com", "gitlab.com", "codeberg.org", "bitbucket.org",
                     "sourceforge.net", "gitee.com", "huggingface.co")
REGISTROS = ("pypi.org/project/", "npmjs.com/package/", "crates.io/crates/",
             "nuget.org/packages/", "rubygems.org/gems/", "packagist.org/packages/",
             "pkg.go.dev/", "hex.pm/packages/", "pub.dev/packages/",
             "mvnrepository.com/artifact/", "cocoapods.org/pods/")

# --- P1..P4: proxies textuais ----------------------------------------------
P1_MULTIAGENTE = re.compile(
    r"multi[- ]?agent|multiagent|agent[- ]based|\babm\b|agent society|"
    r"population of agents|swarm|crowd simul|colony|flocking|boids|"
    r"social simulation|opinion dynamic|emergent|interaction between agents|"
    r"pettingzoo|marl\b|self[- ]play|npcs?\b", re.I)
P2_ESTADO_POR_DENTRO = re.compile(
    r"\bhooks?\b|callback|introspect|trace|tracing|span|replay|snapshot|"
    r"serializ|checkpoint|observab|telemetry|inspect|event stream|"
    r"state machine|history|audit|logging|instrument", re.I)
P3_AMBIENTE_POR_CODIGO = re.compile(
    r"custom environment|define your own|configurable|extensible|"
    r"\bplugin|scenario|rule[- ]?set|declarative|\bdsl\b|schema|"
    r"subclass|interface|abstract base|environment api|world model|"
    r"grid|space|topolog|scheduler", re.I)
P4_REPRODUTIVEL = re.compile(
    r"\bseed\b|deterministic|reproducib|metric|benchmark|evaluat|"
    r"batch run|parameter sweep|export|dataframe|csv|analysis|"
    r"statistic|monte carlo|experiment", re.I)

# --- PORTÃO DE RELEVÂNCIA --------------------------------------------------
# Achado ao conferir os 12 primeiros do pool, e é o mesmo tipo de erro da
# Entrega 1 — a nota de proxy mede vocabulário, não substância. Aqui foi pior:
# o topo veio tomado por `sensu-plugins-docker-swarm` e `puma-plugin-telemetry`,
# que são monitoramento de infraestrutura. O motivo é que DevOps compartilha
# quase todo o vocabulário deste recorte: "swarm" é Docker Swarm, "agent" é
# agente de monitoramento, "orchestration" é Kubernetes, "telemetry" é APM.
#
# A correção não inventa critério novo: ela faz valer o critério P1 que o aluno
# declarou ("modela múltiplos agentes SE AFETANDO"). Casar a palavra "swarm"
# não é evidência disso; casar "multi-agent", "agent-based" ou "generative
# agents" é. Então o item precisa de pelo menos um sinal FORTE do tema para
# entrar no pool, e um sinal de outro domínio sem sinal forte reprova.
TEMA_FORTE = re.compile(
    r"multi[- ]?agent|multiagent|agent[- ]based|\babm\b|agent simulation|"
    r"simulation (framework|library|engine|toolkit)|generative agents|"
    r"agent society|societ(y|ies) of agents|social simulation|opinion dynamic|"
    r"\bmarl\b|pettingzoo|gym(nasium)? environment|reinforcement learning environment|"
    r"self[- ]play|\bnpcs?\b|behavio(u)?r tree|\bgoap\b|swarm intelligence|"
    r"boids|flocking|cellular automata|crowd simulation|colony simulation|"
    r"discrete[- ]event simulation|epidemic (model|simulation)|"
    r"llm agents?|autonomous agents?|agentic (framework|workflow|system)|"
    r"agent (framework|runtime|orchestration|memory|harness)", re.I)

# Domínios que compartilham o vocabulário sem compartilhar o assunto.
FALSO_AMIGO = re.compile(
    r"docker swarm|kubernetes|\bk8s\b|sensu|fluentd|fluent-plugin|nagios|zabbix|"
    r"prometheus exporter|datadog|new relic|puma|sidekiq|logstash|filebeat|"
    r"apm agent|monitoring agent|\buser[- ]agent\b|http agent|ssh agent|"
    r"mail (transfer )?agent|browser agent|deploy(ment)? agent|"
    r"chef|puppet|ansible|terraform|salt(stack)?|systemd|cron", re.I)

# --- E4: suspeita de invólucro fino ----------------------------------------
S_INVOLUCRO = re.compile(
    r"simple wrapper|thin wrapper|lightweight wrapper|wrapper (around|for) "
    r"(the )?(openai|anthropic|gemini|llm)|just a wrapper|unofficial (api )?client|"
    r"api client for|sdk for the .* api", re.I)

PESOS = {"P1": 3.0, "P2": 2.0, "P3": 2.0, "P4": 1.5}


def texto_de(c: dict) -> str:
    partes = [c.get("nome", ""), c.get("descricao_fonte", ""), c.get("url", "")]
    s = c.get("sinais") or {}
    for k in ("topicos", "palavras_chave", "licencas"):
        v = s.get(k)
        if isinstance(v, list):
            partes.append(" ".join(str(x) for x in v))
        elif isinstance(v, str):
            partes.append(v)
    for k in ("faceta", "linguagem", "biblioteca", "tarefa", "registro"):
        if s.get(k):
            partes.append(str(s[k]))
    return " ".join(p for p in partes if p)


def eliminar(c: dict) -> str | None:
    """Motivo da eliminação, ou None se sobrevive à peneira mecânica."""
    url = c.get("url") or ""
    dominio = c.get("dominio", "")
    s = c.get("sinais") or {}

    if not url:
        return "E1: sem URL"
    if dominio in DOMINIOS_NAO_CODIGO:
        return "E1: domínio não hospeda código instalável"
    eh_registro = any(r in url for r in REGISTROS)
    eh_codigo = any(h in url for h in HOSPEDAGEM_CODIGO)
    if not (eh_registro or eh_codigo):
        return "E1: não é registro de pacote nem hospedagem de código"

    # E3 só onde o dado já existe. A busca do GitHub devolve a licença SPDX;
    # ausência declarada é ausência de licença, não falta de informação.
    if c.get("fonte") == "github" and "licenca" in s and not s.get("licenca"):
        return "E3: repositório sem licença declarada"
    if s.get("licenca") in ("NOASSERTION",):
        return "E3: licença não identificável (NOASSERTION)"
    return None


def pontuar(c: dict) -> tuple[float, dict]:
    t = texto_de(c)
    det = {
        "P1": bool(P1_MULTIAGENTE.search(t)),
        "P2": bool(P2_ESTADO_POR_DENTRO.search(t)),
        "P3": bool(P3_AMBIENTE_POR_CODIGO.search(t)),
        "P4": bool(P4_REPRODUTIVEL.search(t)),
    }
    nota = sum(PESOS[k] for k, v in det.items() if v)
    det["tema_forte"] = bool(TEMA_FORTE.search(t))
    det["falso_amigo"] = bool(FALSO_AMIGO.search(t))
    if not det["tema_forte"]:
        nota -= 5.0            # sem sinal forte do tema, não compete
    if det["falso_amigo"] and not det["tema_forte"]:
        nota -= 5.0            # é de outro domínio que fala a mesma língua
    det["suspeita_involucro"] = bool(S_INVOLUCRO.search(t))
    det["sem_texto"] = len((c.get("descricao_fonte") or "").strip()) < 20
    det["de_registro"] = any(r in (c.get("url") or "") for r in REGISTROS)
    return nota, det


def baixar(c: dict, modo: str) -> float:
    s = c.get("sinais") or {}
    if modo == "downloads":
        for k in ("downloads", "downloads_semana", "downloads_recentes"):
            if isinstance(s.get(k), (int, float)):
                return float(s[k])
        return float(s.get("estrelas") or 0)  # repositório não tem download
    if modo == "estrelas":
        return float(s.get("estrelas") or s.get("likes") or s.get("pontos") or 0)
    if modo == "raridade":
        return -len(c.get("fontes_extras") or [])
    if modo == "manutencao":
        bruto = s.get("ultimo_push") or s.get("atualizado") or ""
        try:
            return datetime.fromisoformat(str(bruto).replace("Z", "+00:00")).timestamp()
        except Exception:
            return 0.0
    return 0.0


# Cota por fonte no pool de enriquecimento. A lição da Entrega 1: ranquear tudo
# junto pela nota de proxy fez o topo virar repositório obscuro, porque todo
# README de agente escreve "multi-agent" e "trace" por hábito. Cota por fonte
# impede que a convenção de escrita de uma fonte sequestre a fila.
COTAS = {
    "npm": 260, "crates": 260, "nuget": 200, "packagist": 120, "rubygems": 120,
    "github": 420, "awesome": 320, "huggingface": 160, "hn": 160,
}
COTA_HERDADO = 480  # somada entre todas as fontes `herdado:*`


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--desempate", default="downloads",
                   choices=["downloads", "estrelas", "raridade", "manutencao"])
    p.add_argument("--pool", type=int, default=2500)
    args = p.parse_args()

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

    vivos.sort(key=lambda c: (c["nota_proxy"], baixar(c, args.desempate)), reverse=True)

    # O pool só aceita item com sinal forte do tema. Sem esse portão, a cota por
    # fonte enche com o que a fonte tem de mais popular, e não com o que é do
    # recorte — foi o que aconteceu na primeira execução.
    no_tema = [c for c in vivos if c["proxy"]["tema_forte"]]
    fora_do_tema = len(vivos) - len(no_tema)

    por_fonte: dict[str, list[dict]] = {}
    for c in no_tema:
        chave = "herdado" if c["fonte"].startswith("herdado:") else c["fonte"]
        por_fonte.setdefault(chave, []).append(c)

    pool: list[dict] = []
    usado: dict[str, int] = {}
    for fonte, itens in por_fonte.items():
        cota = COTA_HERDADO if fonte == "herdado" else COTAS.get(fonte, 100)
        escolhidos = itens[:cota]
        pool += escolhidos
        usado[fonte] = len(escolhidos)

    with (DADOS / "preselecao.jsonl").open("w", encoding="utf-8") as f:
        for c in pool:
            f.write(json.dumps(c, ensure_ascii=False) + "\n")

    por_motivo = Counter(m for _, m in mortos)
    vivos_por_fonte = Counter(c["fonte"] for c in vivos)
    mortos_por_fonte = Counter(c["fonte"] for c, _ in mortos)
    L = [
        "# Relatório da peneira mecânica — Entrega 2",
        "",
        f"Gerado em {datetime.now(timezone.utc).astimezone().isoformat(timespec='seconds')}",
        f"Desempate aplicado: **{args.desempate}**",
        "",
        f"- candidatos brutos: **{len(candidatos)}**",
        f"- eliminados por regra mecânica: **{len(mortos)}**",
        f"- sobreviventes: **{len(vivos)}**",
        f"- com sinal forte do tema (portão de relevância): **{len(no_tema)}**",
        f"- sobreviventes descartados do pool por não terem sinal forte: **{fora_do_tema}**",
        f"- enviados ao enriquecimento (pool): **{len(pool)}**",
        "",
        "## O que cada regra matou", "", "| motivo | quantos |", "|---|---|",
    ]
    L += [f"| {m} | {n} |" for m, n in por_motivo.most_common()]
    L += ["", "## Sobrevivência por fonte", "",
          "| fonte | sobreviveu | morreu |", "|---|---|---|"]
    for f in sorted(set(vivos_por_fonte) | set(mortos_por_fonte)):
        L.append(f"| {f} | {vivos_por_fonte.get(f, 0)} | {mortos_por_fonte.get(f, 0)} |")
    L += ["", "## Cota por fonte no pool de enriquecimento", "",
          "O pool não é o top-N por nota. Ranquear tudo junto pela nota de proxy foi tentado",
          "na Entrega 1 e falhou: o topo virou repositório obscuro, porque todo README de",
          "agente escreve 'multi-agent' e 'trace' por hábito. A nota mede vocabulário, não",
          "substância — daí a cota por fonte.", "",
          "| fonte | sobreviventes | entraram no pool |", "|---|---|---|"]
    L += [f"| {f} | {len(por_fonte.get(f, []))} | {usado.get(f, 0)} |" for f in sorted(por_fonte)]
    L += ["", "## Amostra do que o SEU critério derrubou", "",
          "Dez eliminados de maior popularidade — para conferir se aceita a perda.", ""]
    for c, m in sorted(mortos, key=lambda x: baixar(x[0], "estrelas"), reverse=True)[:10]:
        s = c.get("sinais") or {}
        L.append(f"- **{c['nome']}** ({s.get('estrelas') or s.get('downloads') or '?'}) — "
                 f"{c['url']}  \n  motivo: {m}")
    (DADOS / "relatorio_peneira.md").write_text("\n".join(L) + "\n", encoding="utf-8")

    print(f"brutos {len(candidatos)} | eliminados {len(mortos)} | vivos {len(vivos)} | "
          f"pool {len(pool)}")
    for m, n in por_motivo.most_common():
        print(f"  {n:>6}  {m}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
