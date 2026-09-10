"""Executor da varredura (Fase A).

Uso:
    uv run python atividade-1/varrer.py                     # todas as fontes
    uv run python atividade-1/varrer.py --fontes hn,github  # só algumas
    uv run python atividade-1/varrer.py --paginas 10        # mais fundo
    uv run python atividade-1/varrer.py --limpar-estado     # recomeça do zero

Retomada: se cair no meio, basta rodar de novo. O estado guarda que
(fonte, consulta, página) já terminaram e o cache guarda as respostas HTTP,
então a segunda execução não repete requisição nem incomoda servidor nenhum.
"""

from __future__ import annotations

import argparse
import importlib
import os
import time
from pathlib import Path

RAIZ = Path(__file__).parent
import sys

sys.path.insert(0, str(RAIZ))

from coletor.deposito import Deposito, Estado  # noqa: E402
from coletor.fontes import Contexto  # noqa: E402
from coletor.rede import Cliente, LogBruto  # noqa: E402

# Intervalo mínimo entre requisições ao mesmo host, POR FONTE.
#
# arXiv: os 3 s dos Termos de Uso NÃO bastaram na prática — com 3,5 s o
# servidor devolveu 429 vinte e quatro vezes seguidas e a fonte rendeu zero.
# O limite real é mais apertado que o documentado (ou a cota é por IP e já
# estava gasta pela sondagem). Subido para 12 s, que é o valor em que parou de
# recusar. Documentação diz uma coisa, servidor diz outra; vale o servidor.
#
# toolify pediria 5 s de crawl-delay, mas está bloqueado e não é varrido.
INTERVALOS = {
    "hn": 0.5, "arxiv": 12.0, "huggingface": 0.7, "github": 2.2,
    "reddit": 2.0, "diretorios": 1.0, "itchio": 2.0, "producthunt": 1.0,
}
ORDEM = ["hn", "huggingface", "github", "diretorios", "itchio", "arxiv", "reddit", "producthunt"]


def carregar_env(caminho: Path) -> None:
    if not caminho.exists():
        return
    for linha in caminho.read_text().splitlines():
        if "=" in linha and not linha.strip().startswith("#"):
            k, v = linha.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip())


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--fontes", default=",".join(ORDEM),
                   help="lista separada por vírgula; padrão = todas")
    p.add_argument("--paginas", type=int, default=5, help="páginas por consulta")
    p.add_argument("--limpar-estado", action="store_true")
    args = p.parse_args()

    carregar_env(RAIZ / ".env")
    dados = RAIZ / "dados"
    estado_arq = dados / "estado.json"
    if args.limpar_estado and estado_arq.exists():
        estado_arq.unlink()

    log = LogBruto(dados / "log_bruto.jsonl")
    deposito = Deposito(dados / "candidatos.jsonl")
    estado = Estado(estado_arq)
    ja_tinha = len(deposito.vistos)

    log.evento("inicio_varredura", {"fontes": args.fontes, "paginas": args.paginas,
                                    "candidatos_antes": ja_tinha})
    print(f"começando com {ja_tinha} candidatos já no depósito\n")

    escolhidas = [f.strip() for f in args.fontes.split(",") if f.strip()]
    for nome in [f for f in ORDEM if f in escolhidas]:
        modulo = importlib.import_module(f"coletor.fontes.{nome}")
        cliente = Cliente(dir_cache=dados / "cache", log=log,
                          intervalo=INTERVALOS.get(nome, 1.0))
        ctx = Contexto(cliente=cliente, deposito=deposito, estado=estado, log=log,
                       limite_paginas=args.paginas,
                       token_github=os.environ.get("GITHUB_TOKEN", ""))
        antes, t0 = deposito.novos, time.monotonic()
        print(f"--- {nome} (intervalo {INTERVALOS.get(nome, 1.0)}s) ...", flush=True)
        try:
            modulo.varrer(ctx)
        except KeyboardInterrupt:
            log.evento("interrompido", {"fonte": nome})
            print("\ninterrompido — o estado ficou salvo, rode de novo para continuar")
            break
        except Exception as e:  # uma fonte quebrada não derruba a varredura
            log.evento("fonte_excecao", {"fonte": nome, "erro": f"{type(e).__name__}: {e}"})
            print(f"    ERRO em {nome}: {type(e).__name__}: {e}")
        finally:
            cliente.fechar()
        print(f"    +{deposito.novos - antes} novos  "
              f"({time.monotonic() - t0:.0f}s, total {len(deposito.vistos)})")

    log.evento("fim_varredura", {"novos": deposito.novos, "repetidos": deposito.repetidos,
                                 "descartados": deposito.descartados,
                                 "total": len(deposito.vistos)})
    print(f"\nnovos: {deposito.novos} | repetidos (dedup): {deposito.repetidos} | "
          f"URLs inválidas: {deposito.descartados} | total único: {len(deposito.vistos)}")
    deposito.fechar()
    log.fechar()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
