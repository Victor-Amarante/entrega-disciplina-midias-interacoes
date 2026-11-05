"""Regras do jogo: o que acontece ao mudar de fase e como os cartões são distribuídos."""

import asyncio
import random
from collections import Counter
from collections.abc import Callable

from ..armazenamento import novo_id
from ..dominio.modelos import FASES, Fase, Respondente, Sala
from . import agentes, enquete, personas

LIMITE_ARMADILHAS_POR_PESSOA = 2

# Guarda referência das tarefas em segundo plano para o GC não as recolher no meio.
_tarefas: set[asyncio.Task] = set()


def _em_segundo_plano(coro, ao_terminar: Callable[[], None]) -> None:
    tarefa = asyncio.create_task(coro)
    _tarefas.add(tarefa)

    def fim(t: asyncio.Task) -> None:
        _tarefas.discard(t)
        ao_terminar()

    tarefa.add_done_callback(fim)


def mudar_fase(sala: Sala, fase: Fase, salvar: Callable[[], None]) -> None:
    sala.fase = fase
    if fase == "respostas" and not sala.ordem_perguntas:
        _fechar_questionario(sala)
        _lancar_agentes(sala, salvar)
    elif fase == "cacada":
        _numerar_cartoes(sala)
    elif fase == "ataque" and sala.enquete.status_sinteticos in ("parado", "erro"):
        _em_segundo_plano(enquete.gerar_sinteticos(sala), salvar)


def proxima_fase(sala: Sala) -> Fase | None:
    i = FASES.index(sala.fase)
    return FASES[i + 1] if i + 1 < len(FASES) else None


def fase_anterior(sala: Sala) -> Fase | None:
    i = FASES.index(sala.fase)
    return FASES[i - 1] if i > 0 else None


# --- armadilhas -----------------------------------------------------------------


def sortear_armadilhas(sala: Sala) -> None:
    """Marca armadilhas da turma até completar o questionário, variando os tipos."""
    da_turma = [p for p in sala.perguntas if p.autor_id]
    vagas = sala.config.max_perguntas - sum(1 for p in sala.perguntas if p.selecionada)
    if vagas <= 0:
        return
    por_tipo: dict[str, list] = {}
    for p in random.sample(da_turma, k=len(da_turma)):
        if not p.selecionada:
            por_tipo.setdefault(p.tipo, []).append(p)
    filas = list(por_tipo.values())
    random.shuffle(filas)
    while vagas > 0 and any(filas):
        for fila in filas:
            if fila and vagas > 0:
                fila.pop().selecionada = True
                vagas -= 1


def _fechar_questionario(sala: Sala) -> None:
    for p in sala.perguntas:
        if p.fixa:
            p.selecionada = True
    if not any(p.selecionada and p.autor_id for p in sala.perguntas):
        sortear_armadilhas(sala)
    selecionadas = [p for p in sala.perguntas if p.selecionada]
    # Genéricas do instituto abrem o questionário; a checagem de atenção vai no meio.
    abertura = [p for p in selecionadas if not p.autor_id and p.tipo != "atencao"]
    atencao = [p for p in selecionadas if not p.autor_id and p.tipo == "atencao"]
    resto = [p for p in selecionadas if p.autor_id]
    random.shuffle(resto)
    meio = len(resto) // 2
    ordem = abertura + resto[:meio] + atencao + resto[meio:]
    sala.ordem_perguntas = [p.id for p in ordem]


# --- agentes --------------------------------------------------------------------


def _lancar_agentes(sala: Sala, salvar: Callable[[], None]) -> None:
    n = sala.config.n_agentes
    n_busca = round(n * sala.config.frac_busca)
    lista = personas.gerar_personas(n)
    for i, persona in enumerate(lista):
        agente = Respondente(
            id=novo_id("a"),
            tipo="agente",
            persona=persona,
            com_busca=i < n_busca,
            status="pendente",
        )
        sala.respondentes[agente.id] = agente
        _em_segundo_plano(agentes.responder(agente, sala.perguntas_em_ordem()), salvar)


def tentar_agente_de_novo(sala: Sala, agente_id: str, salvar: Callable[[], None]) -> bool:
    agente = sala.respondentes.get(agente_id)
    if not agente or agente.tipo != "agente" or agente.status != "erro":
        return False
    agente.status = "pendente"
    _em_segundo_plano(agentes.responder(agente, sala.perguntas_em_ordem()), salvar)
    return True


# --- caçada ---------------------------------------------------------------------


def _numerar_cartoes(sala: Sala) -> None:
    """Dá um número de 10 a 99 a cada respondente pronto. Sorteado, para a ordem de
    chegada não denunciar quem é agente."""
    usados = {r.rotulo for r in sala.respondentes.values() if r.rotulo}
    livres = [str(n) for n in range(10, 100) if str(n) not in usados]
    random.shuffle(livres)
    for r in sala.respondentes.values():
        if not r.rotulo and r.status == "pronto" and r.respostas and livres:
            r.rotulo = livres.pop()


def cartoes_do_juiz(sala: Sala, participante_id: str) -> list[str]:
    """Sorteia (uma vez) os respondentes que o participante vai julgar: metade
    agentes e metade humanos quando dá, preferindo os menos julgados."""
    if participante_id in sala.atribuicoes:
        return sala.atribuicoes[participante_id]
    _numerar_cartoes(sala)  # agentes que terminaram depois de a caçada abrir
    proprio = f"h-{participante_id}"
    prontos = [
        r for r in sala.respondentes.values()
        if r.rotulo and r.status == "pronto" and r.id != proprio
    ]
    uso = Counter(rid for lista in sala.atribuicoes.values() for rid in lista)

    def menos_usados(tipo: str) -> list[Respondente]:
        lista = [r for r in prontos if r.tipo == tipo]
        random.shuffle(lista)
        return sorted(lista, key=lambda r: uso[r.id])

    k = sala.config.cards_por_juiz
    ags, hums = menos_usados("agente"), menos_usados("humano")
    n_ag = min(len(ags), k // 2)
    n_hum = min(len(hums), k - n_ag)
    n_ag = min(len(ags), k - n_hum)
    escolha = [r.id for r in ags[:n_ag] + hums[:n_hum]]
    random.shuffle(escolha)
    if escolha:
        sala.atribuicoes[participante_id] = escolha
    return escolha
