"""Salas em memória, com uma cópia em JSON por sala para sobreviver a um reinício.

Todas as rotas são `async` e rodam no mesmo event loop, então não há escrita
concorrente no estado: não precisa de lock.
"""

import logging
import secrets
import time
from pathlib import Path

from .dominio.modelos import ConfigSala, Pergunta, Sala

log = logging.getLogger(__name__)

# Sem letras que se confundem no telão (O/0, I/1, L).
LETRAS_CODIGO = "ABCDEFGHJKMNPQRSTUVWXYZ"

PERGUNTAS_DO_INSTITUTO = [
    ("generica", "Em poucas palavras, como foi o seu último dia de trabalho?"),
    ("atencao", "Para mostrar que você está lendo, responda esta pergunta só com a palavra \"macaxeira\"."),
]


def novo_id(prefixo: str) -> str:
    return f"{prefixo}-{secrets.token_hex(4)}"


class Armazem:
    def __init__(self, pasta: Path):
        self.pasta = pasta
        self.salas: dict[str, Sala] = {}

    def carregar(self) -> None:
        self.pasta.mkdir(parents=True, exist_ok=True)
        for arquivo in self.pasta.glob("*.json"):
            try:
                sala = Sala.model_validate_json(arquivo.read_text())
                self.salas[sala.codigo] = sala
            except Exception:
                log.exception("sala corrompida: %s", arquivo)

    def salvar(self, sala: Sala) -> None:
        destino = self.pasta / f"{sala.codigo}.json"
        temporario = destino.with_suffix(".tmp")
        temporario.write_text(sala.model_dump_json())
        temporario.replace(destino)

    def obter(self, codigo: str) -> Sala | None:
        return self.salas.get(codigo.upper())

    def criar(self, config: ConfigSala) -> Sala:
        codigo = self._codigo_livre()
        sala = Sala(
            codigo=codigo,
            host_token=secrets.token_urlsafe(16),
            criada_em=time.time(),
            config=config,
            perguntas=[
                Pergunta(id=novo_id("q"), texto=texto, tipo=tipo, selecionada=True, fixa=True)
                for tipo, texto in PERGUNTAS_DO_INSTITUTO
            ],
        )
        self.salas[codigo] = sala
        self.salvar(sala)
        return sala

    def _codigo_livre(self) -> str:
        while True:
            codigo = "".join(secrets.choice(LETRAS_CODIGO) for _ in range(4))
            if codigo not in self.salas:
                return codigo
