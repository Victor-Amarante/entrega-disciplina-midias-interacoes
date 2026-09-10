# Diretrizes da Entrega 2 — o critério escrito, e por quê

> **Como este documento foi produzido.** É o item 4 no formato "diretrizes": os
> cortes duros, os critérios de interesse, a regra de desempate e o que o
> critério deixou passar.
>
> A **estrutura e a redação** são da IA. A **substância de cada decisão é minha**:
> cada bloco abaixo parte de uma escolha que eu fiz explicitamente, entre
> alternativas que a IA colocou na mesa com as consequências declaradas *antes*
> da escolha. Onde eu não tinha dado o motivo, ela se recusou a inventar e
> perguntou — as respostas dessas perguntas são o que está redigido aqui.
>
> Esta entrega é a segunda metade de um mesmo trabalho. A Entrega 1 varreu o
> mesmo tema pelo outro lado, e o registro dela está em
> `atividade-1/entrega/registro-de-decisoes.md`.

CIN0055 · Tendências em Mídia e Interação · CIn/UFPE · 2026.2
Aluno: Victor Amarante · Modo declarado: **MODO 3** (IA executa, aluno orquestra)

---

## D0 · A espinha: as duas entregas são o mesmo tema por lados opostos

A Entrega 1 respondeu **"onde eu vou olhar comportamento emergente"**. A
Entrega 2 responde **"com o que eu vou construir para gerar esse
comportamento"**. A primeira é a pergunta do pesquisador, a segunda é a do
engenheiro — e eu quero ser os dois.

Isso não é arranjo retórico feito depois: é verificável no dado. O critério
eliminatório que eu escolhi na Entrega 1 — **"não se abre e usa"** — rejeitou
5.238 candidatos com motivos como *"repositório sem homepage, nada para abrir e
usar (é Entrega 2)"*. Desses, **2.455 foram herdados literalmente para esta
entrega**, sem uma única requisição nova, reaplicando a mesma função `eliminar()`
que rodou lá.

Um critério vago não serviria de dobradiça entre duas entregas. Este serviu.

---

## D1 · Recorte

**Escolhido:** o mesmo tema, invertido. Simulação com agentes de IA como
**código** — framework de modelagem baseada em agentes, ambiente de aprendizado
por reforço multiagente, orquestração de agentes, memória e estado, trace como
SDK, motor de personagem não jogável.

**Alternativas recusadas:** alargar para "infraestrutura de agentes" em geral
(diluiria o tema e me faria disputar as mesmas bibliotecas famosas que a turma
inteira vai pegar) e trocar de eixo (jogaria fora o reaproveitamento e a
narrativa entre as duas entregas).

---

## D2 · Critérios eliminatórios

| # | critério | como é decidido |
|---|---|---|
| **E1** | não dá para instalar ou importar | prova concreta: publicado em registro de pacote, ou comando de instalação encontrado no README (`pip install`, `cargo add`, `npm i`, `go get`, …) |
| **E3** | sem licença aberta declarada | campo do registro ou da API do GitHub; URL de licença é resolvida pelo endereço, nome de arquivo (`LICENSE`) **não** conta |
| **E4** | invólucro fino sem substância | **não decidível por máquina** — vira suspeita marcada e conferência de leitura |

E1 é o espelho exato do meu critério da Entrega 1 e é o que garante que eu
entregue a categoria certa. E4 fica como suspeita porque nenhuma regra distingue
casca fina de abstração legítima; o número de marcados está no relatório de
julgamento.

**Resultado medido:** 754 reprovados em E1 e cerca de 300 em E3, no julgamento
sobre o texto real — depois de 3.914 já terem caído por licença na peneira
mecânica.

### Por que recusei "projeto morto ou arquivado"

Recusei nas **duas** entregas, e é uma escolha incomum, então registro o
argumento: **data não mede relevância.** O que me interessa é a ideia
implementada, não o suporte. O *Generative Agents* de 2023 está parado e
continua sendo o trabalho que originou este campo inteiro; o **WarAgent**, que
está nas minhas 500, é código de artigo que roda simulação de guerras mundiais
com países representados por agentes — reprovar por inatividade seria reprovar
exatamente aquilo que eu quero apresentar.

A IA argumentou contra, e o argumento dela é bom: para biblioteca o cálculo
inverte, porque código parado quebra na primeira dependência incompatível.
Mantive assim mesmo, e **assumo o custo**: vai ter item na lista que não compila
hoje, e conferir isso é trabalho meu na hora de fixar as 50.

### Por que aceitei o custo do critério de licença

Código público sem licença declarada é, juridicamente, *todos os direitos
reservados* — eu não posso importar no meu projeto. Como esta entrega é
justamente sobre o que eu chamaria de **dentro do meu código**, licença não é
detalhe burocrático: é a condição de uso.

Aceito perder código acadêmico bom por isso, e sei que perdi — a IA me avisou
do custo antes de eu escolher, e o número final (mais de 4.200 eliminados por
licença ao todo) confirma que o aviso estava certo.

---

## D3 · Critérios positivos e seus pesos

| critério | peso | o que ele garante |
|---|---|---|
| **P1** modela múltiplos agentes se afetando | **3,0** | é o que faz ser **sociedade**, e não um agente sozinho |
| **P2** expõe o estado por dentro (hooks, trace, replay, serialização) | 2,0 | sem isso não dá para **analisar** o emergente, só assistir |
| **P3** ambiente e regras definidos por código | 2,0 | é o **controlado**: se eu não mexo nas regras, não é experimento |
| **P4** reprodutível e mensurável (semente, determinismo, métrica) | 1,5 | é o **testar possibilidades**: sem dado saindo, não comparo duas rodadas |

São os mesmos quatro da Entrega 1, traduzidos de "o que a ferramenta mostra"
para "o que a biblioteca expõe ao programador". Não são critérios soltos: são as
quatro condições da frase que eu escrevi antes de qualquer varredura começar —
colocar uma sociedade simulada de agentes num ambiente controlado, simular
possibilidades e analisar o comportamento emergente.

**Sobre os pesos:** eles foram propostos pela IA e ficaram pendentes durante as
duas entregas até eu decidir. **Mantenho como estão, e a ordem passa a ser
minha:** multiagente pesa mais porque é a condição de existência do tema — sem
vários agentes se afetando, os outros três critérios não têm sobre o que
incidir. Os demais entram como qualificadores.

---

## D4 · Desempate: popularidade, agora medida por download

Mantive popularidade, como na Entrega 1, mas aqui com um instrumento melhor:
registro de pacote tem **contagem de download**, e download mede uso, enquanto
estrela de repositório mede aprovação. É o mesmo critério meu, medido de forma
mais honesta.

O risco que assumo é o mesmo de lá: as 50 são exclusivas na turma, e
popularidade é o desempate mais provável dos meus colegas. O plano B também é o
mesmo — o ranking inteiro está gerado, então descer na fila é barato.

_(Alternativas oferecidas e recusadas: manutenção recente e raridade. Ficam
registradas porque a decisão foi tomada sabendo delas.)_

---

## D5 · Fontes, e as que eu não varri

Todas as fontes candidatas foram **sondadas antes** de virar código — uma única
requisição a cada uma, para não construir adaptador em cima de suposição. O
resultado está em `entrega/anexo-tecnico-fontes.md`, com método e viés de cada
uma. O resumo das que ficaram de fora:

| fonte | por quê |
|---|---|
| **PyPI (busca)** | `pypi.org/search/` devolve desafio JavaScript. **Não contornei** — mesma decisão que tomei na Entrega 1 com theresanaiforthat e toolify. Mas o PyPI **foi** varrido pelo sitemap, que o próprio `robots.txt` publica: 257 arquivos, ~2 milhões de projetos, filtrados por token do slug. |
| **Papers with Code** | a API devolve HTML em vez de JSON: está desativada. |
| **libraries.io** | exige chave (401). |
| **pkg.go.dev** | `robots.txt` proíbe `/search?*`. Sobraria o sitemap e eu não fiz — **buraco declarado, não resolvido**. |
| **ecosyste.ms** | `ConnectTimeout` em todas as chamadas a partir desta rede. |
| **OpenAlex** | funciona, foi testada e eu **descartei de propósito**: devolve artigo científico, e artigo reprova no meu próprio E1. |
| **Reddit** | `robots.txt` proíbe coleta de todo o site, como já medido na Entrega 1. |

> **Sobre a exceção do arXiv:** na Entrega 1 eu autorizei usar a API oficial do
> arXiv apesar do `Disallow: /` no `robots.txt`, porque os Termos de Uso da
> própria API autorizam acesso programático. O critério que eu aplico é
> **respeitar a vontade declarada do serviço**, e no documento mais específico
> — os Termos da API — a vontade era "colete assim, nesse ritmo". Aqui o arXiv
> nem entrou, porque artigo reprova em E1.

---

## D6 · Regras de deduplicação (precisam ser defendidas)

**Herdada da Entrega 1, com uma extensão:** os registros de pacote entraram na
regra. Lá, `pypi.org` e `npmjs.com` eram domínio de publicação e caíam fora
inteiros — não eram ferramenta. Aqui cada pacote **é** uma ferramenta, e sem a
extensão os milhares de pacotes de um registro colapsariam numa chave só.

Isso é exatamente o bug que custou 7.774 candidatos na Entrega 1 — desta vez
**previsto em vez de descoberto**. Incluindo o caso do pacote com escopo do npm,
que precisa de profundidade 3: sem isso, `@langchain/core` e `@langchain/openai`
virariam a mesma chave.

**Nova nesta entrega — colapso de família.** Duas entradas que apontam para o
**mesmo repositório** são o mesmo **projeto**. Fica o pacote com mais downloads
(meu desempate); em empate, o de nome mais curto, que costuma ser o principal e
não o módulo satélite. Os irmãos não somem: ficam listados em `pacotes_irmaos`.

Sem esta regra, **142 das 500 vagas iriam para subpacote redundante** — 28% da
lista. `microsoft/autogen` aparecia com 9 pacotes, `ascending-ai/lash` com 12,
`autoagents` com 5, todos com README idêntico.

---

## D7 · O que a IA achou conferindo, e que mudou a lista

Registro porque o processo é o que está sendo avaliado, e porque em todos os
casos o defeito apareceu **olhando o resultado**, não lendo o código.

| # | o que apareceu | efeito |
|---|---|---|
| 1 | **O topo do pool estava tomado por DevOps** — `sensu-plugins-docker-swarm`, `puma-plugin-telemetry`. Monitoramento de infraestrutura compartilha quase todo o vocabulário do meu tema: "swarm" é Docker Swarm, "agent" é agente de monitoramento, "orchestration" é Kubernetes. | Criado um **portão de relevância** exigindo sinal forte do tema. Não é critério novo: é o meu P1 sendo aplicado de verdade, já que casar a palavra "swarm" não é evidência de agentes se afetando. Dos 54.013 sobreviventes, 7.139 passaram. |
| 2 | **O enriquecimento não tratava PyPI nem NuGet.** Os ~300 itens desses dois reprovariam em E3 por defeito do código, não pelo meu critério. | Corrigido: PyPI por `pypi.org/pypi/<nome>/json` (licença vinda do classificador, porque o campo `license` vem vazio nos pacotes modernos) e NuGet pelo `.nuspec`. |
| 3 | **Licença declarada como URL ou nome de arquivo.** | URL é resolvida pelo endereço; `LICENSE` **não** conta como licença aberta declarada, porque não diz qual licença é. |
| 4 | **398 das 500 saíam como "Não classificado"**, porque registro de pacote não tem campo de categoria. | Classificador por texto real, com prioridade declarada — simulação social ganha de observabilidade quando as duas casam, porque a primeira é o núcleo do recorte. Sobraram 28. |

O padrão é o mesmo que eu já tinha registrado na Entrega 1: **o total agregado
não é verificação, é conforto.** Verificação é a decomposição por fonte e a
leitura dos 20 primeiros do ranking. Foi assim que os quatro apareceram.

---

## D8 · O que eu sei que a minha lista não tem

- **Python está sub-representado** em relação ao que ele significa no tema. A
  busca do PyPI está bloqueada, e a via do sitemap seleciona **pelo nome do
  pacote e mais nada** — uma biblioteca de simulação chamada "Orion" não aparece
  por caminho nenhum.
- **Go quase não aparece**, porque `pkg.go.dev` proíbe busca no `robots.txt`.
- **Maven, CocoaPods, pub.dev e Hex não foram varridos** por escolha de escopo.
- **Código de pesquisa sem licença ficou fora** — decisão minha, custo assumido
  em D2.
- **A varredura vê o que o vocabulário deixa ver.** São 35 frases, 50 termos
  curtos e 21 tópicos do GitHub, em `garimpo/consultas.py`. O que não está lá
  não existe nesta lista.

---

## As sete perguntas do enunciado

| # | pergunta | onde está respondida |
|---|---|---|
| 1 | quais fontes, e o que cada uma NÃO mostra | `entrega/anexo-tecnico-fontes.md` — método e viés medidos, fonte por fonte |
| 2 | o que reprova na hora | D2 — E1, E3 e E4, com os números de cada um |
| 3 | o que conta como interessante, em regra | D3 — P1 a P4 e os pesos, agora assumidos por mim |
| 4 | o que decide o empate | D4 — popularidade por download, com o risco declarado |
| 5 | como sabe que o link existe | o enriquecimento abre a API de cada registro e o README de cada repositório; status e prova de instalação ficam gravados por item |
| 6 | que ferramenta boa o seu critério derruba | D2 (licença e projeto morto) e `dados/relatorio_peneira.md`, seção "Amostra do que o SEU critério derrubou" |
| 7 | por que essas 50 e não outras | **só eu posso responder** — e a resposta começa em D0: são as que sobrevivem a "instala, tem licença aberta, e modela agentes que se afetam de um jeito que eu consigo inspecionar e repetir" |
