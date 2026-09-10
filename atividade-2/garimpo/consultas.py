"""Vocabulário de busca da Entrega 2.

Este arquivo É a especificação do recorte. O que não está aqui não aparece na
varredura, e a ausência não é do mundo — é do vocabulário.

Recorte escolhido: o MESMO tema da Entrega 1 (simulação com agentes de IA),
agora do lado do código — o que se instala, importa e chama.

LIÇÃO REAPROVEITADA DA ENTREGA 1
--------------------------------
Lá, a busca do Hugging Face rendeu 3 itens em 41 consultas porque o parâmetro
`search` casa SUBSTRING do identificador, não frase. Registro de pacote se
comporta igual: "multi-agent simulation framework" quase não casa nada no npm,
enquanto "multiagent" satura. Por isso existem duas listas separadas aqui, e
cada adaptador usa a que corresponde ao seu dialeto — em vez de descobrir isso
de novo depois de uma varredura inteira perdida.
"""

from __future__ import annotations

# --- frases: para HN, OpenAlex e busca do GitHub ---------------------------
# Ferramentas que fazem busca textual de verdade aceitam frase e ganham com ela.
FACETAS: dict[str, list[str]] = {
    "abm_framework": [
        "agent based modeling framework",
        "agent based simulation library",
        "cellular automata simulation library",
        "netlogo alternative python",
    ],
    "multiagente_llm": [
        "multi agent llm framework",
        "agent orchestration library",
        "generative agents framework",
        "llm agent simulation library",
    ],
    "ambiente_rl": [
        "multi agent reinforcement learning environment",
        "gym environment multi agent",
        "pettingzoo environment",
        "self play training environment",
    ],
    "memoria_estado": [
        "agent memory library",
        "long term memory llm agent",
        "agent state persistence library",
        "episodic memory framework",
    ],
    "observabilidade_sdk": [
        "llm agent tracing sdk",
        "agent replay library",
        "opentelemetry llm instrumentation",
        "agent execution trace library",
    ],
    "avaliacao_bench": [
        "llm agent evaluation framework",
        "agent benchmark harness",
        "multi agent benchmark suite",
    ],
    "npc_jogos": [
        "game ai behavior tree library",
        "npc dialogue engine library",
        "goal oriented action planning library",
    ],
    "simulacao_social": [
        "social network simulation library",
        "opinion dynamics simulation",
        "epidemic simulation framework",
        "crowd simulation library",
    ],
    "economia_mercado": [
        "market simulation library",
        "auction simulation framework",
        "agent based economic model",
    ],
    "sandbox_execucao": [
        "code execution sandbox library",
        "agent tool sandbox sdk",
    ],
}


def todas() -> list[tuple[str, str]]:
    """[(faceta, termo)] em ordem estável."""
    return [(f, t) for f, termos in FACETAS.items() for t in termos]


# --- termos curtos: para registros de pacote --------------------------------
# npm, crates.io, NuGet, Packagist e RubyGems casam substring de nome, descrição
# e palavra-chave. Frase longa devolve zero; termo curto satura.
TERMOS_CURTOS = [
    "multiagent", "multi-agent", "agent-based", "abm", "simulation", "simulator",
    "agents", "agent framework", "swarm", "crowd", "society", "social simulation",
    "emergent", "cellular automata", "mesa", "netlogo", "gym", "pettingzoo",
    "reinforcement learning", "self-play", "environment", "sandbox",
    "behavior tree", "goap", "npc", "dialogue", "game ai", "pathfinding",
    "agent memory", "episodic memory", "vector memory", "state machine",
    "orchestration", "workflow agents", "agent runtime", "tracing", "telemetry",
    "replay", "observability", "evaluation", "benchmark", "eval harness",
    "market simulation", "auction", "game theory", "discrete event",
    "monte carlo", "epidemic", "opinion dynamics", "network simulation",
]

# --- tópicos do GitHub -----------------------------------------------------
# Tópico é curadoria feita pelo próprio autor do repositório: mais preciso que
# busca textual, e traz projeto que a busca por palavra não alcança.
TOPICOS_GITHUB = [
    "agent-based-modeling", "agent-based-simulation", "multi-agent-systems",
    "multi-agent-reinforcement-learning", "multiagent-systems",
    "generative-agents", "llm-agents", "ai-agents", "agent-framework",
    "social-simulation", "complex-systems", "emergent-behavior",
    "simulation-framework", "discrete-event-simulation", "crowd-simulation",
    "behavior-tree", "game-ai", "npc", "reinforcement-learning-environments",
    "llm-observability", "agent-evaluation",
]

# --- consultas de busca do GitHub ------------------------------------------
FACETA_DA_CONSULTA_GITHUB = {
    "agent based modeling framework": "abm_framework",
    "multi agent simulation library": "abm_framework",
    "generative agents framework": "multiagente_llm",
    "multi agent llm orchestration": "multiagente_llm",
    "multi agent reinforcement learning env": "ambiente_rl",
    "agent memory library": "memoria_estado",
    "llm tracing sdk": "observabilidade_sdk",
    "agent evaluation harness": "avaliacao_bench",
    "behavior tree npc": "npc_jogos",
    "social simulation python": "simulacao_social",
}
CONSULTAS_GITHUB = list(FACETA_DA_CONSULTA_GITHUB)
