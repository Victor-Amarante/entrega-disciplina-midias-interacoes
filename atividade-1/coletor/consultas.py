"""Vocabulário de busca da varredura.

Este arquivo É a especificação do recorte. Se uma categoria de ferramenta não
está aqui, ela não vai aparecer na varredura — e a ausência não é do mundo, é
do vocabulário. Por isso ele fica versionado e separado do código: dá para
apontar depois "varri com ESTES 40 termos, e por isso não vi aquilo".

Recorte escolhido pelo aluno: simulação com agentes de IA entendida como
AMBIENTE que se abre e se usa (Entrega 1 = inspiração), não como biblioteca
que se importa (isso é Entrega 2).
"""

from __future__ import annotations

# Cada faceta cobre um jeito diferente de "simulação de agentes" existir como
# produto. A faceta viaja junto com o candidato para o relatório de cobertura:
# se no fim uma faceta trouxe 3 itens e outra 900, isso é informação.
FACETAS: dict[str, list[str]] = {
    "sociedade_simulada": [
        "generative agents simulation",
        "agent society simulation",
        "social simulation LLM",
        "AI town simulation",
        "emergent behavior multi agent",
        "artificial society simulation",
    ],
    "sandbox_ambiente": [
        "multi agent sandbox",
        "LLM agent playground",
        "agent simulation environment",
        "virtual world AI agents",
        "multi agent simulation platform",
        "no-code multi agent builder",
    ],
    "observabilidade_replay": [
        "LLM agent observability",
        "agent trace viewer",
        "agent replay debugging",
        "multi agent conversation visualizer",
        "agent execution timeline",
    ],
    "avaliacao_arena": [
        "LLM agent benchmark platform",
        "agent evaluation arena",
        "multi agent competition environment",
        "agent leaderboard simulation",
    ],
    "npc_jogos": [
        "AI NPC game",
        "LLM game characters",
        "AI villager simulation",
        "generative agents game",
        "AI driven simulation game",
    ],
    "usuarios_sinteticos": [
        "synthetic users research",
        "AI persona simulation research",
        "synthetic focus group",
        "simulated customer interviews AI",
        "digital twin of customer",
    ],
    "abm_classico": [
        "agent based modeling tool",
        "agent based simulation software",
        "crowd simulation tool",
        "social science simulation platform",
    ],
    "economia_negociacao": [
        "market simulation agents",
        "negotiation agents simulation",
        "auction simulation multi agent",
        "supply chain agent simulation",
    ],
    "robotica_mundo": [
        "embodied agents simulator",
        "multi agent robotics simulator",
        "3D environment AI agents",
    ],
}


def todas() -> list[tuple[str, str]]:
    """[(faceta, termo)] em ordem estável."""
    return [(f, t) for f, termos in FACETAS.items() for t in termos]


# Termos curtos para o Hugging Face.
#
# Medido: o parâmetro `search` da API do HF faz correspondência de SUBSTRING no
# identificador do Space, não busca semântica. "multi agent sandbox" devolve 1
# resultado; "agent simulation" devolve 32; "agent" sozinho satura em 100.
# Frase longa não funciona aqui — daí esta lista separada do vocabulário frasal
# que serve para HN e arXiv. Fonte diferente, dialeto diferente.
TERMOS_CURTOS_HF = [
    "agent", "agents", "multiagent", "multi-agent", "simulation", "simulator",
    "sandbox", "society", "social", "crowd", "swarm", "emergent", "population",
    "npc", "town", "village", "world", "environment", "roleplay", "persona",
    "debate", "negotiation", "market", "economy", "auction", "game-theory",
    "arena", "benchmark", "leaderboard", "evaluation", "trace", "replay",
    "observability", "visualizer", "timeline", "abm", "netlogo", "mesa",
    "autogen", "crewai", "langgraph", "camel", "generative-agents", "ai-town",
]

# Subreddits varridos (só os que respondem por RSS; o endpoint .json devolve 403).
SUBREDDITS = [
    "LLMDevs", "AI_Agents", "MachineLearning", "singularity", "LocalLLaMA",
    "artificial", "gamedev", "proceduralgeneration", "simulation", "compsocialsci",
]

# Tags do itch.io permitidas por robots.txt (/search é proibido, /games/tag-* não).
TAGS_ITCHIO = [
    "artificial-intelligence", "simulation", "sandbox", "life-simulation",
    "procedural-generation", "emergent", "colony-sim", "god-game",
]

# Termos de busca do GitHub. Aqui o alvo é diferente: o campo `homepage` do
# repositório costuma apontar para o app hospedado — é ELE que interessa na
# Entrega 1, não o repositório.
CONSULTAS_GITHUB = [
    "generative agents simulation",
    "multi agent simulation llm",
    "agent based model web",
    "ai town",
    "agent sandbox llm",
    "npc ai llm game",
    "agent observability trace",
    "social simulation agents",
]
