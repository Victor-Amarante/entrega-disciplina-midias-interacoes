"""Fase D da Entrega 2 — repontuar sobre o README real e montar a fila das 500.

Diferença em relação à peneira: lá a pontuação olhava nome, URL e a descrição
curta que a fonte deu. Aqui ela olha o README do projeto, buscado e verificado
em `enriquecer.py`. É a diferença entre "o nome tem a palavra agent" e "o
projeto explica que agentes se afetam".

E é aqui que os eliminatórios do aluno finalmente têm dado para decidir:

  E1  instalável — prova concreta: publicado em registro de pacote, ou comando
      de instalação encontrado no README (`pip install`, `cargo add`, …).
  E3  licença aberta declarada — campo do registro ou da API do GitHub.
  E4  invólucro fino — continua sendo SUSPEITA marcada, porque nenhuma regra
      decide isso; a conferência é de leitura.

Saídas:
  dados/ranqueado.jsonl        tudo, ordenado, com nota e evidência
  dados/para_descrever.jsonl   os N do topo, com o texto junto
  dados/relatorio_julgamento.md
"""

from __future__ import annotations

import argparse
import collections
import hashlib
import json
import re
import sys
from datetime import datetime
from pathlib import Path

RAIZ = Path(__file__).parent
sys.path.insert(0, str(RAIZ))
DADOS = RAIZ / "dados"

from peneirar import (  # noqa: E402
    P1_MULTIAGENTE, P2_ESTADO_POR_DENTRO, P3_AMBIENTE_POR_CODIGO, P4_REPRODUTIVEL,
    S_INVOLUCRO, PESOS, baixar,
)

# Licenças abertas reconhecidas. Fora daqui (ou vazio) reprova em E3.
ABERTAS = {
    "MIT", "APACHE-2.0", "APACHE 2.0", "BSD-3-CLAUSE", "BSD-2-CLAUSE", "BSD",
    "GPL-3.0", "GPL-2.0", "AGPL-3.0", "LGPL-3.0", "LGPL-2.1", "MPL-2.0",
    "ISC", "UNLICENSE", "CC0-1.0", "EPL-2.0", "BSL-1.0", "ZLIB", "PSF-2.0",
    "APACHE-2.0 OR MIT", "MIT OR APACHE-2.0", "CC-BY-4.0", "CC-BY-SA-4.0",
    "OPENRAIL", "BIGSCIENCE-OPENRAIL-M", "LLAMA2", "LLAMA3", "GEMMA",
}


def normalizar_licenca(v) -> str:
    if not v:
        return ""
    if isinstance(v, list):
        v = ", ".join(str(x) for x in v)
    return str(v).strip().upper()


# Alguns registros declaram a licença como URL (o NuGet antigo faz isso) ou
# como nome de arquivo ("LICENSE"). URL dá para resolver pelo endereço; nome de
# arquivo não diz qual licença é, e por isso não conta como licença aberta
# DECLARADA — que é o que o critério E3 do aluno exige.
URL_PARA_LICENCA = (
    ("apache.org/licenses/license-2.0", "APACHE-2.0"),
    ("opensource.org/licenses/mit", "MIT"),
    ("opensource.org/licenses/bsd", "BSD"),
    ("gnu.org/licenses/agpl", "AGPL-3.0"),
    ("gnu.org/licenses/lgpl", "LGPL-3.0"),
    ("gnu.org/licenses/gpl", "GPL-3.0"),
    ("gnu.org/copyleft/gpl", "GPL-3.0"),
    ("mozilla.org/en-us/mpl", "MPL-2.0"),
    ("unlicense.org", "UNLICENSE"),
    ("creativecommons.org/publicdomain/zero", "CC0-1.0"),
    ("licenses/mit", "MIT"), ("licenses/apache", "APACHE-2.0"),
)
ARQUIVO_DE_LICENCA = {"LICENSE", "LICENSE.TXT", "LICENSE.MD", "LICENCE",
                      "COPYING", "LICENSE-MIT", "LICENSE.RST"}


def resolver_url(v: str) -> str:
    baixo = v.lower()
    for pedaco, nome in URL_PARA_LICENCA:
        if pedaco in baixo:
            return nome
    return v


def aberta(v: str) -> bool:
    if v in ARQUIVO_DE_LICENCA:
        return False  # aponta para um arquivo, não diz qual licença é
    if v.startswith(("HTTP://", "HTTPS://")):
        v = resolver_url(v)
    if not v or v in ("NOASSERTION", "NONE", "UNLICENSED", "PROPRIETARY", "OTHER"):
        return False
    if v in ABERTAS:
        return True
    # licença composta ou com sufixo de versão: basta um pedaço reconhecido
    return any(a in v for a in ("MIT", "APACHE", "BSD", "GPL", "MPL", "ISC",
                                "UNLICENSE", "CC0", "CC-BY", "EPL", "ZLIB", "OPENRAIL"))


# --- colapso de família de pacotes -----------------------------------------
# Achado ao ler o topo das 500: `autoagents`, `autoagents-core`,
# `autoagents-llm`, `autoagents-derive` e `autoagents-protocol` são cinco
# entradas do MESMO projeto, com o MESMO README. O caso extremo tinha 12
# (`ascending-ai/lash`) e a Microsoft aparecia com 9 pacotes de `autogen`.
# Medido: 66 famílias, 208 pacotes — 142 das 500 vagas iriam para subpacote
# redundante, 28% da lista.
#
# A regra: duas entradas que apontam para o MESMO repositório são o mesmo
# PROJETO, e projeto é a unidade que interessa a quem procura ferramenta.
# Fica o pacote com mais downloads (desempate escolhido pelo aluno); em caso de
# empate, o de nome mais curto, que costuma ser o pacote principal e não o
# módulo satélite. Os irmãos não somem: ficam listados em `pacotes_irmaos`,
# porque saber que o projeto se distribui em 12 crates é informação útil.
#
# Quando não há repositório declarado, a impressão digital dos primeiros 600
# caracteres do README faz o mesmo trabalho — README idêntico é o sinal mais
# forte de que se trata do mesmo projeto publicado várias vezes.
_GH = re.compile(r"github\.com[:/]([\w.\-]+)/([\w.\-]+)")


def familia(c: dict) -> str:
    d = c.get("detalhe") or {}
    for origem in (d.get("repositorio") or "", c.get("url") or ""):
        m = _GH.search(origem)
        if m:
            return "repo:" + f"{m.group(1)}/{m.group(2)}".lower().removesuffix(".git")
    readme = (c.get("texto") or {}).get("readme", "")[:600].strip()
    if len(readme) > 200:
        return "rdm:" + hashlib.sha256(readme.encode()).hexdigest()[:16]
    return "url:" + (c.get("url") or "")


def colapsar(itens: list[dict]) -> tuple[list[dict], int]:
    grupos: dict[str, list[dict]] = {}
    for c in itens:
        grupos.setdefault(familia(c), []).append(c)
    saida, colapsados = [], 0
    for _, membros in grupos.items():
        if len(membros) == 1:
            saida.append(membros[0])
            continue
        membros.sort(key=lambda c: (-(float((c.get("detalhe") or {}).get("downloads") or 0)),
                                    len(c.get("nome") or "")))
        principal = membros[0]
        principal["pacotes_irmaos"] = [m.get("nome") for m in membros[1:]]
        colapsados += len(membros) - 1
        saida.append(principal)
    return saida, colapsados


def texto_real(c: dict) -> str:
    t = c.get("texto") or {}
    s = c.get("sinais") or {}
    extras = []
    for k in ("topicos", "palavras_chave"):
        v = s.get(k)
        if isinstance(v, list):
            extras.append(" ".join(str(x) for x in v))
    return " ".join([c.get("nome", ""), t.get("descricao", ""), t.get("readme", "")] + extras)


def julgar(c: dict) -> dict:
    t = texto_real(c)
    d = c.get("detalhe") or {}
    lic = normalizar_licenca(d.get("licenca"))
    if lic.startswith(("HTTP://", "HTTPS://")):
        lic = resolver_url(lic)

    ev = {
        "P1": bool(P1_MULTIAGENTE.search(t)),
        "P2": bool(P2_ESTADO_POR_DENTRO.search(t)),
        "P3": bool(P3_AMBIENTE_POR_CODIGO.search(t)),
        "P4": bool(P4_REPRODUTIVEL.search(t)),
    }
    nota = sum(PESOS[k] for k, v in ev.items() if v)

    ev["instalavel"] = bool(d.get("instalavel"))
    ev["prova_instalacao"] = d.get("prova_instalacao", "")
    ev["licenca"] = lic
    ev["licenca_aberta"] = aberta(lic)
    ev["tem_readme"] = bool(d.get("tem_readme"))
    ev["suspeita_involucro"] = bool(S_INVOLUCRO.search(t))
    ev["texto_curto"] = len((c.get("texto") or {}).get("readme", "")) < 300
    ev["status"] = d.get("status")

    # E1 e E3 são eliminatórios do aluno: reprovam, não penalizam.
    reprova = None
    if not ev["instalavel"]:
        reprova = "E1: sem prova de que instala ou importa"
    elif not ev["licenca_aberta"]:
        reprova = ("E3: sem licença aberta declarada"
                   if not lic else f"E3: licença não aberta ou não reconhecida ({lic[:40]})")
    ev["reprovado"] = reprova

    # E4 não é decidível por máquina: empurra para baixo e marca para leitura.
    if ev["suspeita_involucro"]:
        nota -= 2.0
    if ev["texto_curto"]:
        nota -= 1.5

    c["nota"] = round(nota, 2)
    c["evidencia"] = ev
    return c


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--desempate", default="downloads",
                   choices=["downloads", "estrelas", "raridade", "manutencao"])
    p.add_argument("--quantos", type=int, default=500)
    args = p.parse_args()

    validos = set()
    pre = DADOS / "preselecao.jsonl"
    if pre.exists():
        for l in pre.read_text(encoding="utf-8").splitlines():
            if l.strip():
                validos.add(json.loads(l)["url"])

    itens, fora_da_peneira = [], 0
    for l in (DADOS / "enriquecidos.jsonl").read_text(encoding="utf-8").splitlines():
        if not l.strip():
            continue
        try:
            d = json.loads(l)
        except json.JSONDecodeError:
            continue
        if validos and d["url"] not in validos:
            fora_da_peneira += 1
            continue
        itens.append(julgar(d))
    if fora_da_peneira:
        print(f"{fora_da_peneira} itens enriquecidos descartados por não passarem "
              f"mais na peneira atual")

    aprovados = [c for c in itens if not c["evidencia"]["reprovado"]]
    reprovados = [c for c in itens if c["evidencia"]["reprovado"]]
    aprovados, colapsados = colapsar(aprovados)
    aprovados.sort(key=lambda c: (c["nota"], baixar(c, args.desempate)), reverse=True)
    print(f"colapso de família: {colapsados} subpacotes do mesmo projeto recolhidos "
          f"no seu pacote principal")

    (DADOS / "ranqueado.jsonl").write_text(
        "\n".join(json.dumps(c, ensure_ascii=False) for c in aprovados) + "\n",
        encoding="utf-8")

    topo = aprovados[: args.quantos]
    with (DADOS / "para_descrever.jsonl").open("w", encoding="utf-8") as f:
        for c in topo:
            d = c.get("detalhe") or {}
            f.write(json.dumps({
                "nome": c["nome"], "url": c["url"], "url_coletada": c["url"],
                "fonte": c["fonte"], "faceta": (c.get("sinais") or {}).get("faceta"),
                "nota": c["nota"], "evidencia": c["evidencia"],
                "sinais": c.get("sinais"), "detalhe": d,
                "descricao": (c.get("texto") or {}).get("descricao", ""),
                "readme": (c.get("texto") or {}).get("readme", "")[:1800],
                "pacotes_irmaos": c.get("pacotes_irmaos") or [],
            }, ensure_ascii=False) + "\n")

    por_motivo = collections.Counter(c["evidencia"]["reprovado"] for c in reprovados)
    por_fonte = collections.Counter(c["fonte"] for c in topo)
    L = [
        "# Relatório do julgamento sobre o README real — Entrega 2", "",
        f"Gerado em {datetime.now().astimezone().isoformat(timespec='seconds')}",
        f"Desempate: **{args.desempate}** · Fila para descrição: **{len(topo)}**", "",
        f"- itens enriquecidos e julgados: **{len(itens)}**",
        f"- aprovados nos eliminatórios E1 e E3: **{len(aprovados)}**",
        f"- reprovados: **{len(reprovados)}**",
        f"- subpacotes do mesmo projeto colapsados no principal: **{colapsados}**",
        "", "Colapso de família: duas entradas que apontam para o mesmo repositório são o",
        "mesmo PROJETO. Fica o pacote com mais downloads; os irmãos ficam registrados em",
        "`pacotes_irmaos` e não desaparecem. Sem esta regra, 142 das 500 vagas iriam para",
        "subpacote redundante — 9 do `microsoft/autogen`, 12 do `ascending-ai/lash`.", "",
        "## Por que cada um reprovou", "", "| motivo | quantos |", "|---|---|",
    ]
    L += [f"| {m} | {n} |" for m, n in por_motivo.most_common(12)]
    L += ["", "## Composição da fila das 500", "", "| fonte | itens |", "|---|---|"]
    L += [f"| {f} | {n} |" for f, n in por_fonte.most_common()]
    L += ["", "## Suspeitas marcadas na fila (E4)", "",
          f"- suspeita de invólucro fino sem substância: "
          f"**{sum(1 for c in topo if c['evidencia']['suspeita_involucro'])}**", "",
          "Nenhuma regra decide isso. O número diz quantos itens da fila precisam de",
          "conferência de leitura antes de entrarem nas 50.", "",
          "## Licenças na fila", "", "| licença | itens |", "|---|---|"]
    L += [f"| {l or '(vazia)'} | {n} |" for l, n in
          collections.Counter(c["evidencia"]["licenca"] for c in topo).most_common(15)]
    L += ["", "## Faixa de nota", "",
          f"- maior: {topo[0]['nota'] if topo else '-'}",
          f"- menor: {topo[-1]['nota'] if topo else '-'}",
          f"- itens com nota negativa na fila: **{sum(1 for c in topo if c['nota'] < 0)}** "
          "(número alto significa fila preenchida com sobra, não com mérito)"]
    (DADOS / "relatorio_julgamento.md").write_text("\n".join(L) + "\n", encoding="utf-8")

    print(f"julgados {len(itens)} | aprovados {len(aprovados)} | reprovados {len(reprovados)} "
          f"| fila {len(topo)}")
    for m, n in por_motivo.most_common(6):
        print(f"  {n:>6}  {m}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
