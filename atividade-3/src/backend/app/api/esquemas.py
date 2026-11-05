"""Corpos de requisição."""

from pydantic import BaseModel, Field

from ..dominio.modelos import ConfigSala, Fase, Opcao, TipoPergunta, Veredito


class NovaSala(BaseModel):
    config: ConfigSala = Field(default_factory=ConfigSala)


class Entrada(BaseModel):
    apelido: str = Field(min_length=1, max_length=24)


class NovaArmadilha(BaseModel):
    texto: str = Field(min_length=5, max_length=300)
    tipo: TipoPergunta


class Respostas(BaseModel):
    respostas: dict[str, str]


class NovoJulgamento(BaseModel):
    respondente_id: str
    veredito: Veredito
    pista_id: str | None = None


class Voto(BaseModel):
    opcao: Opcao


class MudancaDeFase(BaseModel):
    fase: Fase


class PerguntaDoInstituto(BaseModel):
    texto: str = Field(min_length=5, max_length=300)
    tipo: TipoPergunta = "generica"


class EdicaoEnquete(BaseModel):
    pergunta: str = Field(min_length=5, max_length=200)
    opcao_a: str = Field(min_length=1, max_length=60)
    opcao_b: str = Field(min_length=1, max_length=60)
