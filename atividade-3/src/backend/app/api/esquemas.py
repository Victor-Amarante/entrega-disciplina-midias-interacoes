from pydantic import BaseModel, Field, field_validator

from ..dominio.modelos import TIPOS_DA_TURMA, ConfigSala, Fase, TipoPergunta, Veredito


class NovaSala(BaseModel):
    config: ConfigSala = Field(default_factory=ConfigSala)


class Entrada(BaseModel):
    apelido: str = Field(min_length=1, max_length=24)


class NovaArmadilha(BaseModel):
    texto: str = Field(min_length=5, max_length=300)
    tipo: TipoPergunta

    @field_validator("tipo")
    @classmethod
    def _tipo_da_turma(cls, tipo: str) -> str:
        if tipo not in TIPOS_DA_TURMA:
            raise ValueError("tipo de armadilha indisponível")
        return tipo


class Respostas(BaseModel):
    respostas: dict[str, str]


class NovoJulgamento(BaseModel):
    respondente_id: str
    veredito: Veredito
    pista_id: str | None = None


class MudancaDeFase(BaseModel):
    fase: Fase


class PerguntaDoInstituto(BaseModel):
    texto: str = Field(min_length=5, max_length=300)
    tipo: TipoPergunta = "generica"
