"""Ajusta o log bruto ao limite de 45 MB do sistema de entrega, num arquivo só.

O QUE ESTE SCRIPT NÃO FAZ
-------------------------
Não remove linha, não deduplica, não ordena, não conserta URL, não apaga erro,
não junta execução repetida. Toda a "sujeira" que o enunciado pede para manter
continua lá: as repetições, os `utm_source`, os `www.` e `docs.` do mesmo
domínio, as requisições 429, as linhas de lixo. O número de linhas e o conjunto
de endereços distintos — que é o que o sistema conta — ficam idênticos.

O QUE ELE FAZ
-------------
Uma regra só, aplicada uniformemente: todo VALOR DE TEXTO com mais de N
caracteres é cortado em N e recebe a marca `…[truncado: X caracteres]`, de modo
que a perda fica visível dentro do próprio registro em vez de silenciosa.

Por que isso resolve: 62 dos 89 MB estavam em `huggingface:paper`, a 6,7 KB por
linha, porque a API do Hugging Face devolve o mesmo resumo três vezes
(`paper.summary`, `summary` e `highlightedSummary`) — e `siblings`, a listagem
de arquivos do repositório de cada Space, somava outros 10 MB sem dizer nada
sobre a ferramenta. O corte por tamanho atinge exatamente esses blocos e quase
não toca no resto do log.

O arquivo original, sem corte nenhum, continua em `dados/log_bruto.jsonl`.

Uso:  uv run python atividade-1/compactar_log.py
"""

from __future__ import annotations

import json
from pathlib import Path

RAIZ = Path(__file__).parent
ORIGEM = RAIZ / "dados" / "log_bruto.jsonl"
DESTINO = RAIZ / "entrega" / "log-bruto.jsonl"
# 45 MB pode significar 45 milhões de bytes ou 45 MiB, dependendo de quem
# escreveu o validador. 43 milhões cabe nas duas leituras sem depender de sorte.
LIMITE_BYTES = 43_000_000


def cortar(valor, n: int):
    """Aplica o corte recursivamente dentro do registro.

    Duas regras, ambas com marca visível do que foi cortado:
      - texto acima de `n` caracteres é truncado;
      - lista com mais de `itens_max` elementos é truncada.

    A segunda regra é necessária porque boa parte do peso não estava em texto
    longo e sim em estrutura aninhada: `siblings` (a listagem de arquivos do
    repositório de cada Space) e `authors` (a lista de autores de cada paper)
    somavam dezenas de MB em milhares de pequenos dicionários. Cortar só string
    não chegava nem perto do limite — medido: 46,2 MB mesmo truncando todo
    texto em 40 caracteres.
    """
    itens_max = max(3, n // 40)
    if isinstance(valor, str):
        if len(valor) > n:
            return valor[:n] + f"…(+{len(valor) - n} car)"
        return valor
    if isinstance(valor, dict):
        return {k: cortar(v, n) for k, v in valor.items()}
    if isinstance(valor, list):
        if len(valor) > itens_max:
            return [cortar(v, n) for v in valor[:itens_max]] + \
                   [f"…(+{len(valor) - itens_max} itens)"]
        return [cortar(v, n) for v in valor]
    return valor


def tentar(linhas: list[str], n: int) -> tuple[bytes, int, int]:
    saida = []
    cortados = 0
    for l in linhas:
        d = json.loads(l)
        antes = len(l)
        d = cortar(d, n)
        s = json.dumps(d, ensure_ascii=False) + "\n"
        if len(s) < antes:
            cortados += 1
        saida.append(s)
    return "".join(saida).encode("utf-8"), len(saida), cortados


def main() -> int:
    linhas = [l for l in ORIGEM.read_text(encoding="utf-8").splitlines() if l.strip()]
    original = ORIGEM.stat().st_size
    print(f"origem: {len(linhas)} linhas, {original/1024/1024:.1f} MB")

    # Procura o MAIOR limite de caracteres que ainda cabe no arquivo. Buscar o
    # maior, e não um valor fixo escolhido no chute, é o que garante que o corte
    # seja o mínimo necessário para caber.
    melhor = None
    baixo, alto = 40, 4000
    while baixo <= alto:
        meio = (baixo + alto) // 2
        dados, n_linhas, cortados = tentar(linhas, meio)
        cabe = len(dados) <= LIMITE_BYTES
        print(f"  corte em {meio:>5} caracteres -> {len(dados)/1024/1024:>5.1f} MB "
              f"{'cabe' if cabe else 'não cabe'}")
        if cabe:
            melhor = (meio, dados, n_linhas, cortados)
            baixo = meio + 1
        else:
            alto = meio - 1

    if melhor is None:
        print("não foi possível caber no limite nem com o corte mais agressivo")
        return 1

    n, dados, n_linhas, cortados = melhor
    DESTINO.parent.mkdir(parents=True, exist_ok=True)
    DESTINO.write_bytes(dados)

    # Conferência: mesma contagem de linhas e mesmo conjunto de endereços.
    urls_antes, urls_depois = set(), set()
    for l in linhas:
        d = json.loads(l)
        for k in ("url", "loc", "href", "link"):
            if isinstance(d.get(k), str):
                urls_antes.add(d[k])
            b = d.get("bruto") or {}
            if isinstance(b.get(k), str):
                urls_antes.add(b[k])
    for l in DESTINO.read_text(encoding="utf-8").splitlines():
        d = json.loads(l)
        for k in ("url", "loc", "href", "link"):
            if isinstance(d.get(k), str):
                urls_depois.add(d[k])
            b = d.get("bruto") or {}
            if isinstance(b.get(k), str):
                urls_depois.add(b[k])

    print()
    print(f"escrito: {DESTINO}")
    print(f"  regra aplicada     : texto acima de {n} caracteres é cortado e marcado")
    print(f"  linhas             : {len(linhas)} -> {n_linhas}  "
          f"({'idêntico' if len(linhas) == n_linhas else 'DIFERENTE'})")
    print(f"  endereços distintos: {len(urls_antes)} -> {len(urls_depois)}  "
          f"({'idêntico' if urls_antes == urls_depois else 'DIFERENTE'})")
    print(f"  linhas com algum corte: {cortados} ({100*cortados/n_linhas:.1f}%)")
    print(f"  tamanho            : {original/1024/1024:.1f} MB -> "
          f"{len(dados)/1024/1024:.1f} MB")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
