"""Personas de desenvolvedor de software para os agentes, montadas a partir de listas.

Segue a ideia de Westwood: uma persona longa e concreta, com rotina, trajetória e
jeito de escrever, para o agente ter de onde tirar detalhes de "vida vivida".
O ofício de dev é bem documentado na web, então o agente com busca acha com
facilidade o que precisa para sustentar a persona.

Dentro de uma sala, nenhum traço se repete entre agentes: se dois agentes tivessem
a mesma stack ou a mesma empresa, contariam histórias parecidas, e o jogador
pegaria a coincidência do sorteio em vez da máquina. Por isso cada lista tem pelo
menos MAX_AGENTES itens.
"""

import random

from ..dominio.modelos import Persona

MAX_AGENTES = 12

NOMES = [
    ("Ana Clara", "mulher"), ("Beatriz", "mulher"), ("Camila", "mulher"), ("Júlia", "mulher"),
    ("Larissa", "mulher"), ("Maria Eduarda", "mulher"), ("Rafaela", "mulher"), ("Thaís", "mulher"),
    ("Arthur", "homem"), ("Caio", "homem"), ("Davi", "homem"), ("Gabriel", "homem"),
    ("João Pedro", "homem"), ("Lucas", "homem"), ("Matheus", "homem"), ("Pedro Henrique", "homem"),
    ("Rodrigo", "homem"), ("Vinícius", "homem"), ("Kauã", "homem"), ("Sam", "pessoa não binária"),
]

# (cargo, faixa de idade, faixa de anos de experiência). Escritos sem marca de
# gênero, para servir a qualquer nome. São só cinco níveis, então o cargo se
# repete com mais de cinco agentes; o sorteio espalha os níveis por igual.
CARGOS = [
    ("faz estágio em desenvolvimento", (19, 23), (0, 1)),
    ("é dev júnior", (21, 27), (1, 3)),
    ("é dev pleno", (24, 32), (3, 6)),
    ("é dev sênior", (28, 40), (6, 14)),
    ("é tech lead", (30, 42), (8, 16)),
]
FREELANCER = "como freelancer, pegando projetos de sites e sistemas internos"

STACKS = [
    "front-end, em React e TypeScript",
    "back-end, em Java e Spring Boot",
    "back-end, em Python com Django e FastAPI",
    "back-end, em Go, com microsserviços na AWS",
    "apps Android, em Kotlin",
    "apps mobile, em Flutter",
    "full stack, em Next.js e Node",
    "engenharia de dados, em Python, Spark e Airflow",
    "infraestrutura e DevOps, com Kubernetes e Terraform",
    "back-end, em C# e .NET",
    "QA e automação de testes, com Cypress e Playwright",
    "sistemas web em PHP com Laravel",
]

EMPRESAS = [
    "numa fintech em Recife, no Porto Digital, em modelo híbrido",
    "numa consultoria de software que atende clientes de fora, em remoto",
    "numa empresa gringa, em remoto, recebendo em dólar",
    "no time de tecnologia de um banco grande, em remoto com ida mensal ao escritório",
    "numa startup pequena de saúde, onde faz um pouco de tudo",
    "numa empresa de varejo, num time de e-commerce, em modelo híbrido",
    FREELANCER,
    "numa empresa de logística, mantendo um sistema legado enorme",
    "numa agência digital, fazendo sites e apps para campanhas de clientes",
    "num estúdio pequeno de games em Recife",
    "numa edtech que vende cursos online, em remoto",
    "numa operadora de telecom, num time de sistemas internos",
]

FORMACOES = [
    "se formou em Ciência da Computação numa federal",
    "fez Sistemas de Informação numa universidade particular",
    "começou em outra área e migrou para tecnologia com um bootcamp",
    "aprendeu por conta própria, com cursos online e projetos pessoais",
    "ainda está terminando a graduação enquanto trabalha",
    "fez curso técnico em informática e depois a faculdade",
    "começou Engenharia da Computação e largou no meio para trabalhar",
    "fez mestrado em Ciência da Computação antes de ir para o mercado",
    "veio de Engenharia Elétrica e foi parar em software",
    "fez Análise e Desenvolvimento de Sistemas num instituto federal",
    "fez uma faculdade a distância enquanto trabalhava em outra coisa",
    "estudou Design e foi migrando para programação",
]

CIDADES = [
    "mora no Recife, em Boa Viagem", "mora no Recife, nas Graças", "mora no Recife, na Torre",
    "mora em Olinda", "mora em Jaboatão", "mora em Caruaru e trabalha remoto",
    "mora em João Pessoa", "veio do interior e mora no Recife, em Casa Amarela",
    "mora em Paulista", "mora no Recife, na Várzea", "mora em Camaragibe",
    "mora em Natal e trabalha remoto",
]

ROTINAS = [
    "trabalha em sprints de duas semanas num time de oito pessoas espalhadas pelo Brasil",
    "entra em plantão de sobreaviso uma semana por mês e já perdeu noite de sono por alerta de madrugada",
    "passa boa parte do tempo revisando pull request dos colegas",
    "vive apagando incêndio em produção e mexendo em código que ninguém documentou",
    "trabalha de casa, com fone o dia inteiro e câmera desligada sempre que pode",
    "está estudando para trocar de emprego e faz entrevista técnica de vez em quando",
    "mentora os estagiários do time e escreve muita documentação",
    "está num time pequeno e também atende chamado de suporte",
    "passa metade da semana com o pessoal de produto definindo o que entra na próxima versão",
    "cuida da esteira de integração contínua e vive tentando deixar o build mais rápido",
    "está no meio da migração de um monolito antigo para serviços menores",
    "faz programação em par quase todo dia com alguém do time",
]

FERRAMENTAS = [
    "usa VS Code com Copilot ligado o tempo todo",
    "usa as IDEs da JetBrains e não troca por nada",
    "migrou para o Cursor e usa o chat do editor para quase tudo",
    "usa Neovim e tem orgulho da própria configuração",
    "usa assistente de IA no terminal para gerar teste e refatorar",
    "usa o editor que a empresa manda e não liga muito para isso",
    "usa Vim quando entra em servidor e VS Code no resto",
    "trocou para o Zed porque achou mais leve",
    "usa VS Code puro, sem nenhuma extensão de IA",
    "deixa o ChatGPT aberto numa aba ao lado em vez de usar plugin no editor",
    "não pode usar assistente de IA no editor por regra da empresa",
    "vive no terminal, com tmux e muitos atalhos próprios",
]

MIDIAS = [
    "lê Hacker News e newsletter de tecnologia no café da manhã",
    "acompanha o pessoal de tecnologia no X e no LinkedIn",
    "vê vídeo de programação no YouTube",
    "fica no Discord e no Reddit de programação, quase não lê notícia",
    "lê o TabNews e grupos de vagas no Telegram",
    "vê notícia quando alguém manda no Slack da empresa",
    "escuta podcast brasileiro de tecnologia no trânsito e quase não lê texto",
    "guarda newsletters gringas de engenharia para ler no fim de semana",
    "assiste live de programação na Twitch à noite",
    "lê os blogs de engenharia das empresas grandes de tecnologia",
    "quase não consome nada de tecnologia fora do trabalho",
    "participa de grupos de WhatsApp de comunidades de tecnologia de Recife",
]

OPINIOES = [
    "usa IA para quase tudo no trabalho e acha que quem não usa vai ficar para trás",
    "usa IA para tarefas chatas, mas revisa tudo porque já viu muito código errado gerado",
    "desconfia de IA e acha que está gerando uma geração de devs que não sabe depurar",
    "acha IA útil mas tem medo do que isso faz com as vagas de júnior",
    "não tem opinião muito formada, usa quando o prazo aperta",
    "usa IA só para escrever teste e documentação",
    "acha que IA no trabalho é mais propaganda do que ganho de produtividade",
    "passou a usar porque a empresa exigiu e ainda está se acostumando",
    "usa IA para estudar tecnologia nova, mas não para código que vai para produção",
    "tem receio de vazar código da empresa e evita colar coisa sensível",
    "acha que em poucos anos quase ninguém vai escrever código na mão",
    "usa todo dia mas não confia em nada que não testou",
]

ESTILOS = [
    "escreve tudo em minúsculas, quase sem pontuação, frases bem curtas",
    "escreve rápido e às vezes erra uma letra ou outra, usa 'kkkk' quando acha graça",
    "escreve certinho mas curto, sem enrolar",
    "mistura muito inglês no meio: 'deploy', 'subir pra prod', 'fazer o merge', 'tá buggado'",
    "responde com preguiça, às vezes só duas ou três palavras",
    "abrevia muito: 'vc', 'tb', 'pq', 'q', 'mto'",
    "escreve frases compridas, emendando uma ideia na outra com vírgula",
    "põe um emoji no fim de quase toda frase",
    "escreve meio formal, como se fosse e-mail de trabalho",
    "usa muito 'tipo' e 'aí' no meio das frases",
    "escreve seco, com maiúscula e ponto final, sem simpatia",
    "responde com ironia e uma piadinha sempre que pode",
]

# Um traço fora do trabalho, para cada agente ter uma vida própria e as respostas
# não convergirem para a mesma história.
PARTICULARIDADES = [
    "tem um filho pequeno e trabalha com a rotina da creche",
    "toca baixo numa banda de amigos nos fins de semana",
    "está fazendo pós em segurança da informação à noite",
    "voltou há pouco de uma licença médica",
    "joga vôlei de praia em Boa Viagem aos sábados",
    "cuida da avó e mora com ela",
    "está planejando se mudar para Portugal",
    "corre de manhã cedo e está treinando para uma meia maratona",
    "faz faculdade de Psicologia em paralelo, por curiosidade",
    "tem três gatos resgatados",
    "é a primeira pessoa da família a trabalhar com tecnologia",
    "trabalhou dois anos num call center antes de virar dev",
]


def _distribuir(rng: random.Random, opcoes: list, n: int) -> list:
    """Embaralha e entrega um item diferente por agente; só repete se faltar item."""
    embaralhadas = rng.sample(opcoes, k=len(opcoes))
    return [embaralhadas[i % len(embaralhadas)] for i in range(n)]


def gerar_personas(n: int, semente: int | None = None) -> list[Persona]:
    rng = random.Random(semente)
    tracos = {
        "nome": _distribuir(rng, NOMES, n),
        "cargo": _distribuir(rng, CARGOS, n),
        "stack": _distribuir(rng, STACKS, n),
        "empresa": _distribuir(rng, EMPRESAS, n),
        "formacao": _distribuir(rng, FORMACOES, n),
        "cidade": _distribuir(rng, CIDADES, n),
        "rotina": _distribuir(rng, ROTINAS, n),
        "ferramenta": _distribuir(rng, FERRAMENTAS, n),
        "midia": _distribuir(rng, MIDIAS, n),
        "opiniao": _distribuir(rng, OPINIOES, n),
        "estilo": _distribuir(rng, ESTILOS, n),
        "particularidade": _distribuir(rng, PARTICULARIDADES, n),
    }
    _resolver_conflitos(tracos, n)
    return [_persona(rng, {chave: valores[i] for chave, valores in tracos.items()}) for i in range(n)]


# Combinações que não fazem sentido com o cargo: (traço, valor, cargos em que é proibido).
CONFLITOS = [
    ("empresa", FREELANCER, ("estágio", "tech lead")),  # freelancer não lidera nem estagia
    ("rotina", "mentora os estagiários do time e escreve muita documentação", ("estágio", "júnior")),
    ("formacao", "fez mestrado em Ciência da Computação antes de ir para o mercado", ("estágio",)),
    ("formacao", "ainda está terminando a graduação enquanto trabalha", ("sênior", "tech lead")),
]


def _proibido(traco: str, valor, cargo: str) -> bool:
    return any(t == traco and v == valor and any(c in cargo for c in cargos) for t, v, cargos in CONFLITOS)


def _resolver_conflitos(tracos: dict, n: int) -> None:
    """Troca o traço incoerente com o de outro agente, sem criar repetição nem novo conflito."""
    cargo = lambda k: tracos["cargo"][k][0]
    for traco, *_ in CONFLITOS:
        valores = tracos[traco]
        for i in range(n):
            if not _proibido(traco, valores[i], cargo(i)):
                continue
            j = next(
                (j for j in range(n) if j != i
                 and not _proibido(traco, valores[i], cargo(j))
                 and not _proibido(traco, valores[j], cargo(i))),
                None,
            )
            if j is not None:
                valores[i], valores[j] = valores[j], valores[i]
            else:
                lista = {"empresa": EMPRESAS, "rotina": ROTINAS, "formacao": FORMACOES}[traco]
                valores[i] = next(v for v in lista if v not in valores and not _proibido(traco, v, cargo(i)))


def _persona(rng: random.Random, t: dict) -> Persona:
    nome, genero = t["nome"]
    cargo, (idade_min, idade_max), (anos_min, anos_max) = t["cargo"]
    idade = rng.randint(idade_min, idade_max)
    anos = min(rng.randint(anos_min, anos_max), idade - 18)
    experiencia = (
        "começou a trabalhar com isso este ano"
        if anos == 0
        else f"trabalha com desenvolvimento há {anos} ano{'s' if anos > 1 else ''}"
    )

    texto = (
        f"Seu nome é {nome}, {genero}, {idade} anos. Você {cargo} e trabalha com {t['stack']}, "
        f"{t['empresa']}. Você {experiencia}. Você {t['formacao']}. Você {t['cidade']}. "
        f"No dia a dia, você {t['rotina']}. Você {t['ferramenta']}. "
        f"Sobre mídia: você {t['midia']}. Sobre IA no trabalho: você {t['opiniao']}. "
        f"Fora do trabalho, você {t['particularidade']}. "
        f"Seu jeito de escrever no celular: você {t['estilo']}. "
        "Invente detalhes da sua vida e do seu trabalho quando precisar, mas mantenha tudo "
        "coerente com esta descrição."
    )
    resumo = f"{idade} anos, {cargo.removeprefix('é ')}, {t['stack']}; {t['empresa']}"
    return Persona(nome=nome, resumo=resumo, texto=texto)
