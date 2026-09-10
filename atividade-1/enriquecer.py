"""Fase C — abrir cada candidato pré-selecionado e olhar o que tem lá.

Faz três coisas que nenhuma API de busca faz por você:

  1. VERIFICA que o link existe. Requisição de verdade, status registrado,
     redirecionamento seguido e URL final anotada. É a resposta concreta à
     pergunta "como você sabe que o link existe?": não é confiança, é 200.

  2. EXTRAI o texto real da página — <title>, meta description, og:description
     e o começo do corpo. É essa matéria-prima que permite escrever descrição
     em três frases sem abrir 500 abas na mão, e é ela que alimenta o
     julgamento em lote dos critérios E2/E3, que regex nenhum decide.

  3. RESOLVE ficha de diretório. `futuretools.io/tools/x` é a página do
     diretório SOBRE a ferramenta, não a ferramenta. Aqui a gente segue o link
     de saída e guarda o endereço verdadeiro — senão a lista final aponta 300
     vezes para o mesmo diretório.

Concorrência com educação: 12 threads no total, mas no máximo uma requisição
por host a cada `INTERVALO_HOST` segundos. Domínio popular não leva rajada.

Uso:
    uv run python atividade-1/enriquecer.py
    uv run python atividade-1/enriquecer.py --trabalhadores 8 --limite 300
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from urllib.parse import urljoin, urlsplit

import httpx
from selectolax.parser import HTMLParser

RAIZ = Path(__file__).parent
DADOS = RAIZ / "dados"
CACHE = DADOS / "cache_paginas"

UA = ("cin0055-coletor-atividade1/1.0 "
      "(+trabalho academico CIn/UFPE; contato: victoramarante00@gmail.com)")
INTERVALO_HOST = 1.5

# Hosts que exigem mais folga que o padrão. Medido, não chutado: com 1,5 s o
# huggingface.co devolveu 50 respostas 429 ("We had to rate limit your IP")
# no primeiro enriquecimento.
# Nota sobre o huggingface.co: os 429 vinham da PÁGINA web, não da API. Depois
# que os Spaces passaram a ser verificados por `api/spaces/<id>`, 4 s virou
# exagero — a varredura já tinha feito 168 chamadas de API a 0,7 s sem um único
# 429. 1,2 s é folgado para a API e corta o enriquecimento de ~40 para ~12 min.
INTERVALO_POR_HOST = {
    "huggingface.co": 1.2,
    "www.aixploria.com": 2.0,
    "aixploria.com": 2.0,
}

# Status cujo corpo pode ir para o cache. 429, 5xx e falha de rede são
# TRANSITÓRIOS: cachear um 429 envenena o item para sempre e faz a rodada
# seguinte "confirmar" um erro que já tinha passado. Foi o que aconteceu na
# primeira execução — 50 Spaces ficaram gravados como mortos sendo que só
# tinham esbarrado no limite de taxa.
CACHEAVEL = {200, 301, 302, 400, 401, 403, 404, 410, 451}

_trava = threading.Lock()
_ultimo: dict[str, float] = {}

# Ficha de diretório -> como achar o link real da ferramenta.
SELETORES_SAIDA = {
    "futuretools.io": ["a.link-block-2", "a[href*='/go/']", "a.tool-link"],
    "aixploria.com": ["a.visit-website", "a.aix-link", "a[rel~=nofollow][target=_blank]"],
}


def _esperar(host: str) -> None:
    intervalo = INTERVALO_POR_HOST.get(host, INTERVALO_HOST)
    while True:
        with _trava:
            agora = time.monotonic()
            ultimo = _ultimo.get(host, 0.0)
            if agora - ultimo >= intervalo:
                _ultimo[host] = agora
                return
            falta = intervalo - (agora - ultimo)
        time.sleep(min(falta, 0.5))


def _cache(url: str) -> Path:
    return CACHE / (hashlib.sha256(url.encode()).hexdigest() + ".json")


def buscar(cliente: httpx.Client, url: str) -> dict:
    arq = _cache(url)
    if arq.exists():
        d = json.loads(arq.read_text())
        d["do_cache"] = True
        return d
    _esperar(urlsplit(url).netloc)
    t0 = time.monotonic()
    try:
        r = cliente.get(url)
        d = {"status": r.status_code, "url_final": str(r.url),
             "html": r.text[:400_000], "erro": "",
             "ms": int((time.monotonic() - t0) * 1000)}
    except Exception as e:
        d = {"status": -1, "url_final": url, "html": "",
             "erro": f"{type(e).__name__}: {e}",
             "ms": int((time.monotonic() - t0) * 1000)}
    if d["status"] in CACHEAVEL:
        arq.write_text(json.dumps(d))
    d["do_cache"] = False
    return d


def buscar_space_hf(cliente: httpx.Client, url: str) -> dict:
    """Space do Hugging Face: consulta a API em vez de raspar a página.

    A página web do HF limita taxa com agressividade (429 mesmo a 1,5 s por
    requisição), enquanto `api/spaces/<id>` responde em ~270 ms sem reclamar —
    e ainda devolve `runtime.stage`, que diz se o Space está RUNNING, SLEEPING
    ou com erro de build. Isso é sinal de vida melhor do que um GET na página,
    que devolve 200 mesmo para Space quebrado.
    """
    ident = url.split("/spaces/", 1)[1].strip("/") if "/spaces/" in url else ""
    if not ident:
        return buscar(cliente, url)
    api = f"https://huggingface.co/api/spaces/{ident}"
    arq = _cache(api)
    if arq.exists():
        d = json.loads(arq.read_text())
        d["do_cache"] = True
        return d
    _esperar("huggingface.co")
    t0 = time.monotonic()
    try:
        r = cliente.get(api)
        meta = r.json() if r.status_code == 200 else {}
    except Exception as e:
        return {"status": -1, "url_final": url, "html": "", "erro": f"{type(e).__name__}: {e}",
                "ms": int((time.monotonic() - t0) * 1000), "do_cache": False}
    cartao = meta.get("cardData") or {}
    estagio = (meta.get("runtime") or {}).get("stage", "")
    # Monta um "corpo" textual a partir dos metadados, para o julgamento ter o
    # que ler. Nada aqui é inventado: são campos declarados pelo autor do Space.
    corpo = " · ".join(str(x) for x in [
        cartao.get("title", ""), cartao.get("short_description", ""),
        f"SDK {meta.get('sdk') or cartao.get('sdk') or '?'}",
        f"estado {estagio or '?'}", f"{meta.get('likes', 0)} likes",
        " ".join(cartao.get("tags") or []),
        " ".join(meta.get("models") or [])[:200],
    ] if x)
    d = {"status": r.status_code, "url_final": url, "html": "", "erro": "",
         "ms": int((time.monotonic() - t0) * 1000),
         "hf": {"estagio": estagio, "sdk": meta.get("sdk") or cartao.get("sdk"),
                "likes": meta.get("likes"), "gated": meta.get("gated"),
                "disabled": meta.get("disabled"), "atualizado": meta.get("lastModified"),
                "modelos": meta.get("models"), "titulo": cartao.get("title", "")},
         "extraido": {"titulo": cartao.get("title", "") or ident,
                      "meta": cartao.get("short_description", "") or "",
                      "corpo": corpo}}
    if d["status"] in CACHEAVEL:
        arq.write_text(json.dumps(d))
    d["do_cache"] = False
    return d


def extrair(html: str, url_base: str) -> dict:
    if not html:
        return {"titulo": "", "meta": "", "corpo": ""}
    a = HTMLParser(html)
    titulo = ""
    if a.css_first("title"):
        titulo = " ".join(a.css_first("title").text().split())
    meta = ""
    for sel, attr in (("meta[name=description]", "content"),
                      ("meta[property='og:description']", "content"),
                      ("meta[name='twitter:description']", "content")):
        n = a.css_first(sel)
        if n and n.attributes.get(attr):
            meta = " ".join(n.attributes[attr].split())
            break
    for lixo in a.css("script, style, nav, footer, noscript, svg"):
        lixo.decompose()
    corpo = " ".join((a.body.text() if a.body else "").split())[:2500]
    return {"titulo": titulo, "meta": meta, "corpo": corpo}


def link_de_saida(html: str, url_base: str) -> str:
    """Numa ficha de diretório, acha o link para o site real da ferramenta."""
    host = urlsplit(url_base).netloc.replace("www.", "")
    seletores = None
    for chave, sels in SELETORES_SAIDA.items():
        if chave in host:
            seletores = sels
            break
    if not seletores or not html:
        return ""
    a = HTMLParser(html)
    for sel in seletores:
        n = a.css_first(sel)
        if n and n.attributes.get("href"):
            return urljoin(url_base, n.attributes["href"])
    # Recurso final: primeiro link externo que não seja rede social.
    social = ("twitter.com", "x.com", "facebook.com", "linkedin.com", "instagram.com",
              "youtube.com", "discord", "reddit.com", "producthunt.com")
    for n in a.css("a[href^='http']"):
        h = n.attributes.get("href", "")
        d = urlsplit(h).netloc.replace("www.", "")
        if d and d != host and not any(s in d for s in social):
            return h
    return ""


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--trabalhadores", type=int, default=12)
    p.add_argument("--limite", type=int, default=0, help="0 = todos")
    args = p.parse_args()

    CACHE.mkdir(parents=True, exist_ok=True)
    entrada = DADOS / "preselecao.jsonl"
    itens = [json.loads(l) for l in entrada.read_text(encoding="utf-8").splitlines() if l.strip()]
    if args.limite:
        itens = itens[: args.limite]

    saida = DADOS / "enriquecidos.jsonl"
    ja_feitos = set()
    if saida.exists():
        for l in saida.read_text(encoding="utf-8").splitlines():
            if l.strip():
                ja_feitos.add(json.loads(l)["url"])
    pendentes = [c for c in itens if c["url"] not in ja_feitos]
    print(f"{len(itens)} pré-selecionados | {len(ja_feitos)} já enriquecidos | "
          f"{len(pendentes)} a fazer")

    cliente = httpx.Client(headers={"User-Agent": UA}, timeout=httpx.Timeout(25.0, connect=10.0),
                           follow_redirects=True, verify=False)
    trava_escrita = threading.Lock()
    contagem = {"ok": 0, "erro": 0, "feito": 0}

    def tratar(c: dict) -> dict:
        eh_space = "huggingface.co/spaces/" in c["url"]
        r = buscar_space_hf(cliente, c["url"]) if eh_space else buscar(cliente, c["url"])
        info = r.get("extraido") or extrair(r.get("html", ""), r["url_final"])
        if eh_space:
            # Vivo para um Space = a API confirma que ele existe e não está
            # desativado. SLEEPING não é morto: o Space acorda quando alguém
            # abre — mas isso é um limite real e vai na descrição.
            hf = r.get("hf") or {}
            vivo = r["status"] == 200 and not hf.get("disabled")
            c["hf"] = hf
        else:
            vivo = r["status"] == 200 and len(r.get("html", "")) > 500
        c["verificacao"] = {
            "status": r["status"], "url_final": r["url_final"], "erro": r["erro"],
            "ms": r["ms"], "do_cache": r["do_cache"], "vivo": vivo,
        }
        c["pagina"] = info
        saida_real = link_de_saida(r.get("html", ""), r["url_final"])
        if saida_real:
            c["url_ferramenta"] = saida_real
        return c

    with saida.open("a", encoding="utf-8") as f, \
            ThreadPoolExecutor(max_workers=args.trabalhadores) as executor:
        futuros = {executor.submit(tratar, c): c for c in pendentes}
        for fut in as_completed(futuros):
            try:
                c = fut.result()
            except Exception as e:
                c = futuros[fut]
                c["verificacao"] = {"status": -1, "erro": f"{type(e).__name__}: {e}",
                                    "vivo": False, "url_final": c["url"]}
                c["pagina"] = {"titulo": "", "meta": "", "corpo": ""}
            with trava_escrita:
                f.write(json.dumps(c, ensure_ascii=False) + "\n")
                f.flush()
                contagem["feito"] += 1
                contagem["ok" if c["verificacao"].get("vivo") else "erro"] += 1
                if contagem["feito"] % 100 == 0:
                    print(f"  {contagem['feito']}/{len(pendentes)}  "
                          f"vivos {contagem['ok']} | mortos {contagem['erro']}", flush=True)

    cliente.close()
    print(f"\nverificados {contagem['feito']} | link vivo (200 + conteúdo): {contagem['ok']} | "
          f"morto/erro: {contagem['erro']}")
    print(f"saída: {saida}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
