"""Respostas prontas para quando não há chave da API. Servem para testar a interface,
não para o experimento: são fáceis de pegar de propósito."""

import random
import re

from ..dominio.modelos import Persona, Pergunta

GENERICAS = [
    "normal, daily, umas tasks e code review",
    "corrido, tinha deploy no fim do dia",
    "tranquilo, fiquei refatorando um módulo antigo",
    "cansativo kkkk muita reunião",
]
LOCAIS = [
    "acho que sim, mas não lembro direito",
    "geralmente almoço por ali perto do porto digital",
    "uso isso no trabalho mas não sei os detalhes",
    "sei não, nunca reparei",
]
IMPOSSIVEIS = [
    "não fiquei sabendo disso não",
    "vi alguma coisa no grupo mas não prestei atenção",
    "foi massa, todo mundo comentando",
]
VIVENCIAS = [
    "uma vez derrubei o banco de homologação sem querer",
    "lembro do primeiro deploy, tremia mais que vara verde",
    "já passei uma madrugada inteira caçando um bug de fuso horário",
]
SORTEIO = {"generica": GENERICAS, "local": LOCAIS, "impossivel": IMPOSSIVEIS, "vivencia": VIVENCIAS}


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


def justificativas(n: int, opcao: str) -> list[str]:
    base = [
        f"{opcao.lower()}, sem dúvida",
        "acho que é o mais justo pra todo mundo",
        "já vi isso funcionar em outra empresa",
        "a maioria dos meus amigos pensa assim",
        "não tem como controlar mesmo, melhor assim",
        "pensei bastante e fico com essa",
    ]
    return [random.choice(base) for _ in range(n)]
