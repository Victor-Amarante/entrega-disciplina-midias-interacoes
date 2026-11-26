from typing import Literal

from pydantic import BaseModel, Field, field_validator

Fase = Literal["lobby", "armadilhas", "respostas", "cacada", "placar"]
FASES: list[Fase] = ["lobby", "armadilhas", "respostas", "cacada", "placar"]

TipoPergunta = Literal[
    "generica", "atencao", "vivencia", "sem_filtro", "pegadinha",
    "local", "impossivel", "invertida", "sala",
]
TIPOS_DA_TURMA: set[str] = {"vivencia", "sem_filtro", "pegadinha"}
Veredito = Literal["humano", "maquina"]


class ConfigSala(BaseModel):
    n_agentes: int = Field(8, ge=1, le=12)
    max_perguntas: int = Field(6, ge=2, le=10)
    cards_por_juiz: int = Field(8, ge=2, le=20)


class Participante(BaseModel):
    id: str
    token: str
    apelido: str


class Pergunta(BaseModel):
    id: str
    texto: str
    tipo: TipoPergunta
    autor_id: str | None = None
    selecionada: bool = False


class Persona(BaseModel):
    nome: str
    resumo: str
    texto: str


class Respondente(BaseModel):
    id: str
    tipo: Literal["humano", "agente"]
    rotulo: str | None = None
    participante_id: str | None = None
    persona: Persona | None = None
    respostas: dict[str, str] = {}
    status: Literal["pendente", "pronto", "erro"] = "pronto"
    erro: str | None = None
    custo_usd: float = 0.0
    segundos: float = 0.0
    simulado: bool = False


class Julgamento(BaseModel):
    juiz_id: str
    respondente_id: str
    veredito: Veredito
    pista_id: str | None = None


class Sala(BaseModel):
    codigo: str
    host_token: str
    criada_em: float
    fase: Fase = "lobby"
    config: ConfigSala = Field(default_factory=ConfigSala)
    participantes: dict[str, Participante] = {}
    perguntas: list[Pergunta] = []
    ordem_perguntas: list[str] = []
    respondentes: dict[str, Respondente] = {}
    atribuicoes: dict[str, list[str]] = {}
    julgamentos: list[Julgamento] = []

    @field_validator("fase", mode="before")
    @classmethod
    def _fase_removida(cls, fase: str) -> str:
        return "placar" if fase in ("enquete", "ataque") else fase

    def pergunta(self, pergunta_id: str) -> Pergunta | None:
        return next((p for p in self.perguntas if p.id == pergunta_id), None)

    def perguntas_em_ordem(self) -> list[Pergunta]:
        por_id = {p.id: p for p in self.perguntas}
        return [por_id[i] for i in self.ordem_perguntas if i in por_id]

    def participante_por_token(self, token: str) -> Participante | None:
        return next((p for p in self.participantes.values() if p.token == token), None)

    def agentes(self) -> list[Respondente]:
        return [r for r in self.respondentes.values() if r.tipo == "agente"]
