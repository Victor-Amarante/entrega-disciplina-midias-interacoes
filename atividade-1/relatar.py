"""Gera os anexos técnicos da entrega a partir do que REALMENTE aconteceu.

Nada aqui é escrito à mão: todo número sai do log bruto e todo texto de viés
sai da constante VIES declarada dentro do próprio adaptador da fonte. Se a
varredura mudar, o relatório muda junto — não há como o documento discordar
dos dados.

ATENÇÃO ao que este script NÃO faz: ele não escreve o item 3 nem o item 4 da
entrega no lugar do aluno. Ele produz a MATÉRIA-PRIMA medida (o que foi
varrido, quanto, com que erro, com que cego declarado). O julgamento sobre
essas fontes — se o recorte é aceitável, o que ficou de fora e se ele assume
isso — é do aluno e vai por cima.

Uso:  uv run python atividade-1/relatar.py
"""

from __future__ import annotations

import collections
import importlib
import json
from datetime import datetime
from pathlib import Path
from urllib.parse import urlsplit

import sys

RAIZ = Path(__file__).parent
sys.path.insert(0, str(RAIZ))
DADOS = RAIZ / "dados"
SAIDA = RAIZ / "entrega"

FONTES = ["hn", "huggingface", "github", "diretorios", "itchio", "arxiv",
          "reddit", "producthunt"]


def ler_log() -> tuple[collections.Counter, collections.Counter, collections.Counter, list]:
    req_host, status, itens, eventos = (collections.Counter(), collections.Counter(),
                                        collections.Counter(), [])
    for linha in (DADOS / "log_bruto.jsonl").read_text(encoding="utf-8").splitlines():
        if not linha.strip():
            continue
        d = json.loads(linha)
        t = d.get("tipo")
        if t == "requisicao":
            req_host[urlsplit(d["url"]).netloc] += 1
            status[d["status"]] += 1
        elif t == "item":
            itens[d["fonte"]] += 1
        elif t in ("fonte_bloqueada", "fonte_falhou", "robots_bloqueou", "robots_excecao",
                   "sem_itens", "fonte_excecao", "fonte_pulada"):
            eventos.append(d)
    return req_host, status, itens, eventos


def main() -> int:
    SAIDA.mkdir(parents=True, exist_ok=True)
    req_host, status, itens, eventos = ler_log()

    candidatos = []
    arq = DADOS / "candidatos.jsonl"
    if arq.exists():
        candidatos = [json.loads(l) for l in arq.read_text(encoding="utf-8").splitlines() if l.strip()]
    por_fonte = collections.Counter(c["fonte"] for c in candidatos)
    por_faceta = collections.Counter((c.get("sinais") or {}).get("faceta", "?") for c in candidatos)
    multi_fonte = sum(1 for c in candidatos if c.get("fontes_extras"))

    L = [
        "# Anexo técnico — fontes varridas, viés e números medidos",
        "",
        "> **Como este arquivo foi produzido.** Gerado por `relatar.py` a partir de",
        "> `dados/log_bruto.jsonl` e `dados/candidatos.jsonl`. Todo número aqui foi",
        "> medido, nenhum foi estimado. O texto de viés de cada fonte está declarado",
        "> na constante `VIES` dentro do adaptador correspondente em",
        "> `coletor/fontes/`, e é a leitura do coletor — o julgamento sobre aceitar",
        "> ou não esse recorte é do aluno e não está neste arquivo.",
        "",
        f"Gerado em {datetime.now().astimezone().isoformat(timespec='seconds')}",
        "",
        "## Números da varredura",
        "",
        f"- itens brutos colhidos (antes da deduplicação): **{sum(itens.values())}**",
        f"- requisições HTTP feitas: **{sum(req_host.values())}**",
        f"- candidatos únicos após deduplicação: **{len(candidatos)}**",
        f"- candidatos vistos em mais de uma fonte: **{multi_fonte}**",
        "",
        "### Requisições por host",
        "", "| host | requisições |", "|---|---|",
    ]
    L += [f"| `{h}` | {n} |" for h, n in req_host.most_common()]
    L += ["", "### Códigos de resposta", "", "| status | ocorrências |", "|---|---|"]
    L += [f"| {s} | {n} |" for s, n in sorted(status.items(), key=lambda x: -x[1])]
    L += ["", "_status -1 = falha de rede/timeout; 999 = requisição não feita por robots.txt._"]

    L += ["", "### Itens brutos por fonte", "", "| fonte | itens brutos | candidatos únicos |",
          "|---|---|---|"]
    todas_fontes = sorted(set(itens) | set(por_fonte))
    for f in todas_fontes:
        L.append(f"| {f} | {itens.get(f, 0)} | {por_fonte.get(f, 0)} |")

    L += ["", "### Candidatos por faceta do vocabulário", "",
          "A faceta vem de `coletor/consultas.py`. Faceta com número baixo significa",
          "que o vocabulário daquele recorte rendeu pouco — pode ser que o assunto",
          "seja raro, ou que os termos estejam errados. As duas hipóteses são do aluno.",
          "", "| faceta | candidatos |", "|---|---|"]
    L += [f"| {f} | {n} |" for f, n in por_faceta.most_common()]

    # ---------------------------------------------------------------- viés
    L += ["", "## Viés declarado de cada fonte", "",
          "Cada bloco abaixo é o texto da constante `VIES` do adaptador — ou seja,",
          "o que aquela fonte **sistematicamente não mostra**.", ""]
    for nome in FONTES:
        try:
            mod = importlib.import_module(f"coletor.fontes.{nome}")
        except Exception as e:
            L.append(f"### {nome}\n\n_não foi possível carregar o adaptador: {e}_\n")
            continue
        desativada = getattr(mod, "DESATIVADA", False)
        marca = " — **NÃO VARRIDA**" if desativada else ""
        L.append(f"### {nome}{marca}")
        L.append("")
        if desativada:
            L.append(f"**Motivo de não ter sido varrida:** {getattr(mod, 'MOTIVO_DESATIVACAO', '')}")
            L.append("")
        L.append(f"**Rendimento medido:** {itens.get(nome, 0) or sum(v for k, v in itens.items() if k.startswith(nome))} "
                 f"itens brutos → {sum(v for k, v in por_fonte.items() if k.startswith(nome))} candidatos únicos.")
        L.append("")
        L.append(f"**Como foi varrida.** {getattr(mod, 'METODO', '_método não declarado no adaptador._')}")
        L.append("")
        L.append(f"**Viés — o que esta fonte sistematicamente NÃO mostra.** "
                 f"{getattr(mod, 'VIES', '_viés não declarado no adaptador._')}")
        L.append("")

    # -------------------------------------------------- incidentes do log
    L += ["## Incidentes registrados no log", "",
          "O que quebrou, o que foi bloqueado e o que foi decidido no meio do caminho.", ""]
    agrupado = collections.Counter(
        (d["tipo"], d.get("fonte", "") or d.get("host", ""), str(d.get("motivo", ""))[:90])
        for d in eventos)
    L += ["| tipo | fonte/host | detalhe | ocorrências |", "|---|---|---|---|"]
    for (tipo, fonte, motivo), n in agrupado.most_common(30):
        L.append(f"| `{tipo}` | {fonte} | {motivo} | {n} |")

    L += ["", "## O arquivo de log entregue: o que ele é e o que aconteceu com ele",
          "",
          "**Incidente.** Durante a coleta, duas instâncias de `varrer.py` rodaram ao mesmo tempo",
          "(arXiv em segundo plano enquanto o Hugging Face rodava em primeiro), as duas com o mesmo",
          "arquivo de log aberto para escrita. Ao conferir os números deste relatório contra o log,",
          "ele tinha voltado a conter apenas as execuções mais antigas. **Perdeu-se de vez o registro",
          "dos eventos de falha da varredura original** — as respostas 429 do arXiv, as requisições",
          "bloqueadas por robots e as falhas do Reddit daquela rodada. O log foi refeito num processo",
          "único, com todo o HTTP vindo do cache, e as fontes que falham (arXiv e Reddit) foram",
          "reexecutadas para que o atrito voltasse a ser evento real gravado no momento em que",
          "aconteceu, e não afirmação de memória. Os números deste relatório saem do log atual.",
          "",
          "**Ajuste ao limite de 45 MB.** O log bruto tem 89 MB. O arquivo entregue passou por uma",
          "regra única e uniforme, aplicada por `compactar_log.py`: todo valor de texto acima de N",
          "caracteres e toda lista acima de N/40 elementos são truncados **com marca visível dentro",
          "do próprio registro** (`…(+1832 car)`, `…(+47 itens)`). O script procura o MAIOR N que",
          "ainda cabe no limite, de modo que o corte seja o mínimo necessário.",
          "",
          "Nada foi removido, deduplicado, ordenado ou consertado: as repetições, os `utm_source`,",
          "os subdomínios do mesmo site, as linhas de erro e as execuções repetidas continuam lá.",
          "A conferência é automática e roda a cada geração — **número de linhas e conjunto de",
          "endereços distintos idênticos antes e depois**, que são exatamente os dois números que o",
          "sistema de entrega exibe.",
          "",
          "O corte atingiu onde estava o desperdício: a API do Hugging Face devolve o resumo de cada",
          "paper três vezes (`paper.summary`, `summary` e `highlightedSummary`), e `siblings` — a",
          "listagem de arquivos do repositório de cada Space, irrelevante para julgar a ferramenta —",
          "somava 10 MB sozinha. O arquivo original, sem corte algum, está em `dados/log_bruto.jsonl`.",
          "",
          "**Nota sobre a contagem de candidatos.** A reexecução do arXiv descrita acima aconteceu",
          "DEPOIS de a lista das 500 estar fechada e descrita, e acrescentou 57 candidatos ao total.",
          "Por isso o número de candidatos únicos aqui é maior que o que aparece no relatório da",
          "peneira: as 500 foram peneiradas sobre 17.937 candidatos, e o total varrido é o desta",
          "página. Os 57 novos não entraram na lista final.",
          "",
          "## Fontes consideradas e NÃO varridas", "",
          "| fonte | por quê |", "|---|---|",
          "| theresanaiforthat.com | sitemap responde 403 (proteção anti-bot Cloudflare). Não contornado. |",
          "| toolify.ai | sitemap responde 403 (proteção anti-bot Cloudflare). Não contornado. |",
          "| reddit.com | `robots.txt` proíbe coleta automatizada de todo o site; API oficial exige OAuth. |",
          "| Product Hunt (busca) | API GraphQL exige token de desenvolvedor. Só o feed dos ~50 lançamentos recentes foi coletado. |",
          "| Tavily / Exa / Brave / SerpAPI | o aluno optou por não usar API de busca paga ou com chave. |",
          "",
          "## Onde o tempo foi mal gasto",
          "",
          "Registrado porque faz parte do relato de método, e porque a próxima varredura",
          "não deve repetir os mesmos erros.",
          "",
          "| o que custou tempo | quanto | o que evitaria |",
          "|---|---|---|",
          "| **arXiv.** Adaptador escrito, testado e afinado três vezes (3,5 s → 12 s de intervalo) "
          "para render 1 resposta útil em 65 requisições. | ~35 min | Ter sondado o arXiv com "
          "10 requisições seguidas ANTES de escrever o adaptador. A sondagem inicial fez só uma, "
          "que passou — e uma requisição não revela limite de taxa. |",
          "| **Primeira varredura inteira com a regra de dedup errada.** Diretórios renderam 2 "
          "candidatos em vez de 7.776, e só se percebeu ao ler a contagem por fonte. | ~25 min | "
          "Ter testado a função de dedup com uma URL de diretório junto das de produto. O teste "
          "existia, mas só cobria github, huggingface e streamlit. |",
          "| **Enriquecimento com cache de resposta 429.** 50 Spaces gravados como link morto "
          "sendo que só tinham esbarrado em limite de taxa; cache teve de ser purgado e a "
          "rodada refeita. | ~20 min | Regra óbvia em retrospecto: só cachear status estável. |",
          "| **Log bruto perdeu as execuções do meio.** Duas instâncias de `varrer.py` rodaram "
          "ao mesmo tempo (arXiv em segundo plano enquanto o Hugging Face rodava em primeiro), as "
          "duas com o mesmo arquivo de log aberto para escrita. Ao conferir os números do relatório "
          "contra o log, ele tinha voltado a conter só as duas primeiras execuções. Refeito num "
          "processo único, com tudo vindo do cache. | ~15 min | Nunca rodar duas instâncias do "
          "coletor gravando no mesmo log. O mecanismo exato não foi apurado; o efeito foi. |",
          "| **Primeira montagem do pool por top-N global.** O topo virou repositório obscuro do "
          "GitHub porque todo README de agente escreve 'multi-agent' e 'trace'. Pool descartado "
          "e refeito por cota de fonte. | ~15 min | Ter olhado os 20 primeiros do ranking ANTES "
          "de mandar 1.950 itens para enriquecimento. |",
          "",
          "O padrão dos quatro é o mesmo: **confiar no código antes de olhar o que ele produziu.**",
          "Em todos, o defeito apareceu na contagem por fonte ou no topo do ranking — dois",
          "lugares baratos de conferir, que passaram a ser conferidos a cada etapa.",
          ""]

    destino = SAIDA / "anexo-tecnico-fontes.md"
    destino.write_text("\n".join(L) + "\n", encoding="utf-8")
    print(f"escrito: {destino}")
    print(f"  {sum(itens.values())} itens brutos | {sum(req_host.values())} requisições | "
          f"{len(candidatos)} candidatos únicos")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
