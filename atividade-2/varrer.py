"""Executor da varredura da Entrega 2.

Uso:
    uv run python atividade-2/varrer.py                        # todas as fontes
    uv run python atividade-2/varrer.py --fontes registros     # só uma
    uv run python atividade-2/varrer.py --paginas 3
    uv run python atividade-2/varrer.py --limpar-estado

NUNCA rode duas instâncias ao mesmo tempo. Na Entrega 1 isso foi feito por
descuido — arXiv em segundo plano enquanto o Hugging Face rodava em primeiro —,
as duas com o mesmo arquivo de log aberto para escrita, e o log voltou a conter
apenas as execuções mais antigas. Perdeu-se de vez o registro dos erros daquela
rodada. Como tudo fica em cache, rodar em série custa segundos.
"""

from __future__ import annotations

import argparse
import importlib
import os
import sys
import time
from pathlib import Path

RAIZ = Path(__file__).parent
sys.path.insert(0, str(RAIZ))

from garimpo import Cliente, Contexto, Deposito, Estado, LogBruto  # noqa: E402

# Intervalo mínimo entre requisições ao MESMO host, por fonte.
# crates.io pede cerca de 1 req/s na sua política de uso; GitHub permite 30
# requisições por minuto na busca autenticada; herdados não toca a rede.
INTERVALOS = {
    "herdados": 0.0, "hn": 0.5, "huggingface": 0.7, "registros": 1.1,
    "awesome": 1.0, "github": 2.2, "pypi": 0.8,
}
ORDEM = ["herdados", "registros", "pypi", "github", "awesome", "huggingface", "hn"]


def carregar_env() -> None:
    """O token do GitHub já existe na Entrega 1; não se duplica segredo."""
    for caminho in (RAIZ / ".env", RAIZ.parent / "atividade-1" / ".env"):
        if caminho.exists():
            for linha in caminho.read_text().splitlines():
                if "=" in linha and not linha.strip().startswith("#"):
                    k, v = linha.split("=", 1)
                    os.environ.setdefault(k.strip(), v.strip())


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--fontes", default=",".join(ORDEM))
    p.add_argument("--paginas", type=int, default=5)
    p.add_argument("--limpar-estado", action="store_true")
    args = p.parse_args()

    carregar_env()
    dados = RAIZ / "dados"
    estado_arq = dados / "estado.json"
    if args.limpar_estado and estado_arq.exists():
        estado_arq.unlink()

    log = LogBruto(dados / "log_bruto.jsonl")
    deposito = Deposito(dados / "candidatos.jsonl")
    estado = Estado(estado_arq)
    ja_tinha = len(deposito.vistos)

    log.evento("inicio_varredura", {"entrega": 2, "fontes": args.fontes,
                                    "paginas": args.paginas, "candidatos_antes": ja_tinha})
    print(f"começando com {ja_tinha} candidatos já no depósito\n")

    escolhidas = [f.strip() for f in args.fontes.split(",") if f.strip()]
    for nome in [f for f in ORDEM if f in escolhidas]:
        modulo = importlib.import_module(f"garimpo.fontes.{nome}")
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
        except Exception as e:
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
