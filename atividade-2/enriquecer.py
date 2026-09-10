"""Fase C da Entrega 2 — abrir cada candidato e procurar a prova de que ele
é instalável, sob que licença, e o que ele realmente faz.

Diferença central em relação à Entrega 1: lá o enriquecimento buscava a PÁGINA
da ferramenta, porque a pergunta era "isso abre?". Aqui a pergunta é outra —
"isso instala, com que licença e expondo o quê?" — e a resposta não está em
página de marketing, está na API do registro e no README do repositório.

Três coisas são apuradas, e as duas primeiras são critério eliminatório do aluno:

  E1  INSTALÁVEL. Para item de registro, estar publicado já é a prova. Para
      repositório, procura-se comando de instalação de verdade no README
      (`pip install`, `npm i`, `cargo add`, `go get`, `gem install`, …). Sem
      isso, é código que existe mas não se importa — e reprova.

  E3  LICENÇA. Vem do campo declarado de cada registro (`license`, `licenses`,
      `licenseUrl`) ou da API do GitHub. Ausência declarada é ausência de
      licença, não falta de informação.

  TEXTO. README e descrição do autor, que alimentam a repontuação e, depois, a
  escrita das três frases exigidas — sem isso a descrição vira propaganda copiada.

Uso:
    uv run python atividade-2/enriquecer.py --trabalhadores 12
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
from urllib.parse import quote, urlsplit

import httpx

RAIZ = Path(__file__).parent
DADOS = RAIZ / "dados"
CACHE = DADOS / "cache_detalhe"
UA = ("cin0055-coletor-atividade2/1.0 "
      "(+trabalho academico CIn/UFPE; contato: victoramarante00@gmail.com)")

INTERVALO_PADRAO = 1.0
INTERVALO_POR_HOST = {
    "raw.githubusercontent.com": 0.35,   # CDN, tolerante
    "api.github.com": 2.2,               # 30 req/min autenticado
    "registry.npmjs.org": 0.4,
    "crates.io": 1.1,                    # a política do crates.io pede ~1 req/s
    "huggingface.co": 1.2,
    "rubygems.org": 0.8,
    "packagist.org": 0.8,
}
# Status transitório NÃO entra no cache. Cachear 429 envenena o item para
# sempre e faz a rodada seguinte "confirmar" um erro que já tinha passado —
# aconteceu na Entrega 1 e custou 50 itens marcados como mortos por engano.
CACHEAVEL = {200, 301, 302, 400, 401, 403, 404, 410, 451}

_trava = threading.Lock()
_ultimo: dict[str, float] = {}

# Comando de instalação de verdade — a prova do critério E1.
INSTALACAO = re.compile(
    r"(pip3?\s+install\s+[\w\.\-\[\]]+)"
    r"|(uv\s+(?:pip\s+)?add\s+[\w\.\-]+)"
    r"|(poetry\s+add\s+[\w\.\-]+)"
    r"|(conda\s+install\s+[\w\.\-]+)"
    r"|(npm\s+(?:i|install)\s+(?!-g\s*$)[@\w\./\-]+)"
    r"|(yarn\s+add\s+[@\w\./\-]+)"
    r"|(pnpm\s+(?:i|add)\s+[@\w\./\-]+)"
    r"|(cargo\s+(?:add|install)\s+[\w\-]+)"
    r"|(go\s+get\s+[\w\./\-]+)"
    r"|(gem\s+install\s+[\w\-]+)"
    r"|(composer\s+require\s+[\w\-/]+)"
    r"|(dotnet\s+add\s+package\s+[\w\.\-]+)"
    r"|(mix\s+deps)|(<dependency>)|(implementation\s+['\"][\w\.\-:]+['\"])",
    re.I)


def _esperar(host: str) -> None:
    intervalo = INTERVALO_POR_HOST.get(host, INTERVALO_PADRAO)
    while True:
        with _trava:
            agora = time.monotonic()
            if agora - _ultimo.get(host, 0.0) >= intervalo:
                _ultimo[host] = agora
                return
            falta = intervalo - (agora - _ultimo.get(host, 0.0))
        time.sleep(min(falta, 0.4))


def _cache(url: str) -> Path:
    return CACHE / (hashlib.sha256(url.encode()).hexdigest() + ".json")


def buscar(cli: httpx.Client, url: str, cab: dict | None = None) -> dict:
    arq = _cache(url)
    if arq.exists():
        d = json.loads(arq.read_text())
        d["do_cache"] = True
        return d
    _esperar(urlsplit(url).netloc)
    t0 = time.monotonic()
    try:
        r = cli.get(url, headers=cab)
        d = {"status": r.status_code, "texto": r.text[:300_000], "erro": "",
             "ms": int((time.monotonic() - t0) * 1000)}
    except Exception as e:
        d = {"status": -1, "texto": "", "erro": f"{type(e).__name__}: {e}",
             "ms": int((time.monotonic() - t0) * 1000)}
    if d["status"] in CACHEAVEL:
        arq.write_text(json.dumps(d))
    d["do_cache"] = False
    return d


def _json(d: dict):
    try:
        return json.loads(d["texto"]) if d["status"] == 200 else None
    except Exception:
        return None


def _repo_de(url: str) -> str | None:
    """Extrai `dono/repo` de uma URL do GitHub."""
    m = re.search(r"github\.com/([\w.\-]+)/([\w.\-]+)", url or "")
    if not m:
        return None
    return f"{m.group(1)}/{m.group(2)}".removesuffix(".git")


def readme_do_github(cli: httpx.Client, repo: str) -> str:
    for ramo in ("HEAD", "master", "main"):
        for arq in ("README.md", "readme.md", "README.rst", "README"):
            d = buscar(cli, f"https://raw.githubusercontent.com/{repo}/{ramo}/{arq}")
            if d["status"] == 200 and len(d["texto"]) > 120:
                return d["texto"]
        break  # HEAD já resolve o ramo padrão; os outros são só rede desperdiçada
    return ""


def tratar(cli: httpx.Client, c: dict, token: str) -> dict:
    url = c.get("url") or ""
    s = c.get("sinais") or {}
    info = {"licenca": s.get("licenca") or None, "instalacao": s.get("instalacao") or "",
            "downloads": None, "readme": "", "descricao": c.get("descricao_fonte") or "",
            "repositorio": s.get("repositorio") or "", "versao": s.get("versao") or "",
            "status": None, "fonte_detalhe": ""}

    # --- registros de pacote: a API de detalhe traz licença e README --------
    if "npmjs.com/package/" in url:
        nome = url.split("/package/", 1)[1].strip("/")
        d = buscar(cli, f"https://registry.npmjs.org/{quote(nome, safe='@/')}")
        info["status"] = d["status"]; info["fonte_detalhe"] = "registry.npmjs.org"
        j = _json(d) or {}
        ultima = (j.get("versions") or {}).get((j.get("dist-tags") or {}).get("latest"), {})
        info["licenca"] = ultima.get("license") or j.get("license") or None
        info["readme"] = (j.get("readme") or "")[:20000]
        info["descricao"] = j.get("description") or info["descricao"]
        rep = j.get("repository")
        info["repositorio"] = (rep or {}).get("url", "") if isinstance(rep, dict) else (rep or "")
        info["versao"] = (j.get("dist-tags") or {}).get("latest", "")
    elif "crates.io/crates/" in url:
        nome = url.split("/crates/", 1)[1].strip("/")
        d = buscar(cli, f"https://crates.io/api/v1/crates/{nome}")
        info["status"] = d["status"]; info["fonte_detalhe"] = "crates.io/api"
        j = _json(d) or {}
        cr = j.get("crate") or {}
        versoes = j.get("versions") or []
        info["licenca"] = (versoes[0].get("license") if versoes else None)
        info["descricao"] = cr.get("description") or info["descricao"]
        info["downloads"] = cr.get("downloads")
        info["repositorio"] = cr.get("repository") or ""
        info["versao"] = cr.get("max_version") or ""
    elif "rubygems.org/gems/" in url:
        nome = url.split("/gems/", 1)[1].strip("/")
        d = buscar(cli, f"https://rubygems.org/api/v1/gems/{nome}.json")
        info["status"] = d["status"]; info["fonte_detalhe"] = "rubygems.org/api"
        j = _json(d) or {}
        lic = j.get("licenses")
        info["licenca"] = ", ".join(lic) if isinstance(lic, list) and lic else None
        info["descricao"] = j.get("info") or info["descricao"]
        info["downloads"] = j.get("downloads")
        info["repositorio"] = j.get("source_code_uri") or j.get("homepage_uri") or ""
        info["versao"] = j.get("version") or ""
    elif "packagist.org/packages/" in url:
        nome = url.split("/packages/", 1)[1].strip("/").removesuffix(".json")
        d = buscar(cli, f"https://packagist.org/packages/{nome}.json")
        info["status"] = d["status"]; info["fonte_detalhe"] = "packagist.org/api"
        j = (_json(d) or {}).get("package") or {}
        versoes = list((j.get("versions") or {}).values())
        if versoes:
            lic = versoes[0].get("license")
            info["licenca"] = ", ".join(lic) if isinstance(lic, list) and lic else None
            info["versao"] = versoes[0].get("version", "")
        info["descricao"] = j.get("description") or info["descricao"]
        info["downloads"] = (j.get("downloads") or {}).get("total")
        info["repositorio"] = j.get("repository") or ""
    elif "pypi.org/project/" in url:
        nome = url.split("/project/", 1)[1].strip("/").split("/")[0]
        d = buscar(cli, f"https://pypi.org/pypi/{nome}/json")
        info["status"] = d["status"]; info["fonte_detalhe"] = "pypi.org/pypi/json"
        j = (_json(d) or {}).get("info") or {}
        # A licença do PyPI vem em dois lugares e o campo `license` costuma vir
        # vazio nos pacotes modernos; o classificador é a fonte mais confiável.
        lic = (j.get("license") or "").strip()
        if not lic or len(lic) > 60:
            for cl in (j.get("classifiers") or []):
                if cl.startswith("License :: "):
                    lic = cl.rsplit(" :: ", 1)[-1]
                    break
        info["licenca"] = lic or None
        info["descricao"] = j.get("summary") or info["descricao"]
        info["readme"] = (j.get("description") or "")[:20000]
        info["versao"] = j.get("version") or ""
        urls = j.get("project_urls") or {}
        info["repositorio"] = (urls.get("Source") or urls.get("Repository")
                               or urls.get("Homepage") or j.get("home_page") or "")
    elif "nuget.org/packages/" in url:
        nome = url.split("/packages/", 1)[1].strip("/").split("/")[0]
        baixo = nome.lower()
        # O nuspec é o único lugar com a expressão de licença; a busca só devolve
        # uma URL de licença, que não diz qual licença é.
        idx = buscar(cli, f"https://api.nuget.org/v3-flatcontainer/{baixo}/index.json")
        versao = ""
        j = _json(idx) or {}
        if j.get("versions"):
            versao = j["versions"][-1]
        info["status"] = idx["status"]; info["fonte_detalhe"] = "api.nuget.org"
        info["versao"] = versao
        if versao:
            d = buscar(cli, f"https://api.nuget.org/v3-flatcontainer/{baixo}/{versao}/{baixo}.nuspec")
            if d["status"] == 200:
                m = re.search(r"<license[^>]*>([^<]+)</license>", d["texto"])
                if not m:
                    m = re.search(r"<licenseUrl>([^<]+)</licenseUrl>", d["texto"])
                info["licenca"] = (m.group(1).strip() if m else None)
                md = re.search(r"<description>([^<]*)</description>", d["texto"], re.S)
                if md:
                    info["descricao"] = md.group(1).strip() or info["descricao"]
                mr = re.search(r"<repository[^>]*url=\"([^\"]+)\"", d["texto"])
                if mr:
                    info["repositorio"] = mr.group(1)
    elif "huggingface.co/" in url and "/spaces/" not in url:
        ident = url.split("huggingface.co/", 1)[1].strip("/")
        d = buscar(cli, f"https://huggingface.co/api/models/{ident}")
        info["status"] = d["status"]; info["fonte_detalhe"] = "huggingface.co/api"
        j = _json(d) or {}
        cartao = j.get("cardData") or {}
        info["licenca"] = cartao.get("license")
        info["downloads"] = j.get("downloads")
        info["descricao"] = cartao.get("short_description") or info["descricao"]

    # --- repositório: README é a prova de instalabilidade -------------------
    repo = _repo_de(url) or _repo_de(info["repositorio"])
    if repo:
        if info["status"] is None:
            info["status"] = 200
            info["fonte_detalhe"] = "raw.githubusercontent.com"
        info["readme"] = info["readme"] or readme_do_github(cli, repo)
        if not info["licenca"] and token:
            d = buscar(cli, f"https://api.github.com/repos/{repo}",
                       {"Authorization": f"Bearer {token}",
                        "Accept": "application/vnd.github+json"})
            j = _json(d) or {}
            info["licenca"] = (j.get("license") or {}).get("spdx_id")
            info["descricao"] = info["descricao"] or (j.get("description") or "")
            info["status"] = info["status"] or d["status"]

    texto = f"{info['descricao']}\n{info['readme']}"
    achado = INSTALACAO.search(texto)
    de_registro = any(r in url for r in (
        "npmjs.com/package/", "crates.io/crates/", "rubygems.org/gems/",
        "packagist.org/packages/", "nuget.org/packages/", "pypi.org/project/"))
    c["detalhe"] = {
        "licenca": info["licenca"],
        "licenca_declarada": bool(info["licenca"]) and info["licenca"] not in ("NOASSERTION",),
        "instalavel": bool(de_registro or achado),
        "prova_instalacao": ("publicado em registro de pacote" if de_registro
                             else (achado.group(0).strip()[:80] if achado else "")),
        "downloads": info["downloads"] or (c.get("sinais") or {}).get("downloads"),
        "versao": info["versao"],
        "repositorio": info["repositorio"],
        "status": info["status"],
        "fonte_detalhe": info["fonte_detalhe"],
        "tem_readme": len(info["readme"]) > 200,
    }
    c["texto"] = {"descricao": info["descricao"][:1200],
                  "readme": re.sub(r"\s+", " ", info["readme"])[:3000]}
    return c


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--trabalhadores", type=int, default=12)
    p.add_argument("--limite", type=int, default=0)
    args = p.parse_args()

    CACHE.mkdir(parents=True, exist_ok=True)
    token = ""
    for env in (RAIZ / ".env", RAIZ.parent / "atividade-1" / ".env"):
        if env.exists():
            for linha in env.read_text().splitlines():
                if linha.startswith("GITHUB_TOKEN="):
                    token = linha.split("=", 1)[1].strip()

    itens = [json.loads(l) for l in
             (DADOS / "preselecao.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
    if args.limite:
        itens = itens[: args.limite]

    saida = DADOS / "enriquecidos.jsonl"
    feitos = set()
    if saida.exists():
        for l in saida.read_text(encoding="utf-8").splitlines():
            if l.strip():
                feitos.add(json.loads(l)["url"])
    pendentes = [c for c in itens if c["url"] not in feitos]
    print(f"{len(itens)} pré-selecionados | {len(feitos)} já enriquecidos | "
          f"{len(pendentes)} a fazer")

    cli = httpx.Client(headers={"User-Agent": UA},
                       timeout=httpx.Timeout(25.0, connect=10.0),
                       follow_redirects=True, verify=False)
    trava = threading.Lock()
    n = {"feito": 0, "instalavel": 0, "com_licenca": 0}
    with saida.open("a", encoding="utf-8") as f, \
            ThreadPoolExecutor(max_workers=args.trabalhadores) as ex:
        futuros = {ex.submit(tratar, cli, c, token): c for c in pendentes}
        for fut in as_completed(futuros):
            try:
                c = fut.result()
            except Exception as e:
                c = futuros[fut]
                c["detalhe"] = {"licenca": None, "licenca_declarada": False,
                                "instalavel": False, "prova_instalacao": "",
                                "status": -1, "erro": f"{type(e).__name__}: {e}",
                                "tem_readme": False, "downloads": None}
                c["texto"] = {"descricao": c.get("descricao_fonte", ""), "readme": ""}
            with trava:
                f.write(json.dumps(c, ensure_ascii=False) + "\n")
                f.flush()
                n["feito"] += 1
                n["instalavel"] += bool(c["detalhe"].get("instalavel"))
                n["com_licenca"] += bool(c["detalhe"].get("licenca_declarada"))
                if n["feito"] % 100 == 0:
                    print(f"  {n['feito']}/{len(pendentes)}  instaláveis {n['instalavel']} | "
                          f"com licença {n['com_licenca']}", flush=True)
    cli.close()
    print(f"\nverificados {n['feito']} | instaláveis {n['instalavel']} | "
          f"com licença declarada {n['com_licenca']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
