"""PyPI pelo SITEMAP — a única via que o robots.txt do PyPI libera.

Por que não pela busca: `pypi.org/search/` responde 200 mas devolve um desafio
JavaScript ("JavaScript is disabled in your browser"), ou seja, proteção
anti-bot. Contornar seria burlar bloqueio de servidor, e esta coleta não faz
isso — mesma decisão tomada na Entrega 1 com theresanaiforthat e toolify.

Por que pelo sitemap: o próprio `robots.txt` do PyPI publica
`Sitemap: https://pypi.org/sitemap.xml` e só proíbe `/simple/` e `/packages/`.
Percorrer o sitemap é fazer exatamente o que o site pede que se faça.

O problema do sitemap é o oposto do da busca: ele traz TUDO — 257 arquivos com
cerca de 7.900 URLs cada, algo perto de 2 milhões de projetos — e não tem
descrição nenhuma, só o endereço. Filtrar por substring foi medido e dá 1,4%
com muito lixo ("sim" casa dentro de "simple", "agent" dentro de "agentic-crm").
Por isso o filtro é por TOKEN do slug: o nome é quebrado em `-`, `_` e `.`, e
só passa quem tem um token forte do vocabulário. Nome de pacote é escolhido
para ser lido por gente, então o token diz bastante — mas continua sendo um
palpite pelo nome, e a confirmação real só vem no enriquecimento, que consulta
`pypi.org/pypi/<nome>/json` e lê descrição, licença e classificadores.

Isso corrige o maior viés conhecido desta varredura: sem PyPI, a lista pende
para JavaScript e Rust, enquanto Python é onde a simulação científica mora.
"""

from __future__ import annotations

import re

from . import Contexto

NOME = "pypi"
METODO = (
    "Percorre o índice de sitemaps publicado no `robots.txt` do PyPI: 257 arquivos com cerca "
    "de 7.900 URLs de projeto cada. A busca do site não foi usada porque responde com desafio "
    "JavaScript, e contornar proteção anti-bot está fora do que esta coleta faz. Como o "
    "sitemap traz só o endereço, o filtro é por TOKEN do slug — o nome é quebrado em `-`, `_` "
    "e `.` e precisa conter um token forte do vocabulário (agent, abm, simul, swarm, mesa, "
    "netlogo, pettingzoo, marl, npc, boids…). Filtrar por substring foi medido antes e dá "
    "1,4% com muito falso positivo. A confirmação de descrição e licença acontece depois, no "
    "enriquecimento, em `pypi.org/pypi/<nome>/json`."
)
VIES = (
    "O sitemap não tem descrição, categoria nem popularidade: a seleção aqui é feita pelo NOME "
    "do pacote e mais nada. Isso favorece quem batizou o projeto de forma descritiva e é cego "
    "para a biblioteca bem nomeada de outro jeito — uma simulação de agentes chamada 'Orion' "
    "não aparece por nenhum caminho. Também entra muito homônimo: 'agent' é palavra comum em "
    "monitoramento, automação comercial e antivírus, domínios que nada têm a ver com este "
    "recorte. E, por vir do índice completo, não há ordenação por qualidade nem por uso: "
    "pacote abandonado com nome bom passa, e pacote ativo com nome ruim não."
)

INDICE = "https://pypi.org/sitemap.xml"
_LOC = re.compile(r"<loc>\s*(.*?)\s*</loc>", re.S)

# Tokens exatos: o slug é quebrado e cada pedaço é comparado com este conjunto.
TOKENS_FORTES = {
    "agent", "agents", "agentic", "multiagent", "multi-agent", "abm", "mas",
    "simulation", "simulations", "simulator", "simulate", "sim", "sims",
    "swarm", "swarms", "crowd", "colony", "flock", "flocking", "boids",
    "netlogo", "mesa", "pettingzoo", "gymnasium", "gym", "marl", "rl",
    "society", "societies", "social", "emergent", "emergence", "automata",
    "cellular", "npc", "npcs", "behaviortree", "behavior-tree", "goap",
    "worldmodel", "sandbox", "orchestrator", "orchestration",
}
# Prefixos: pegam família inteira sem listar cada variante.
PREFIXOS_FORTES = ("agent", "multiagent", "simul", "swarm", "netlogo", "pettingzoo",
                   "abm", "marl", "crowdsim", "socialsim", "gymnas")

SEPARADOR = re.compile(r"[-_.]+")


def interessa(url: str) -> bool:
    slug = url.rstrip("/").rsplit("/", 1)[-1].lower()
    tokens = [t for t in SEPARADOR.split(slug) if t]
    if any(t in TOKENS_FORTES for t in tokens):
        return True
    return any(t.startswith(PREFIXOS_FORTES) for t in tokens)


def varrer(ctx: Contexto) -> None:
    r = ctx.cliente.get(INDICE)
    if r.status != 200:
        ctx.log.evento("fonte_falhou", {"fonte": NOME, "consulta": INDICE,
                                        "status": r.status})
        return
    subs = _LOC.findall(r.texto)
    ctx.log.evento("pypi_indice", {"sub_sitemaps": len(subs)})

    vistos = achados = 0
    for sub in subs:
        if ctx.estado.concluido(NOME, sub, 0):
            continue
        rs = ctx.cliente.get(sub)
        if rs.status != 200:
            ctx.log.evento("fonte_falhou", {"fonte": NOME, "consulta": sub,
                                            "status": rs.status})
            continue
        for loc in _LOC.findall(rs.texto):
            vistos += 1
            if not interessa(loc):
                continue
            nome = loc.rstrip("/").rsplit("/", 1)[-1]
            ctx.log.item(NOME, sub, {"loc": loc, "slug": nome})
            ctx.deposito.adicionar(
                nome=nome, url=loc, fonte=NOME, consulta=sub,
                descricao_fonte="",  # sitemap não tem descrição; vem no enriquecimento
                sinais={"faceta": "pacote_python", "via": "sitemap",
                        "instalacao": f"pip install {nome}"},
            )
            achados += 1
        ctx.estado.marcar(NOME, sub, 0)
    ctx.log.evento("pypi_varredura", {"urls_vistas": vistos, "aproveitadas": achados})
