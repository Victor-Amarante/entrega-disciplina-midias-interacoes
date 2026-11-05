"""Estado de uma sala de jogo. Uma sala é um teste com a turma, do começo ao fim."""

from typing import Literal

from pydantic import BaseModel, Field

Fase = Literal["lobby", "armadilhas", "respostas", "cacada", "placar", "enquete", "ataque"]
FASES: list[Fase] = ["lobby", "armadilhas", "respostas", "cacada", "placar", "enquete", "ataque"]

TipoPergunta = Literal["generica", "atencao", "local", "impossivel", "vivencia"]
Veredito = Literal["humano", "maquina"]
Opcao = Literal["a", "b"]


class ConfigSala(BaseModel):
    n_agentes: int = Field(8, ge=1, le=12)  # = personas.MAX_AGENTES: acima disso, traços se repetiriam
    frac_busca: float = Field(0.5, ge=0, le=1)
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
    autor_id: str | None = None  # None = pergunta do instituto (do apresentador)
    selecionada: bool = False
    fixa: bool = False  # as duas do instituto: sempre entram, não dá para desmarcar


class Persona(BaseModel):
    nome: str
    resumo: str
    texto: str


class Respondente(BaseModel):
    id: str
    tipo: Literal["humano", "agente"]
    rotulo: str | None = None  # número que aparece no cartão da caçada
    participante_id: str | None = None
    persona: Persona | None = None
    com_busca: bool = False
    respostas: dict[str, str] = {}
    status: Literal["pendente", "pronto", "erro"] = "pronto"
    erro: str | None = None
    custo_usd: float = 0.0
    buscas: int = 0
    segundos: float = 0.0
    simulado: bool = False


class Julgamento(BaseModel):
    juiz_id: str
    respondente_id: str
    veredito: Veredito
    pista_id: str | None = None  # pergunta cuja resposta entregou a máquina


class VotoSintetico(BaseModel):
    opcao: Opcao
    justificativa: str


class Enquete(BaseModel):
    pergunta: str = "Empresas deveriam exigir que devs usem assistentes de IA no dia a dia?"
    opcao_a: str = "Sim, exigir"
    opcao_b: str = "Não, deixar opcional"
    votos: dict[str, Opcao] = {}
    sinteticos: list[VotoSintetico] = []
    status_sinteticos: Literal["parado", "gerando", "pronto", "erro"] = "parado"
    custo_sinteticos_usd: float = 0.0


class Sala(BaseModel):
    codigo: str
    host_token: str
    criada_em: float
    fase: Fase = "lobby"
    config: ConfigSala = Field(default_factory=ConfigSala)
    participantes: dict[str, Participante] = {}
    perguntas: list[Pergunta] = []
    ordem_perguntas: list[str] = []  # congelada ao abrir a fase de respostas
    respondentes: dict[str, Respondente] = {}
    atribuicoes: dict[str, list[str]] = {}  # participante -> respondentes que ele julga
    julgamentos: list[Julgamento] = []
    enquete: Enquete = Field(default_factory=Enquete)

    def pergunta(self, pergunta_id: str) -> Pergunta | None:
        return next((p for p in self.perguntas if p.id == pergunta_id), None)

    def perguntas_em_ordem(self) -> list[Pergunta]:
        por_id = {p.id: p for p in self.perguntas}
        return [por_id[i] for i in self.ordem_perguntas if i in por_id]

    def participante_por_token(self, token: str) -> Participante | None:
        return next((p for p in self.participantes.values() if p.token == token), None)

    def agentes(self) -> list[Respondente]:
        return [r for r in self.respondentes.values() if r.tipo == "agente"]
