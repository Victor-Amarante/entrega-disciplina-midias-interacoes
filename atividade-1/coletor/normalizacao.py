"""Normalização de URL e regra de deduplicação.

A regra está escrita aqui, em um lugar só, porque ela precisa ser DEFENDIDA na
entrega: "por que essas 500 e não 700?" costuma ter como resposta "porque
dedupliquei assim". Se a regra mudar, o número de ferramentas muda.
"""

from __future__ import annotations

from dataclasses import dataclass
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

import tldextract

# Extrator offline: não consulta a lista de sufixos públicos pela rede a cada
# execução (evita variação silenciosa de resultado entre rodadas).
_extrator = tldextract.TLDExtract(suffix_list_urls=())

# Parâmetros de rastreamento: não identificam recurso, só campanha. Removidos
# sempre, porque a mesma ferramenta aparece com utm diferente em cada fonte.
PARAMS_DESCARTAVEIS = {
    "utm_source", "utm_medium", "utm_campaign", "utm_term", "utm_content",
    "utm_id", "utm_name", "utm_reader", "utm_social", "utm_brand",
    "ref", "ref_src", "refsrc", "referrer", "referer", "source", "src",
    "via", "fbclid", "gclid", "gbraid", "wbraid", "msclkid", "yclid",
    "igshid", "mc_cid", "mc_eid", "_hsenc", "_hsmi", "hsCtaTracking",
    "spm", "at_medium", "at_campaign", "s", "sk", "share", "shared",
}

# Hosts em que UM domínio hospeda MUITAS ferramentas distintas. Nesses, o
# domínio sozinho não serve como identidade: github.com inteiro viraria uma
# ferramenta só. A chave passa a incluir os primeiros segmentos do caminho.
HOSTS_MULTI_PROJETO: dict[str, int] = {
    "github.com": 2,          # github.com/owner/repo
    "gitlab.com": 2,
    "huggingface.co": 3,      # /spaces/owner/nome  e  /owner/modelo
    "replit.com": 2,
    "itch.io": 1,             # subdomínio já separa; caminho /nome-do-jogo
    "notion.site": 1,
    "gumroad.com": 1,
    "producthunt.com": 2,     # /posts/slug
    "app.gumroad.com": 1,
    "steampowered.com": 2,    # /app/12345
    "figma.com": 2,           # /community/plugin/123
    "chromewebstore.google.com": 2,
    "apps.apple.com": 3,
    "play.google.com": 1,
    "arxiv.org": 2,           # /abs/2501.01234
    "colab.research.google.com": 2,
    "observablehq.com": 2,
    "glitch.com": 2,
    # Diretórios: um domínio, milhares de FICHAS de ferramenta. Sem isto, as
    # ~3000 URLs do futuretools colapsam todas na chave "futuretools.io" e a
    # varredura comercial inteira vira 1 item. (Bug real, pego no primeiro log:
    # a fonte `diretorios` rendeu +2 candidatos em vez de milhares.)
    "futuretools.io": 2,      # /tools/slug
    "aixploria.com": 2,       # /en/slug
    "theresanaiforthat.com": 1,
    "toolify.ai": 2,
    "vercel.app": 0,          # subdomínio É a identidade
    "netlify.app": 0,
    "streamlit.app": 0,
    "hf.space": 0,
    "pages.dev": 0,
    "github.io": 0,
}

# Subdomínios que são só idioma/região/versão: descartados na comparação.
SUBDOMINIOS_IRRELEVANTES = {"www", "m", "en", "pt", "pt-br", "br", "us", "web"}


@dataclass(frozen=True)
class UrlNormalizada:
    original: str
    canonica: str      # URL limpa, é ela que vai para o documento das 500
    chave_dedup: str   # identidade da ferramenta; duas iguais = mesma ferramenta
    dominio: str       # domínio registrável (para relatório de viés por fonte)
    host: str


def _host_limpo(host: str) -> str:
    host = host.lower().strip(".")
    if host.startswith("www."):
        host = host[4:]
    return host


def normalizar(url: str) -> UrlNormalizada | None:
    """Devolve a forma canônica e a chave de deduplicação, ou None se a URL
    não for aproveitável (sem host, esquema não-http, etc.)."""
    url = (url or "").strip()
    if not url:
        return None
    if url.startswith("//"):
        url = "https:" + url
    if "://" not in url:
        url = "https://" + url

    partes = urlsplit(url)
    if partes.scheme not in ("http", "https"):
        return None
    host = _host_limpo(partes.netloc.split("@")[-1])
    if not host or "." not in host:
        return None
    # remove porta padrão
    if host.endswith(":80") or host.endswith(":443"):
        host = host.rsplit(":", 1)[0]

    # --- caminho -------------------------------------------------------
    caminho = partes.path or "/"
    if len(caminho) > 1 and caminho.endswith("/"):
        caminho = caminho.rstrip("/")
    # index.html e afins não mudam o recurso
    for sufixo in ("/index.html", "/index.htm", "/index.php"):
        if caminho.endswith(sufixo):
            caminho = caminho[: -len(sufixo)] or "/"

    # --- query ---------------------------------------------------------
    pares = [
        (k, v) for k, v in parse_qsl(partes.query, keep_blank_values=False)
        if k.lower() not in PARAMS_DESCARTAVEIS and not k.lower().startswith("utm_")
    ]
    pares.sort()
    query = urlencode(pares)

    canonica = urlunsplit(("https", host, caminho, query, ""))  # fragmento sempre fora

    # --- chave de deduplicação ----------------------------------------
    ext = _extrator(host)
    dominio = ".".join(p for p in (ext.domain, ext.suffix) if p)
    subdominio = ext.subdomain.lower()

    profundidade = None
    for padrao, n in HOSTS_MULTI_PROJETO.items():
        if host == padrao or host.endswith("." + padrao) or dominio == padrao:
            profundidade = n
            break

    if profundidade is None:
        # Caso comum: o produto É o domínio. midjourney.com/showcase e
        # midjourney.com/pricing são a mesma ferramenta.
        chave = dominio
    elif profundidade == 0:
        # O subdomínio é a identidade (foo.streamlit.app != bar.streamlit.app).
        chave = host
    else:
        segmentos = [s for s in caminho.split("/") if s][:profundidade]
        base = host if subdominio and subdominio not in SUBDOMINIOS_IRRELEVANTES else dominio
        chave = base + ("/" + "/".join(segmentos) if segmentos else "")

    return UrlNormalizada(
        original=url,
        canonica=canonica,
        chave_dedup=chave.lower(),
        dominio=dominio,
        host=host,
    )
