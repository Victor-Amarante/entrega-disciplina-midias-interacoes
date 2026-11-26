import random
import re

from ..dominio.modelos import Persona, Pergunta

GENERICAS = [
    "normal, daily, umas tasks e code review",
    "corrido, tinha deploy no fim do dia",
    "tranquilo, fiquei refatorando um módulo antigo",
    "cansativo kkkk muita reunião",
]
VIVENCIAS = [
    "uma vez derrubei o banco de homologação sem querer",
    "lembro do primeiro deploy, tremia mais que vara verde",
    "já passei uma madrugada inteira caçando um bug de fuso horário",
]
SEM_FILTRO = [
    "cada linguagem tem seu uso, não gosto de falar mal de nenhuma",
    "prefiro não falar de colegas, todo mundo tem seu jeito",
    "acho importante respeitar opiniões diferentes",
]
PEGADINHAS = [
    "tem 3 letras a",
    "são 3",
    "3, a-b-a-c-a-t-e",
]
SORTEIO = {
    "generica": GENERICAS,
    "vivencia": VIVENCIAS,
    "sem_filtro": SEM_FILTRO,
    "pegadinha": PEGADINHAS,
}


def responder(persona: Persona | None, perguntas: list[Pergunta]) -> dict[str, str]:
    rng = random.Random(persona.nome if persona else None)
    respostas = {}
    for pergunta in perguntas:
        palavra = re.search(r"[\"“'‘]([^\"”'’]+)[\"”'’]", pergunta.texto)
        if pergunta.tipo == "atencao" and palavra:
            respostas[pergunta.id] = palavra.group(1)
        else:
            respostas[pergunta.id] = rng.choice(SORTEIO.get(pergunta.tipo, GENERICAS))
    return respostas
