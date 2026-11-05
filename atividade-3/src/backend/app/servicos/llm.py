"""Cliente da API do Claude e cálculo de custo, compartilhados pelos serviços."""

from dataclasses import dataclass

import anthropic

from ..config import CONFIG, PRECO_BUSCA, PRECOS

_cliente: anthropic.AsyncAnthropic | None = None


def cliente() -> anthropic.AsyncAnthropic:
    global _cliente
    if _cliente is None:
        _cliente = anthropic.AsyncAnthropic(timeout=180.0, max_retries=2)
    return _cliente


@dataclass
class Gasto:
    usd: float = 0.0
    buscas: int = 0

    def somar(self, usage) -> None:
        preco_entrada, preco_saida = PRECOS.get(CONFIG.modelo, PRECOS["claude-opus-5-5"])
        entrada = (
            usage.input_tokens
            + (usage.cache_creation_input_tokens or 0) * 1.25
            + (usage.cache_read_input_tokens or 0) * 0.1
        )
        self.usd += (entrada * preco_entrada + usage.output_tokens * preco_saida) / 1_000_000
        uso_servidor = getattr(usage, "server_tool_use", None)
        buscas = (getattr(uso_servidor, "web_search_requests", 0) or 0) if uso_servidor else 0
        self.buscas += buscas
        self.usd += buscas * PRECO_BUSCA


def eh_haiku() -> bool:
    return CONFIG.modelo.startswith("claude-haiku")


async def criar_mensagem(system: str, messages: list, tools: list):
    extras = {}
    if not eh_haiku():
        # Se o classificador de segurança recusar, a API refaz o pedido em outro
        # modelo em vez de devolver a recusa. O Haiku não tem esse fallback.
        extras = {"betas": ["server-side-fallback-2026-07-01"], "fallbacks": "default"}
    return await cliente().beta.messages.create(
        model=CONFIG.modelo,
        max_tokens=8000,
        system=system,
        messages=messages,
        tools=tools,
        output_config={"effort": CONFIG.esforco},
        **extras,
    )


async def chamar_ferramenta(system: str, pedido: str, ferramenta: dict, extras: list | None = None, gasto: Gasto | None = None) -> dict:
    """Roda a conversa até o modelo chamar `ferramenta` e devolve o input dela.

    `extras` são ferramentas de servidor (busca na web), que o modelo pode usar antes.
    """
    gasto = gasto if gasto is not None else Gasto()
    messages: list = [{"role": "user", "content": pedido}]
    tools = [ferramenta, *(extras or [])]
    for _ in range(5):
        resposta = await criar_mensagem(system, messages, tools)
        gasto.somar(resposta.usage)
        if resposta.stop_reason == "refusal":
            raise RuntimeError("o modelo recusou")
        for bloco in resposta.content:
            if bloco.type == "tool_use" and bloco.name == ferramenta["name"]:
                return bloco.input
        messages.append({"role": "assistant", "content": resposta.content})
        if resposta.stop_reason == "pause_turn":
            continue  # a busca no servidor pausou; reenviar retoma de onde parou
        messages.append(
            {"role": "user", "content": f"Agora envie usando a ferramenta {ferramenta['name']}."}
        )
    raise RuntimeError("o modelo não chamou a ferramenta")
