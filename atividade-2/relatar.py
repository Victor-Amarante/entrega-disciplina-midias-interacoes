"""Gera o anexo técnico da Entrega 2 a partir do que REALMENTE aconteceu.

Nada aqui é escrito à mão: todo número sai de `dados/log_bruto.jsonl` e de
`dados/candidatos.jsonl`, e todo texto de método e de viés sai das constantes
`METODO` e `VIES` declaradas dentro do próprio adaptador de cada fonte. Se a
varredura mudar, o relatório muda junto — o documento não tem como discordar
do que rodou.

O que este script NÃO faz: escrever o item 3 nem o item 4 da entrega no lugar
do aluno. Ele produz a matéria-prima medida. O julgamento sobre o recorte, o
que ficou de fora e se ele assume isso é dele, e vai por cima.
"""

from __future__ import annotations

import collections
import importlib
import json
import sys
from datetime import datetime
from pathlib import Path
from urllib.parse import urlsplit

RAIZ = Path(__file__).parent
sys.path.insert(0, str(RAIZ))
DADOS = RAIZ / "dados"
SAIDA = RAIZ / "entrega"

FONTES = ["herdados", "registros", "pypi", "github", "awesome", "huggingface", "hn"]


def ler_log():
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
        elif t not in ("inicio_varredura", "fim_varredura"):
            eventos.append(d)
    return req_host, status, itens, eventos


# Um adaptador colhe sob rótulos que não são o nome do módulo (registros -> npm,
# crates, …; herdados -> herdado:*). Este mapa junta os dois para o relatório.
ROTULOS = {
    "registros": ("npm", "crates", "nuget", "packagist", "rubygems"),
    "herdados": ("herdados",),
}


def soma(contador, nome) -> int:
    rotulos = ROTULOS.get(nome, (nome,))
    return sum(v for k, v in contador.items()
               if k in rotulos or k.startswith(nome) or k.startswith("herdado:") and nome == "herdados")


def main() -> int:
    SAIDA.mkdir(parents=True, exist_ok=True)
    req_host, status, itens, eventos = ler_log()

    candidatos = []
    arq = DADOS / "candidatos.jsonl"
    if arq.exists():
        for l in arq.read_text(encoding="utf-8").splitlines():
            if l.strip():
                try:
                    candidatos.append(json.loads(l))
                except json.JSONDecodeError:
                    pass
    por_fonte = collections.Counter(c["fonte"] for c in candidatos)
    por_faceta = collections.Counter((c.get("sinais") or {}).get("faceta", "?")
                                     for c in candidatos)
    multi = sum(1 for c in candidatos if c.get("fontes_extras"))

    L = [
        "# Anexo técnico — Entrega 2: fontes varridas, viés e números medidos", "",
        "> **Como este arquivo foi produzido.** Gerado por `relatar.py` a partir de",
        "> `dados/log_bruto.jsonl` e `dados/candidatos.jsonl`. Todo número foi medido,",
        "> nenhum estimado. Método e viés de cada fonte estão declarados nas constantes",
        "> `METODO` e `VIES` dentro do adaptador correspondente, em `garimpo/fontes/` —",
        "> são a leitura do coletor. O julgamento sobre aceitar esse recorte é do aluno",
        "> e não está neste arquivo.", "",
        f"Gerado em {datetime.now().astimezone().isoformat(timespec='seconds')}", "",
        "## O que esta unidade coleta", "",
        "APIs, bibliotecas, SDKs, frameworks, componentes e código aberto que possam ser",
        "instalados, importados ou chamados de dentro do código. Aplicativo usado à mão",
        "é Entrega 1 — e foi entregue separadamente, com o mesmo tema visto pelo outro lado.",
        "", "## Números da varredura", "",
        f"- itens brutos colhidos (antes da deduplicação): **{sum(itens.values())}**",
        f"- requisições HTTP feitas: **{sum(req_host.values())}**",
        f"- candidatos únicos após deduplicação: **{len(candidatos)}**",
        f"- candidatos vistos em mais de uma fonte: **{multi}**", "",
        "### Requisições por host", "", "| host | requisições |", "|---|---|",
    ]
    L += [f"| `{h}` | {n} |" for h, n in req_host.most_common()]
    L += ["", "### Códigos de resposta", "", "| status | ocorrências |", "|---|---|"]
    L += [f"| {s} | {n} |" for s, n in sorted(status.items(), key=lambda x: -x[1])]
    L += ["", "_status -1 = falha de rede/timeout; 999 = requisição não feita por robots.txt._",
          "", "### Itens brutos por rótulo de coleta", "",
          "| rótulo | itens brutos | candidatos únicos |", "|---|---|---|"]
    for f in sorted(set(itens) | set(por_fonte)):
        L.append(f"| {f} | {itens.get(f, 0)} | {por_fonte.get(f, 0)} |")
    L += ["", "### Candidatos por faceta do vocabulário", "",
          "A faceta vem de `garimpo/consultas.py`. Faceta com número baixo significa que",
          "aquele recorte rendeu pouco — pode ser que o assunto seja raro, ou que os termos",
          "estejam errados. As duas hipóteses são do aluno.", "",
          "| faceta | candidatos |", "|---|---|"]
    L += [f"| {f} | {n} |" for f, n in por_faceta.most_common()]

    L += ["", "## Método e viés de cada fonte", "",
          "Cada bloco abaixo sai do próprio adaptador: **como** aquela fonte foi varrida e",
          "**o que ela sistematicamente não mostra**.", ""]
    for nome in FONTES:
        try:
            mod = importlib.import_module(f"garimpo.fontes.{nome}")
        except Exception as e:
            L.append(f"### {nome}\n\n_não foi possível carregar o adaptador: {e}_\n")
            continue
        L.append(f"### {nome}")
        L.append("")
        L.append(f"**Rendimento medido:** {soma(itens, nome)} itens brutos → "
                 f"{soma(por_fonte, nome)} candidatos únicos.")
        L.append("")
        L.append(f"**Como foi varrida.** {getattr(mod, 'METODO', '_não declarado._')}")
        L.append("")
        L.append(f"**Viés — o que esta fonte sistematicamente NÃO mostra.** "
                 f"{getattr(mod, 'VIES', '_não declarado._')}")
        L.append("")

    L += ["## Incidentes registrados no log", "",
          "O que quebrou, o que foi bloqueado e o que foi decidido no meio do caminho.", "",
          "| tipo | fonte/host | detalhe | ocorrências |", "|---|---|---|---|"]
    agr = collections.Counter(
        (d["tipo"], str(d.get("fonte", "") or d.get("host", ""))[:40],
         str(d.get("motivo", "") or d.get("aviso", "") or d.get("status", ""))[:80])
        for d in eventos)
    L += [f"| `{t}` | {f} | {m} | {n} |" for (t, f, m), n in agr.most_common(30)]

    L += ["", "## Fontes consideradas e NÃO varridas", "",
          "| fonte | por quê |", "|---|---|",
          "| **PyPI (busca)** | `pypi.org/search/` responde 200 mas devolve desafio JavaScript "
          "(proteção anti-bot). Não contornado — mesma decisão tomada na Entrega 1 com "
          "theresanaiforthat e toolify. O PyPI **foi** varrido pelo sitemap, que o próprio "
          "`robots.txt` publica. |",
          "| **Papers with Code** | a API `paperswithcode.com/api/v1/` devolve HTML em vez de "
          "JSON: está desativada. |",
          "| **libraries.io** | a API exige chave (401 sem ela). |",
          "| **pkg.go.dev** | `robots.txt` proíbe `/search?*`; sobraria só o sitemap, que não "
          "foi varrido por falta de tempo — buraco declarado, não resolvido. |",
          "| **ecosyste.ms** | `ConnectTimeout` em todas as chamadas a partir desta rede. |",
          "| **OpenAlex** | funciona e foi testada, mas foi descartada de propósito: devolve "
          "artigo científico, e artigo reprova no critério E1 desta entrega (não se instala "
          "nem se importa). |",
          "| **Reddit** | `robots.txt` proíbe coleta automatizada de todo o site, como já "
          "medido na Entrega 1. |",
          "| **Maven, CocoaPods, pub.dev, Hex** | não varridos por escolha de escopo: o tema "
          "quase não vive nesses ecossistemas. Buraco conhecido. |", ""]

    destino = SAIDA / "anexo-tecnico-fontes.md"
    destino.write_text("\n".join(L) + "\n", encoding="utf-8")
    print(f"escrito: {destino}")
    print(f"  {sum(itens.values())} itens brutos | {sum(req_host.values())} requisições | "
          f"{len(candidatos)} candidatos únicos")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
