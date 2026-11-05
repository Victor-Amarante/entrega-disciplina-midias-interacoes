"""Dependências das rotas: o armazém, a sala do código e quem está pedindo."""

from typing import Annotated

from fastapi import Depends, Header, HTTPException, Request

from ..armazenamento import Armazem
from ..dominio.modelos import Participante, Sala


def armazem(request: Request) -> Armazem:
    return request.app.state.armazem


ArmazemDep = Annotated[Armazem, Depends(armazem)]


def sala(codigo: str, arm: ArmazemDep) -> Sala:
    encontrada = arm.obter(codigo)
    if not encontrada:
        raise HTTPException(404, "Sala não encontrada. Confira o código.")
    return encontrada


SalaDep = Annotated[Sala, Depends(sala)]


def participante(s: SalaDep, x_participante_token: Annotated[str, Header()]) -> Participante:
    eu = s.participante_por_token(x_participante_token)
    if not eu:
        raise HTTPException(401, "Você não está nesta sala.")
    return eu


ParticipanteDep = Annotated[Participante, Depends(participante)]


def host(s: SalaDep, x_host_token: Annotated[str, Header()]) -> Sala:
    if x_host_token != s.host_token:
        raise HTTPException(403, "Só o apresentador controla a sala.")
    return s


HostDep = Annotated[Sala, Depends(host)]


def exigir_fase(s: Sala, *fases: str) -> None:
    if s.fase not in fases:
        raise HTTPException(409, "Esta etapa já fechou ou ainda não abriu.")


def exigir_questionario_aberto(s: Sala) -> None:
    # Depois que os agentes começam a responder, mudar as perguntas invalidaria tudo.
    if s.ordem_perguntas:
        raise HTTPException(409, "O questionário já foi fechado. Para mudar as perguntas, crie uma sala nova.")
