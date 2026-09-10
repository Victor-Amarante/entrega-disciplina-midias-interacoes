"""Adaptadores de fonte.

Contrato: cada módulo expõe `varrer(ctx)` e a constante `VIES` (texto do que a
fonte sistematicamente NÃO mostra — vai direto para o item 3 da entrega).
"""

from __future__ import annotations

from dataclasses import dataclass

from ..deposito import Deposito, Estado
from ..rede import Cliente, LogBruto


@dataclass
class Contexto:
    cliente: Cliente
    deposito: Deposito
    estado: Estado
    log: LogBruto
    limite_paginas: int = 5
    token_github: str = ""
