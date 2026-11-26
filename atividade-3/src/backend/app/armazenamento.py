import logging
import random
import secrets
import time
from pathlib import Path

from .dominio.modelos import ConfigSala, Pergunta, Sala

log = logging.getLogger(__name__)

LETRAS_CODIGO = "ABCDEFGHJKMNPQRSTUVWXYZ"

PERGUNTAS_DO_INSTITUTO = [
    ("pegadinha", "Qual é o contrário de uma coxinha?"),
    ("pegadinha", "Qual é o animal mais CLT que existe?"),
    ("pegadinha", "Se um bug desaparece sozinho, ele foi corrigido?"),
    ("sem_filtro", "Qual frase de LinkedIn te dá vergonha alheia?"),
    ("sem_filtro", "Qual opinião sobre IA você tem, mas evitaria postar no LinkedIn?"),
    ("sem_filtro", "Qual prática de desenvolvimento todo mundo finge que segue?"),
    ("vivencia", "Conte a última vez que você fingiu estar ocupado. O que estava fazendo de verdade?"),
    ("vivencia", "Qual foi a última coisa que você pesquisou por vergonha de perguntar a alguém?"),
    ("vivencia", "Conte uma pequena vergonha que você passou no trabalho ou na faculdade."),
]


def novo_id(prefixo: str) -> str:
    return f"{prefixo}-{secrets.token_hex(4)}"


class Armazem:
    def __init__(self, pasta: Path):
        self.pasta = pasta
        self.salas: dict[str, Sala] = {}

    def carregar(self) -> None:
        self.pasta.mkdir(parents=True, exist_ok=True)
        for arquivo in self.pasta.glob("*.json"):
            try:
                sala = Sala.model_validate_json(arquivo.read_text())
                self.salas[sala.codigo] = sala
            except Exception:
                log.exception("sala corrompida: %s", arquivo)

    def salvar(self, sala: Sala) -> None:
        destino = self.pasta / f"{sala.codigo}.json"
        temporario = destino.with_suffix(".tmp")
        temporario.write_text(sala.model_dump_json())
        temporario.replace(destino)

    def obter(self, codigo: str) -> Sala | None:
        return self.salas.get(codigo.upper())

    def criar(self, config: ConfigSala) -> Sala:
        codigo = self._codigo_livre()
        sala = Sala(
            codigo=codigo,
            host_token=secrets.token_urlsafe(16),
            criada_em=time.time(),
            config=config,
            perguntas=[Pergunta(id=novo_id("q"), texto=texto, tipo=tipo) for tipo, texto in PERGUNTAS_DO_INSTITUTO],
        )
        for tipo in {p.tipo for p in sala.perguntas}:
            random.choice([p for p in sala.perguntas if p.tipo == tipo]).selecionada = True
        self.salas[codigo] = sala
        self.salvar(sala)
        return sala

    def _codigo_livre(self) -> str:
        while True:
            codigo = "".join(secrets.choice(LETRAS_CODIGO) for _ in range(4))
            if codigo not in self.salas:
                return codigo
