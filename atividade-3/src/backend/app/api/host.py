"""Rotas do apresentador: criar a sala, mudar de fase, escolher as armadilhas."""

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

from ..armazenamento import novo_id
from ..dominio.modelos import Pergunta
from ..servicos import jogo, placar, visoes
from .deps import ArmazemDep, HostDep, exigir_fase, exigir_questionario_aberto
from .esquemas import EdicaoEnquete, MudancaDeFase, NovaSala, PerguntaDoInstituto

rotas = APIRouter(tags=["apresentador"])


@rotas.post("/salas")
async def criar_sala(corpo: NovaSala, arm: ArmazemDep):
    s = arm.criar(corpo.config)
    return {"codigo": s.codigo, "host_token": s.host_token}


@rotas.get("/salas/{codigo}/painel")
async def painel(s: HostDep):
    return visoes.do_painel(s)


@rotas.get("/salas/{codigo}/dados")
async def baixar_dados(s: HostDep):
    """Tudo o que aconteceu na sala, para o REGISTRO.md. Sem os tokens de acesso."""
    dados = s.model_dump(exclude={"host_token": True, "participantes": {"__all__": {"token"}}})
    dados["placar"] = placar.calcular(s)
    return JSONResponse(
        dados,
        headers={"Content-Disposition": f'attachment; filename="sala-{s.codigo}.json"'},
    )


@rotas.post("/salas/{codigo}/fase")
async def mudar_fase(corpo: MudancaDeFase, s: HostDep, arm: ArmazemDep):
    jogo.mudar_fase(s, corpo.fase, salvar=lambda: arm.salvar(s))
    arm.salvar(s)
    return visoes.do_painel(s)


@rotas.post("/salas/{codigo}/perguntas")
async def nova_pergunta(corpo: PerguntaDoInstituto, s: HostDep, arm: ArmazemDep):
    exigir_fase(s, "lobby", "armadilhas")
    exigir_questionario_aberto(s)
    cabe = sum(p.selecionada for p in s.perguntas) < s.config.max_perguntas
    s.perguntas.append(Pergunta(id=novo_id("q"), texto=corpo.texto.strip(), tipo=corpo.tipo, selecionada=cabe))
    arm.salvar(s)
    return visoes.do_painel(s)


@rotas.post("/salas/{codigo}/perguntas/{pergunta_id}/alternar")
async def alternar_pergunta(pergunta_id: str, s: HostDep, arm: ArmazemDep):
    exigir_fase(s, "lobby", "armadilhas")
    exigir_questionario_aberto(s)
    pergunta = s.pergunta(pergunta_id)
    if not pergunta:
        raise HTTPException(404, "Pergunta não encontrada.")
    if pergunta.fixa:
        raise HTTPException(409, "As perguntas do instituto são fixas: servem de comparação.")
    selecionadas = sum(p.selecionada for p in s.perguntas)
    if not pergunta.selecionada and selecionadas >= s.config.max_perguntas:
        raise HTTPException(409, f"O questionário já está cheio ({selecionadas}/{s.config.max_perguntas}). Desmarque outra antes.")
    pergunta.selecionada = not pergunta.selecionada
    arm.salvar(s)
    return visoes.do_painel(s)


@rotas.post("/salas/{codigo}/perguntas/sortear")
async def sortear(s: HostDep, arm: ArmazemDep):
    exigir_fase(s, "lobby", "armadilhas")
    exigir_questionario_aberto(s)
    for p in s.perguntas:
        if p.autor_id:
            p.selecionada = False
    jogo.sortear_armadilhas(s)
    arm.salvar(s)
    return visoes.do_painel(s)


@rotas.post("/salas/{codigo}/agentes/{agente_id}/tentar-de-novo")
async def tentar_de_novo(agente_id: str, s: HostDep, arm: ArmazemDep):
    if not jogo.tentar_agente_de_novo(s, agente_id, salvar=lambda: arm.salvar(s)):
        raise HTTPException(409, "Este agente não está com erro.")
    arm.salvar(s)
    return visoes.do_painel(s)


@rotas.put("/salas/{codigo}/enquete")
async def editar_enquete(corpo: EdicaoEnquete, s: HostDep, arm: ArmazemDep):
    if s.enquete.votos:
        raise HTTPException(409, "A enquete já tem votos; não dá mais para editar.")
    s.enquete.pergunta = corpo.pergunta.strip()
    s.enquete.opcao_a = corpo.opcao_a.strip()
    s.enquete.opcao_b = corpo.opcao_b.strip()
    arm.salvar(s)
    return visoes.do_painel(s)
