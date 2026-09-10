"""Listas "awesome" do GitHub: curadoria humana já feita.

Por que esta fonte existe: registro de pacote só mostra o que foi publicado, e
busca por palavra só mostra o que usa as palavras que EU escolhi. Lista awesome
é curadoria feita por gente que conhece o assunto, e é onde biblioteca de nicho
aparece — justamente a que escapa das outras duas vias.

Como funciona: acha as listas pela Search API (`awesome <tema> in:name,description`),
baixa o README cru de cada uma e extrai os links de markdown que apontam para
repositório ou para registro de pacote. O texto que acompanha o link na lista
vira a descrição do curador, que costuma ser melhor que a descrição do autor.
"""

from __future__ import annotations

import re
from urllib.parse import urlencode

from . import Contexto

NOME = "awesome"
METODO = (
    "Duas etapas. Primeiro a Search API do GitHub acha as listas com 8 consultas do tipo "
    "`awesome <tema> in:name,description`. Depois o README cru de cada lista é baixado de "
    "`raw.githubusercontent.com/<repo>/HEAD/README.md` (com queda para `master` e `main`) e "
    "os links de markdown `[nome](url)` são extraídos por expressão regular, ficando só os "
    "que apontam para repositório ou registro de pacote. O texto que segue o link na linha "
    "da lista é guardado como descrição — é a palavra do curador, normalmente mais útil que "
    "a autodescrição do autor da biblioteca."
)
VIES = (
    "É curadoria, com todos os vícios de curadoria: reflete o gosto e a data de quem manteve "
    "a lista. Lista awesome envelhece mal e quase nunca remove link morto, então traz projeto "
    "abandonado com naturalidade. Há forte efeito de bola de neve — quem já está na lista "
    "ganha estrela e continua na lista — e listas se copiam entre si, o que faz o mesmo "
    "punhado de bibliotecas famosas aparecer em todas. Cobre bem o que é popular em inglês e "
    "mal o que é recente, regional ou de nicho sem porta-voz."
)

CONSULTAS = [
    "awesome agent based modeling in:name,description",
    "awesome multi agent in:name,description",
    "awesome simulation in:name,description",
    "awesome llm agents in:name,description",
    "awesome reinforcement learning environments in:name,description",
    "awesome game ai in:name,description",
    "awesome complex systems in:name,description",
    "awesome llm observability in:name,description",
]

# [texto](url) seguido, opcionalmente, do travessão e da descrição do curador.
_LINHA = re.compile(r"\[([^\]]{1,120})\]\((https?://[^\s\)]+)\)\s*[-–—:]?\s*([^\n]{0,300})")

ALVOS = ("github.com/", "gitlab.com/", "pypi.org/project/", "npmjs.com/package/",
         "crates.io/crates/", "nuget.org/packages/", "rubygems.org/gems/",
         "packagist.org/packages/", "pkg.go.dev/", "hex.pm/packages/",
         "huggingface.co/", "pub.dev/packages/")
IGNORAR = ("github.com/sindresorhus/awesome", "/blob/", "/issues", "/pulls",
           "/stargazers", "/network/members", "shields.io", "badge", "/actions",
           "github.com/topics/", "/graphs/", "/releases/tag/")


def _achar_listas(ctx: Contexto, cab: dict) -> list[str]:
    listas: list[str] = []
    for consulta in CONSULTAS:
        if ctx.estado.concluido(NOME, consulta, 0):
            continue
        url = ("https://api.github.com/search/repositories?"
               + urlencode({"q": consulta, "per_page": 50, "sort": "stars"}))
        r = ctx.cliente.get(url, headers=cab)
        if r.status != 200:
            ctx.log.evento("fonte_falhou", {"fonte": NOME, "consulta": consulta,
                                            "status": r.status})
            continue
        for repo in r.json().get("items", []):
            nome = repo.get("full_name")
            if nome and nome not in listas:
                listas.append(nome)
        ctx.estado.marcar(NOME, consulta, 0)
    return listas


def varrer(ctx: Contexto) -> None:
    if not ctx.token_github:
        ctx.log.evento("fonte_pulada", {"fonte": NOME, "motivo": "sem GITHUB_TOKEN"})
        return
    cab = {"Authorization": f"Bearer {ctx.token_github}",
           "Accept": "application/vnd.github+json",
           "X-GitHub-Api-Version": "2022-11-28"}

    listas = _achar_listas(ctx, cab)
    ctx.log.evento("awesome_listas", {"quantas": len(listas)})

    for repo in listas:
        if ctx.estado.concluido(NOME, f"readme:{repo}", 0):
            continue
        texto = ""
        for ramo in ("HEAD", "master", "main"):
            r = ctx.cliente.get(
                f"https://raw.githubusercontent.com/{repo}/{ramo}/README.md")
            if r.status == 200 and len(r.texto) > 200:
                texto = r.texto
                break
        if not texto:
            ctx.log.evento("sem_itens", {"fonte": NOME, "consulta": repo,
                                         "aviso": "README não encontrado em HEAD/master/main"})
            ctx.estado.marcar(NOME, f"readme:{repo}", 0)
            continue

        achados = 0
        for titulo, alvo, cauda in _LINHA.findall(texto):
            if not any(a in alvo for a in ALVOS):
                continue
            if any(x in alvo for x in IGNORAR):
                continue
            ctx.log.item(NOME, repo, {"lista": repo, "titulo": titulo,
                                      "url": alvo, "descricao_curador": cauda.strip()[:300]})
            ctx.deposito.adicionar(
                nome=titulo.strip(), url=alvo, fonte=NOME, consulta=repo,
                descricao_fonte=cauda.strip()[:300],
                sinais={"faceta": "curadoria", "lista": repo,
                        "descricao_do_curador": True},
            )
            achados += 1
        ctx.log.evento("awesome_lista_lida", {"lista": repo, "links_uteis": achados})
        ctx.estado.marcar(NOME, f"readme:{repo}", 0)
