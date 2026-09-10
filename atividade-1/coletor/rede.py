"""Camada de rede do coletor: cache em disco, limite de taxa por host,
retomada, retentativa com backoff e respeito a robots.txt.

Tudo que sai pela rede passa por aqui, e tudo que passa por aqui é registrado
no log bruto. Isso é o que permite responder "quantas requisições você fez, a
quem, e o que voltou" sem estimativa.
"""

from __future__ import annotations

import hashlib
import json
import time
import urllib.robotparser
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit

import httpx

# Identificação honesta do coletor. Um administrador que ler o log do servidor
# precisa saber quem passou e como reclamar.
USER_AGENT = (
    "cin0055-coletor-atividade1/1.0 "
    "(+trabalho academico CIn/UFPE; contato: victoramarante00@gmail.com)"
)

INTERVALO_PADRAO = 1.0  # segundos entre requisições ao MESMO host
TENTATIVAS = 4

# Exceções ao robots.txt — cada uma escrita à mão, com justificativa, porque
# ignorar robots em silêncio é exatamente o que esta atividade manda não fazer.
#
# export.arxiv.org/robots.txt responde "User-agent: * / Disallow: /", e o
# coletor obedeceu: 42 requisições bloqueadas no primeiro log, arXiv rendeu
# zero. Só que o arXiv PUBLICA nesse mesmo host uma API oficial
# (https://info.arxiv.org/help/api/) cujos Termos de Uso autorizam acesso
# programático, pedindo no máximo 1 requisição a cada 3 segundos. O robots ali
# mira crawler de mirror do site inteiro, não cliente da API documentada.
#
# Esta é uma decisão de JULGAMENTO, e ela é do aluno, não minha. Está isolada
# aqui para poder ser removida numa linha: apagar a entrada faz o coletor voltar
# a pular o arXiv.
EXCECOES_ROBOTS = {
    "export.arxiv.org": "API oficial documentada, Termos de Uso permitem; respeitado o mínimo de 3 s",
}


@dataclass
class Resposta:
    url: str
    status: int
    texto: str
    do_cache: bool
    duracao_ms: int

    def json(self) -> Any:
        return json.loads(self.texto)


@dataclass
class Cliente:
    """Cliente HTTP com cache em disco.

    O cache é o que torna a varredura *retomável*: se o script cair na fonte 6
    de 9, reexecutar não refaz as 5 primeiras — elas voltam do disco em
    milissegundos e sem tocar o servidor de ninguém.
    """

    dir_cache: Path
    log: "LogBruto"
    intervalo: float = INTERVALO_PADRAO
    respeitar_robots: bool = True
    _ultimo_acesso: dict[str, float] = field(default_factory=dict)
    _robots: dict[str, urllib.robotparser.RobotFileParser | None] = field(default_factory=dict)
    _cliente: httpx.Client | None = None

    def __post_init__(self) -> None:
        self.dir_cache.mkdir(parents=True, exist_ok=True)
        self._cliente = httpx.Client(
            headers={"User-Agent": USER_AGENT, "Accept-Language": "en,pt-BR;q=0.8"},
            timeout=httpx.Timeout(30.0, connect=15.0),
            follow_redirects=True,
        )

    # ------------------------------------------------------------------ cache
    def _caminho_cache(self, url: str, headers: dict | None) -> Path:
        crua = url + "|" + json.dumps(headers or {}, sort_keys=True)
        return self.dir_cache / (hashlib.sha256(crua.encode()).hexdigest() + ".json")

    # ------------------------------------------------------------- boas maneiras
    def _esperar(self, host: str) -> None:
        agora = time.monotonic()
        ultimo = self._ultimo_acesso.get(host)
        if ultimo is not None:
            falta = self.intervalo - (agora - ultimo)
            if falta > 0:
                time.sleep(falta)
        self._ultimo_acesso[host] = time.monotonic()

    def permitido(self, url: str) -> bool:
        if not self.respeitar_robots:
            return True
        partes = urlsplit(url)
        host = partes.netloc
        if host in EXCECOES_ROBOTS:
            self.log.evento("robots_excecao", {"host": host, "url": url,
                                               "justificativa": EXCECOES_ROBOTS[host]})
            return True
        if host not in self._robots:
            rp = urllib.robotparser.RobotFileParser()
            alvo = f"{partes.scheme}://{host}/robots.txt"
            try:
                r = self._cliente.get(alvo)  # type: ignore[union-attr]
                rp.parse(r.text.splitlines() if r.status_code == 200 else [])
            except Exception:
                rp.parse([])  # sem robots legível: não bloqueia, mas fica no log
            self._robots[host] = rp
            self.log.evento("robots", {"host": host, "url": alvo})
        rp = self._robots[host]
        return rp is None or rp.can_fetch(USER_AGENT, url)

    # ------------------------------------------------------------------ get
    def get(self, url: str, headers: dict | None = None, forcar: bool = False) -> Resposta:
        alvo = self._caminho_cache(url, headers)
        if alvo.exists() and not forcar:
            dados = json.loads(alvo.read_text())
            self.log.requisicao(url, dados["status"], 0, cache=True, bytes_=len(dados["texto"]))
            return Resposta(url, dados["status"], dados["texto"], True, 0)

        if not self.permitido(url):
            self.log.evento("robots_bloqueou", {"url": url})
            return Resposta(url, 999, "", False, 0)

        host = urlsplit(url).netloc
        ultimo_erro = ""
        for tentativa in range(1, TENTATIVAS + 1):
            self._esperar(host)
            inicio = time.monotonic()
            try:
                r = self._cliente.get(url, headers=headers)  # type: ignore[union-attr]
            except Exception as e:  # rede caiu, DNS, timeout
                ultimo_erro = f"{type(e).__name__}: {e}"
                self.log.requisicao(url, -1, int((time.monotonic() - inicio) * 1000),
                                    erro=ultimo_erro, tentativa=tentativa)
                time.sleep(min(2 ** tentativa, 30))
                continue

            ms = int((time.monotonic() - inicio) * 1000)

            # 429/503: a fonte está pedindo para desacelerar. Obedecemos ao
            # Retry-After quando ele vem; senão, backoff exponencial.
            if r.status_code in (429, 503):
                espera = float(r.headers.get("Retry-After") or min(2 ** tentativa, 60))
                self.log.requisicao(url, r.status_code, ms, tentativa=tentativa,
                                    erro=f"aguardando {espera}s")
                time.sleep(espera)
                continue
            if 500 <= r.status_code < 600:
                self.log.requisicao(url, r.status_code, ms, tentativa=tentativa)
                time.sleep(min(2 ** tentativa, 30))
                continue

            self.log.requisicao(url, r.status_code, ms, bytes_=len(r.text), tentativa=tentativa)
            if r.status_code == 200:
                alvo.write_text(json.dumps({"status": r.status_code, "texto": r.text}))
            return Resposta(url, r.status_code, r.text, False, ms)

        return Resposta(url, -1, "", False, 0)

    def fechar(self) -> None:
        if self._cliente:
            self._cliente.close()


@dataclass
class LogBruto:
    """Log completo e bruto da varredura (item 2 da entrega).

    Uma linha JSON por evento. Nada é resumido aqui — resumo se faz depois, a
    partir deste arquivo.
    """

    caminho: Path

    def __post_init__(self) -> None:
        self.caminho.parent.mkdir(parents=True, exist_ok=True)
        self._f = self.caminho.open("a", encoding="utf-8")

    def _escrever(self, registro: dict) -> None:
        registro["ts"] = time.strftime("%Y-%m-%dT%H:%M:%S%z")
        self._f.write(json.dumps(registro, ensure_ascii=False) + "\n")
        self._f.flush()

    def requisicao(self, url: str, status: int, ms: int, *, cache: bool = False,
                   bytes_: int = 0, erro: str = "", tentativa: int = 1) -> None:
        self._escrever({"tipo": "requisicao", "url": url, "status": status, "ms": ms,
                        "cache": cache, "bytes": bytes_, "erro": erro,
                        "tentativa": tentativa})

    def evento(self, nome: str, dados: dict) -> None:
        self._escrever({"tipo": nome, **dados})

    def item(self, fonte: str, consulta: str, bruto: dict) -> None:
        """Registra o item exatamente como a fonte devolveu, antes de qualquer
        limpeza. É o que permite refazer a normalização sem varrer de novo."""
        self._escrever({"tipo": "item", "fonte": fonte, "consulta": consulta, "bruto": bruto})

    def fechar(self) -> None:
        self._f.close()
