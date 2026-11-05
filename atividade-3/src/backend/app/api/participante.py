"""Rotas do celular de quem joga."""

import secrets

from fastapi import APIRouter, HTTPException

from ..armazenamento import novo_id
from ..dominio.modelos import Julgamento, Participante, Pergunta, Respondente
from ..servicos import jogo, visoes
from .deps import ArmazemDep, ParticipanteDep, SalaDep, exigir_fase, exigir_questionario_aberto
from .esquemas import Entrada, NovaArmadilha, NovoJulgamento, Respostas, Voto

rotas = APIRouter(prefix="/salas/{codigo}", tags=["participante"])


@rotas.post("/entrar")
async def entrar(corpo: Entrada, s: SalaDep, arm: ArmazemDep):
    exigir_fase(s, "lobby", "armadilhas", "respostas", "cacada")
    eu = Participante(id=novo_id("p"), token=secrets.token_urlsafe(16), apelido=corpo.apelido.strip())
    s.participantes[eu.id] = eu
    arm.salvar(s)
    return {"participante_id": eu.id, "token": eu.token}


@rotas.get("/eu")
async def minha_visao(s: SalaDep, eu: ParticipanteDep, arm: ArmazemDep):
    sorteados_antes = eu.id in s.atribuicoes
    visao = visoes.do_participante(s, eu)
    if not sorteados_antes and eu.id in s.atribuicoes:
        arm.salvar(s)  # os cartões foram sorteados agora
    return visao


@rotas.post("/armadilhas")
async def nova_armadilha(corpo: NovaArmadilha, s: SalaDep, eu: ParticipanteDep, arm: ArmazemDep):
    exigir_fase(s, "armadilhas")
    exigir_questionario_aberto(s)
    minhas = [p for p in s.perguntas if p.autor_id == eu.id]
    if len(minhas) >= jogo.LIMITE_ARMADILHAS_POR_PESSOA:
        raise HTTPException(409, "Você já mandou o máximo de armadilhas.")
    s.perguntas.append(Pergunta(id=novo_id("q"), texto=corpo.texto.strip(), tipo=corpo.tipo, autor_id=eu.id))
    arm.salvar(s)
    return {"ok": True}


@rotas.delete("/armadilhas/{pergunta_id}")
async def apagar_armadilha(pergunta_id: str, s: SalaDep, eu: ParticipanteDep, arm: ArmazemDep):
    exigir_fase(s, "armadilhas")
    exigir_questionario_aberto(s)
    s.perguntas = [p for p in s.perguntas if not (p.id == pergunta_id and p.autor_id == eu.id)]
    arm.salvar(s)
    return {"ok": True}


@rotas.post("/respostas")
async def responder(corpo: Respostas, s: SalaDep, eu: ParticipanteDep, arm: ArmazemDep):
    exigir_fase(s, "respostas")
    ids = set(s.ordem_perguntas)
    respostas = {pid: texto.strip()[:500] for pid, texto in corpo.respostas.items() if pid in ids}
    s.respondentes[f"h-{eu.id}"] = Respondente(
        id=f"h-{eu.id}", tipo="humano", participante_id=eu.id, respostas=respostas
    )
    arm.salvar(s)
    return {"ok": True}


@rotas.post("/julgamentos")
async def julgar(corpo: NovoJulgamento, s: SalaDep, eu: ParticipanteDep, arm: ArmazemDep):
    exigir_fase(s, "cacada")
    if corpo.respondente_id not in s.atribuicoes.get(eu.id, []):
        raise HTTPException(400, "Este cartão não é seu.")
    s.julgamentos = [
        j for j in s.julgamentos
        if not (j.juiz_id == eu.id and j.respondente_id == corpo.respondente_id)
    ]
    s.julgamentos.append(Julgamento(juiz_id=eu.id, **corpo.model_dump()))
    arm.salvar(s)
    return {"ok": True}


@rotas.post("/voto")
async def votar(corpo: Voto, s: SalaDep, eu: ParticipanteDep, arm: ArmazemDep):
    exigir_fase(s, "enquete")
    s.enquete.votos[eu.id] = corpo.opcao
    arm.salvar(s)
    return {"ok": True}
