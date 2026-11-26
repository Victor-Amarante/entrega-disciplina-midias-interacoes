# Caça ao respondente sintético

*CIN0055 · Tendências em Mídia e Interação · 2026.2 · Movimento 3 · vafs*

Experimento derivado da ideia 2 de [`../ideias-sociedades-simuladas.md`](../ideias-sociedades-simuladas.md),
que testa as disrupções D3 e os efeitos e5 e e6 do mapa
[`../tendencia-sociedades-simuladas.md`](../tendencia-sociedades-simuladas.md).

**Link:** https://caca-respondente.onrender.com/ (para criar uma sala: https://caca-respondente.onrender.com/host/)

O servidor gratuito dorme quando ninguém usa; o primeiro acesso pode levar cerca de um minuto.

## O que é

Um jogo de *red team* sobre pesquisa online, jogado pelo celular. A turma escreve perguntas-armadilha
para pegar bots. Essas perguntas viram um questionário que a turma responde ao mesmo tempo que alguns
agentes de IA com persona de desenvolvedor de software; metade deles pode pesquisar na web antes de responder. Depois,
cada pessoa recebe cartões anônimos com as respostas de alguém, humano ou agente, e dá o veredito: gente
ou máquina. O placar mostra qual armadilha pegou mais agentes e quantos humanos foram acusados por engano.

## A pergunta sobre o futuro

Quando uma resposta coerente deixar de provar que há um humano do outro lado, o que ainda distingue gente
de máquina numa pesquisa? E quanto custa virar um resultado?

## Tecnologia emergente

Respondentes sintéticos autônomos baseados em LLM, como o agente de Westwood (PNAS, 2025), que passou em 99,8%
das checagens de atenção. Cada agente aqui recebe uma persona longa e concreta de desenvolvedor de software (cargo, stack, empresa, rotina, ferramentas) e a instrução
de parecer humano. A persona é de dev, e não de aluno, porque fica mais perto da realidade da turma e porque o ofício é bem documentado, então o modelo já sabe o que precisa para sustentá-la.
Todos os agentes rodam num modelo *abliterated*, o `abliterated-model-large-v2` do
[abliteration.ai](https://abliteration.ai/), um GLM-5.3 aberto em que o comportamento de recusa foi removido dos
pesos. A ideia é ver se, sem a camada de ajuste de segurança, o agente escreve com a variação e a falta de filtro
de uma pessoa. Os agentes não pesquisam na web. Para trocar de modelo, use `ABLIT_MODELO`. Na primeira rodada, em
4 de novembro, os agentes rodavam no Claude Haiku, metade com busca na web.

**Por que não dá com tecnologia madura.** Os bots de formulário que existiam até pouco tempo atrás
(scripts, preenchimento aleatório, respostas copiadas) caem justamente nas checagens de atenção e nas
perguntas abertas, e era isso que os denunciava. O experimento só faz sentido porque agora existe um
respondente que lê uma pergunta inédita, escrita minutos antes pela turma, e responde em linguagem natural,
no estilo de uma persona. As defesas contra isso ainda estão sendo inventadas.

## Como usar

### Para quem joga (celular)

1. Abra o link ou leia o QR code no telão.
2. Escolha um apelido.
3. **Armadilhas:** escreva até duas perguntas que gente e máquina conseguem responder igualmente, para a pista
   vir do jeito de responder: uma pegadinha boba (quantas letras "a" tem em "abacate"?), uma opinião sem filtro
   ou uma experiência vivida. Perguntas sobre o que aconteceu na sala, ou que precisem de pesquisa na internet
   (lugares do Recife, por exemplo), ficaram de fora: a máquina não tem como saber e a caçada fica fácil demais.
4. **Questionário:** responda às perguntas como você mesmo.
5. **Caçada:** para cada cartão, toque na resposta que te deu a pista (se houver) e escolha *Humano* ou
   *Máquina*.
6. **Placar:** veja quantos você acertou, o que você disse em cada cartão, quem era quem e a pista que marcou.

### Para quem apresenta (projetor)

1. Abra o link e clique em **Criar uma sala**. Ajuste quantos agentes entram e quantas perguntas
   vão para o questionário.
2. O painel abre com o QR code. Projete-o.
3. Avance as fases pelo botão no canto superior direito. Na fase de armadilhas, marque quais entram no
   questionário, ou deixe o sorteio escolher. Duas perguntas são fixas: uma genérica e uma checagem de
   atenção, para servir de comparação.
4. Ao abrir o questionário, os agentes começam a responder em segundo plano. Espere todos ficarem prontos
   (✓) antes de abrir a caçada. Se algum der erro, clique em *Tentar de novo*.
5. No placar, o telão resume o resultado em frases, mostra onde caiu cada veredito (agente pego, agente que
   passou, humano acusado, humano reconhecido), quais perguntas entregaram a máquina e uma grade com o veredito
   de cada jogador em cada cartão, para conferir o placar.
6. Ao final, clique em **⬇ Dados** para baixar tudo o que aconteceu na sala (armadilhas, respostas,
   personas, vereditos com a pista marcada), em JSON e sem os tokens de acesso.

O painel só funciona no navegador em que a sala foi criada.

### Rodar localmente

Requisitos: Python 3.12 com [uv](https://docs.astral.sh/uv/) e Node 22.

```bash
# backend (porta 8000)
cd backend
cp .env.example .env   # cole a sua ABLITERATION_API_KEY no .env; sem ela, roda em modo simulado
uv run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# frontend (porta 3000), em outro terminal
cd frontend
npm install
npm run dev
```

Abra `http://localhost:3000`. Celulares na mesma rede Wi-Fi entram por `http://<ip-da-máquina>:3000`.

### Colocar no ar (um link só)

O `Dockerfile` desta pasta gera uma imagem com o site e a API juntos.

```bash
docker build -t caca-respondente .
docker run -p 8000:8000 --env-file backend/.env caca-respondente
```

Para ter um link público, sirva a imagem em qualquer serviço que rode Docker. No Render: *New → Web Service*,
aponte para o repositório, defina *Root Directory* como `atividade-3/src`, escolha *Docker* e acrescente as
variável `ABLITERATION_API_KEY`. No plano gratuito o serviço dorme sem uso e as salas se perdem quando ele
reinicia; abra o link alguns minutos antes da aula.

Para um teste rápido sem deploy: rode o container e exponha a porta com `ngrok http 8000`.

### Variáveis de ambiente

| Variável | Padrão | Para quê |
|---|---|---|
| `ABLITERATION_API_KEY` | — | Chave do [abliteration.ai](https://abliteration.ai/console), começando com `ak_`. Localmente, vai em `backend/.env` (fora do git); no deploy, nas variáveis do serviço. Sem ela, os agentes respondem com frases prontas. |
| `ABLIT_MODELO` | `abliterated-model-large-v2` | Modelo dos agentes (GLM-5.3, US$ 3 / US$ 5 por milhão de tokens). Também há `abliterated-model` e `abliterated-model-large-flash`, mais baratos. |
| `ABLIT_TEMPERATURA` | `1` | Temperatura do modelo. |
| `ESFORCO` | `low` | Esforço de raciocínio (`low` a `max`). Baixo deixa os agentes rápidos. |
| `ABLIT_URL` | `https://api.abliteration.ai/v1` | Qualquer API compatível com a da OpenAI serve (um Ollama local, por exemplo). |
| `AGENTES_SIMULTANEOS` | `6` | Quantos agentes chamam a API ao mesmo tempo. |
| `PASTA_DADOS` | `backend/dados` | Onde cada sala é salva em JSON. |

## Como o código está organizado

```
src/
├── Dockerfile
├── backend/                 FastAPI
│   └── app/
│       ├── main.py          rotas e site estático
│       ├── config.py
│       ├── armazenamento.py salas em memória + JSON
│       ├── dominio/         modelos do estado da sala
│       ├── api/             rotas do participante e do apresentador
│       └── servicos/        regras do jogo, agentes, personas, placar
└── frontend/                Next.js (exportado como site estático)
    ├── app/                 páginas: início, sala, criar sala, painel
    ├── components/
    │   ├── participante/    telas do celular, uma por fase
    │   ├── painel/          telas do projetor, uma por fase
    │   └── ui/
    └── lib/                 cliente da API, tipos, polling
```

## O que espero que aconteça

Escrito antes do teste, para ser confrontado no `REGISTRO.md`.

- **Detecção perto do acaso** nas perguntas genéricas e na checagem de atenção: o agente passa.
- **Detecção acima do acaso** nas perguntas de contexto local e de experiência vivida. É a hipótese mais
  interessante: a defesa que sobra seria o contexto, não a lógica. Se os agentes com busca também passarem
  nessas perguntas, nem essa defesa sobra.
- **Falsos positivos.** Humanos acusados de ser máquina por responderem certinho ou curto demais. É, em
  pequena escala, o custo de exclusão que a verificação forte cria (e5.1).
- **Poucas respostas falsas viram a enquete**, a um custo de centavos. O número exato depende da turma, e é
  o dado que a turma leva para casa.
- **O que me faria mudar de ideia:** a turma identificar os agentes bem acima do acaso mesmo nas perguntas
  genéricas. Nesse caso, e5 está superestimado, pelo menos para respostas abertas.
