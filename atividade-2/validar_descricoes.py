"""[CÓPIA DA ENTREGA 1] Utilitário de conferência das descrições, idêntico ao de
`atividade-1/validar_descricoes.py`, com os caminhos apontando para esta pasta. Foi copiado em
vez de importado porque as duas entregas precisam continuar rodando de forma
independente uma da outra.

Confere as descrições escritas à mão antes de elas entrarem no documento das 500.

O enunciado é específico sobre onde quase todo mundo erra, então isto checa
exatamente isso:

  - vocabulário de propaganda proibido ("revolucionário", "poderoso",
    "solução completa", "leva a sua criatividade a outro nível" e parentes);
  - as três alíneas presentes: (a) o que entra e o que sai, (b) onde encaixa,
    (c) qual é o limite — a (c) é detectada pela palavra "Limite:", que é
    obrigatória por convenção deste projeto;
  - descrição colada da meta tag da página (propaganda do próprio produto
    entrando por cópia);
  - `url_coletada` que não existe na fila — descrição órfã não entra em nada.

Uso:  uv run python atividade-2/validar_descricoes.py
"""

from __future__ import annotations

import json
import re
from pathlib import Path

RAIZ = Path(__file__).parent
DADOS = RAIZ / "dados"
DESCRICOES = RAIZ / "descricoes"

PROIBIDAS = [
    "revolucion", "poderos", "solução completa", "solucao completa",
    "outro nível", "outro nivel", "game.chang", "de ponta", "líder de mercado",
    "lider de mercado", "incrível", "incrivel", "impressionante", "inovador",
    "transform", "empodera", "descomplica", "sem esforço", "sem esforco",
    "tudo que você precisa", "tudo que voce precisa", "melhor ferramenta",
]


def frases(t: str) -> list[str]:
    return [f.strip() for f in re.split(r"(?<=[.!?])\s+", t.strip()) if f.strip()]


def main() -> int:
    fila = {}
    arq = DADOS / "para_descrever.jsonl"
    if arq.exists():
        for l in arq.read_text(encoding="utf-8").splitlines():
            if l.strip():
                d = json.loads(l)
                fila[d.get("url_coletada") or d["url"]] = d

    problemas: list[str] = []
    total = 0
    for f in sorted(DESCRICOES.glob("*.jsonl")):
        for n, linha in enumerate(f.read_text(encoding="utf-8").splitlines(), 1):
            if not linha.strip():
                continue
            onde = f"{f.name}:{n}"
            try:
                d = json.loads(linha)
            except json.JSONDecodeError as e:
                problemas.append(f"{onde} JSON inválido: {e}")
                continue
            total += 1
            u = d.get("url_coletada", "")
            desc = (d.get("descricao") or "").strip()
            if not u:
                problemas.append(f"{onde} sem url_coletada")
            elif fila and u not in fila:
                problemas.append(f"{onde} url_coletada não está na fila: {u}")
            if not desc:
                problemas.append(f"{onde} descrição vazia")
                continue
            baixo = desc.lower()
            # "de ponta a ponta" é termo técnico corrente (end-to-end) e não
            # tem nada de propaganda; neutralizado antes da checagem para não
            # disparar contra "de ponta".
            baixo_check = baixo.replace("de ponta a ponta", "")
            # "transformador"/"transformer" é o NOME de uma arquitetura de rede
            # neural, não adjetivo de propaganda. Neutralizado antes da checagem
            # para não disparar contra o radical "transform", pelo mesmo motivo
            # que "de ponta a ponta" já era neutralizado acima.
            for termo_tecnico in ("transformador", "transformer"):
                baixo_check = baixo_check.replace(termo_tecnico, "")
            for p in PROIBIDAS:
                if p in baixo_check:
                    problemas.append(f"{onde} vocabulário de propaganda: '{p}'")
            if "limite:" not in baixo:
                problemas.append(f"{onde} falta a alínea (c) — sem 'Limite:'")
            fs = frases(desc)
            if len(fs) < 3:
                problemas.append(f"{onde} só {len(fs)} frase(s); o formato pede três")
            if len(desc) < 140:
                problemas.append(f"{onde} curta demais ({len(desc)} caracteres)")
            # descrição copiada da meta tag do próprio produto
            orig = fila.get(u) or {}
            meta = (orig.get("meta_pagina") or "").strip()
            if meta and len(meta) > 40 and meta[:60].lower() in baixo:
                problemas.append(f"{onde} primeira frase copiada da meta tag (propaganda do produto)")

    print(f"{total} descrições conferidas em {len(list(DESCRICOES.glob('*.jsonl')))} arquivo(s)")
    if problemas:
        print(f"\n{len(problemas)} problema(s):")
        for p in problemas[:60]:
            print("  -", p)
        if len(problemas) > 60:
            print(f"  ... e mais {len(problemas) - 60}")
        return 1
    print("nenhum problema encontrado.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
