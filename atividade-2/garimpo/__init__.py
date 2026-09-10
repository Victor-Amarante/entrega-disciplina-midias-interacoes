"""Núcleo do coletor da Entrega 2 — reaproveitado da Entrega 1.

NADA do que foi testado na Entrega 1 é reescrito aqui. Normalização de URL,
deduplicação, cache em disco, limite de taxa por host, robots.txt, retomada e
log bruto são importados de `atividade-1/coletor/`, que já rodou 38 mil linhas
de log e teve quatro bugs corrigidos no caminho. Copiar aquilo seria criar uma
segunda versão livre para divergir da primeira.

O que muda na Entrega 2 fica declarado aqui, em dois pontos:

1. A regra de deduplicação ganha os REGISTROS DE PACOTE. Na Entrega 1,
   `pypi.org` e `npmjs.com` eram domínio de publicação e caíam fora inteiros —
   lá eles não eram ferramenta. Aqui cada pacote É uma ferramenta distinta, e
   sem esta extensão os milhares de pacotes de um registro colapsariam numa
   chave só. É exatamente o bug que custou 7.774 candidatos na Entrega 1,
   agora previsto em vez de descoberto.

2. O User-Agent passa a identificar a Entrega 2, para que quem ler o log do
   servidor saiba qual varredura passou.

A extensão é feita sobre o dicionário importado, sem editar o arquivo da
Entrega 1 — aquela entrega está fechada e seus números precisam continuar
reproduzíveis.
"""

from __future__ import annotations

import sys
from dataclasses import dataclass
from pathlib import Path

_ATIVIDADE_1 = Path(__file__).resolve().parent.parent.parent / "atividade-1"
if str(_ATIVIDADE_1) not in sys.path:
    sys.path.insert(0, str(_ATIVIDADE_1))

from coletor import normalizacao as _norm       # noqa: E402
from coletor import rede as _rede               # noqa: E402
from coletor.deposito import Deposito, Estado   # noqa: E402,F401
from coletor.normalizacao import normalizar     # noqa: E402,F401
from coletor.rede import Cliente, LogBruto      # noqa: E402,F401

# --- 1. registros de pacote: cada pacote é uma ferramenta -------------------
REGISTROS = {
    "pypi.org": 2,          # /project/<nome>
    # profundidade 3 por causa do pacote com escopo: sem isso
    # @langchain/core e @langchain/openai viram a mesma chave. Com 3, o
    # pacote sem escopo (/package/foo) continua correto, porque só existem
    # dois segmentos para consumir.
    "npmjs.com": 3,         # /package/<nome> ou /package/@escopo/<nome>
    "crates.io": 2,         # /crates/<nome>
    "nuget.org": 2,         # /packages/<nome>
    "packagist.org": 3,     # /packages/<vendor>/<nome>
    "rubygems.org": 2,      # /gems/<nome>
    "pkg.go.dev": 3,        # /<host>/<org>/<modulo>
    "pub.dev": 2,           # /packages/<nome>
    "cocoapods.org": 2,
    "mvnrepository.com": 3, # /artifact/<grupo>/<artefato>
    "hex.pm": 2,            # /packages/<nome>
    "ecosyste.ms": 3,
    "openalex.org": 1,
    "doi.org": 3,
}
_norm.HOSTS_MULTI_PROJETO.update(REGISTROS)

# --- 2. identificação do coletor -------------------------------------------
_rede.USER_AGENT = (
    "cin0055-coletor-atividade2/1.0 "
    "(+trabalho academico CIn/UFPE; contato: victoramarante00@gmail.com)"
)
USER_AGENT = _rede.USER_AGENT


@dataclass
class Contexto:
    """Mesmo contrato de adaptador da Entrega 1: cada fonte expõe `varrer(ctx)`,
    mais as constantes `METODO` e `VIES`."""

    cliente: Cliente
    deposito: Deposito
    estado: Estado
    log: LogBruto
    limite_paginas: int = 5
    token_github: str = ""
