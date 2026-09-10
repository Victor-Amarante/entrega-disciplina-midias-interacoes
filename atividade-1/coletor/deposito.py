"""Depósito dos candidatos coletados e estado de retomada.

Separa três coisas que costumam ser confundidas:
  - o LOG BRUTO (rede.py)  : tudo que aconteceu, inclusive erro e repetição;
  - os CANDIDATOS (aqui)   : um registro por item colhido, ainda SEM peneira;
  - o estado de retomada    : que (fonte, consulta, página) já terminaram.

A peneira acontece depois, em cima dos candidatos, com os critérios do aluno.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path

from .normalizacao import normalizar


@dataclass
class Candidato:
    nome: str
    url: str                  # canônica
    url_original: str
    fonte: str                # ex.: "github", "producthunt"
    consulta: str             # a query exata que trouxe este item
    chave_dedup: str
    dominio: str
    descricao_fonte: str = "" # texto que a PRÓPRIA fonte deu (nunca inventado)
    sinais: dict = field(default_factory=dict)  # estrelas, votos, data, tags...


class Deposito:
    """Grava candidatos em JSONL, deduplicando em memória pela chave.

    Mantém a PRIMEIRA ocorrência e anota nas demais que a ferramenta apareceu
    em mais de uma fonte — esse contador é um sinal útil na peneira (aparecer
    em 4 fontes diferentes diz algo; aparecer em 1 também).
    """

    def __init__(self, caminho: Path) -> None:
        self.caminho = caminho
        self.caminho.parent.mkdir(parents=True, exist_ok=True)
        self.vistos: dict[str, dict] = {}
        if caminho.exists():
            for linha in caminho.read_text(encoding="utf-8").splitlines():
                if linha.strip():
                    reg = json.loads(linha)
                    self.vistos[reg["chave_dedup"]] = reg
        self._f = caminho.open("a", encoding="utf-8")
        self.novos = 0
        self.repetidos = 0
        self.descartados = 0

    def adicionar(self, *, nome: str, url: str, fonte: str, consulta: str,
                  descricao_fonte: str = "", sinais: dict | None = None) -> bool:
        n = normalizar(url)
        if n is None:
            self.descartados += 1
            return False
        if n.chave_dedup in self.vistos:
            reg = self.vistos[n.chave_dedup]
            fontes = set(reg.get("fontes_extras", [])) | {fonte}
            reg["fontes_extras"] = sorted(fontes)
            self.repetidos += 1
            return False
        cand = Candidato(
            nome=(nome or "").strip() or n.dominio,
            url=n.canonica,
            url_original=url,
            fonte=fonte,
            consulta=consulta,
            chave_dedup=n.chave_dedup,
            dominio=n.dominio,
            descricao_fonte=(descricao_fonte or "").strip(),
            sinais=sinais or {},
        )
        reg = asdict(cand)
        self.vistos[n.chave_dedup] = reg
        self._f.write(json.dumps(reg, ensure_ascii=False) + "\n")
        self._f.flush()
        self.novos += 1
        return True

    def fechar(self) -> None:
        self._f.close()


class Estado:
    """Marca (fonte, consulta, página) já concluídos, para retomar de onde parou.

    O cache de HTTP já evita rebaixar o servidor, mas o estado evita até o
    trabalho de reprocessar — e deixa explícito no log onde a varredura parou.
    """

    def __init__(self, caminho: Path) -> None:
        self.caminho = caminho
        self.caminho.parent.mkdir(parents=True, exist_ok=True)
        self.feitos: set[str] = set()
        if caminho.exists():
            self.feitos = set(json.loads(caminho.read_text()).get("feitos", []))

    @staticmethod
    def _id(fonte: str, consulta: str, pagina: int | str) -> str:
        return f"{fonte}::{consulta}::{pagina}"

    def concluido(self, fonte: str, consulta: str, pagina: int | str) -> bool:
        return self._id(fonte, consulta, pagina) in self.feitos

    def marcar(self, fonte: str, consulta: str, pagina: int | str) -> None:
        self.feitos.add(self._id(fonte, consulta, pagina))
        self.caminho.write_text(json.dumps({"feitos": sorted(self.feitos)}, ensure_ascii=False))
