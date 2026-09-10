# Anexo técnico — fontes varridas, viés e números medidos

> **Como este arquivo foi produzido.** Gerado por `relatar.py` a partir de
> `dados/log_bruto.jsonl` e `dados/candidatos.jsonl`. Todo número aqui foi
> medido, nenhum foi estimado. O texto de viés de cada fonte está declarado
> na constante `VIES` dentro do adaptador correspondente em
> `coletor/fontes/`, e é a leitura do coletor — o julgamento sobre aceitar
> ou não esse recorte é do aluno e não está neste arquivo.

Gerado em 2026-09-03T07:35:26-03:00

## Números da varredura

- itens brutos colhidos (antes da deduplicação): **38196**
- requisições HTTP feitas: **572**
- candidatos únicos após deduplicação: **18044**
- candidatos vistos em mais de uma fonte: **0**

### Requisições por host

| host | requisições |
|---|---|
| `huggingface.co` | 170 |
| `hn.algolia.com` | 127 |
| `www.aixploria.com` | 92 |
| `itch.io` | 67 |
| `api.github.com` | 64 |
| `export.arxiv.org` | 44 |
| `futuretools.io` | 6 |
| `www.producthunt.com` | 2 |

### Códigos de resposta

| status | ocorrências |
|---|---|
| 200 | 570 |
| 429 | 2 |

_status -1 = falha de rede/timeout; 999 = requisição não feita por robots.txt._

### Itens brutos por fonte

| fonte | itens brutos | candidatos únicos |
|---|---|---|
| arxiv | 52 | 52 |
| arxiv:projeto | 0 | 5 |
| diretorios | 15552 | 0 |
| diretorios:aixploria | 0 | 4776 |
| diretorios:futuretools | 0 | 3000 |
| github | 5744 | 2729 |
| hn | 1234 | 472 |
| huggingface:paper | 9660 | 2705 |
| huggingface:space | 3695 | 3481 |
| itchio | 2159 | 774 |
| producthunt | 100 | 50 |

### Candidatos por faceta do vocabulário

A faceta vem de `coletor/consultas.py`. Faceta com número baixo significa
que o vocabulário daquele recorte rendeu pouco — pode ser que o assunto
seja raro, ou que os termos estejam errados. As duas hipóteses são do aluno.

| faceta | candidatos |
|---|---|
| amplo_comercial | 7776 |
| sandbox_ambiente | 4142 |
| ? | 2729 |
| npc_jogos | 1083 |
| sociedade_simulada | 568 |
| observabilidade_replay | 500 |
| usuarios_sinteticos | 424 |
| avaliacao_arena | 316 |
| robotica_mundo | 184 |
| abm_classico | 138 |
| economia_negociacao | 134 |
| amostra_de_contraste | 50 |

## Viés declarado de cada fonte

Cada bloco abaixo é o texto da constante `VIES` do adaptador — ou seja,
o que aquela fonte **sistematicamente não mostra**.

### hn

**Rendimento medido:** 1234 itens brutos → 472 candidatos únicos.

**Como foi varrida.** API de busca do Algolia (`hn.algolia.com/api/v1/search`), sem chave e sem cadastro. 41 termos frasais do vocabulário, até 5 páginas de 100 resultados cada, filtrando `tags=story`. O item colhido é a URL EXTERNA que a pessoa postou, não a página da discussão. Descarta 24 domínios de agregador e rede social, que dominam qualquer busca do HN sem serem ferramenta.

**Viés — o que esta fonte sistematicamente NÃO mostra.** Bolha do Vale do Silício e anglófona. Premia lançamento sobre maturidade: ferramenta boa de 2021 que nunca foi postada simplesmente não existe aqui. O mesmo produto reaparece em vários posts, e post com muito voto costuma ser polêmica, não qualidade. Não indexa nada que não tenha sido submetido por um humano.

### huggingface

**Rendimento medido:** 13355 itens brutos → 6186 candidatos únicos.

**Como foi varrida.** API oficial, sem chave. **Spaces**: `api/spaces?search=` com 44 termos CURTOS — a busca do HF casa substring do identificador, não frase, e o vocabulário frasal rendia 3 itens em 41 consultas. **Papers**: `api/papers/search?q=` com os 41 termos frasais, que aí funcionam. Na verificação, cada Space é reconsultado em `api/spaces/<id>`, que devolve `runtime.stage` (RUNNING / SLEEPING / erro de build) — sinal de vida melhor do que um GET na página, que responde 200 até para Space quebrado.

**Viés — o que esta fonte sistematicamente NÃO mostra.** Só existe o que é aberto e hospedado na própria HF. Todo produto comercial fechado — que é a maioria do que 'se abre e usa' — é invisível aqui. Spaces morrem: muitos ficam em 'Sleeping' ou com build quebrado e a API não diferencia isso de um app vivo. Enviesado para demo de pesquisa em Gradio.

### github

**Rendimento medido:** 5744 itens brutos → 2729 candidatos únicos.

**Como foi varrida.** Search API autenticada por token pessoal (30 requisições/minuto contra 10 sem token). 8 consultas × até 5 páginas de 100, ordenadas por estrelas; a API limita a 1000 resultados por consulta. O truque que faz esta fonte servir à Entrega 1: colhe o campo `homepage` do repositório, que costuma apontar para o app hospedado. Sem homepage, o item é marcado `so_repo` e reprovado no critério E1.

**Viés — o que esta fonte sistematicamente NÃO mostra.** Só código aberto e só o que está no GitHub. Mede popularidade de desenvolvedor (estrela), não utilidade para quem usa: repositório de tutorial com 30 mil estrelas empata com ferramenta real. Repositório arquivado e abandonado aparece igual a projeto ativo se não olhar a data. Por natureza puxa para Entrega 2, não para Entrega 1.

### diretorios

**Rendimento medido:** 15552 itens brutos → 7776 candidatos únicos.

**Como foi varrida.** Sitemap XML em vez de raspar páginas de listagem: é a via que o próprio site publica para ser percorrido, custa 3 requisições em vez de 300 e não depende de seletor de HTML que quebra na próxima reforma de layout. futuretools: `tools-1..3.xml` (~3.000 URLs). aixploria: índice mensal com 48 sub-sitemaps. O nome sai do slug da URL; a descrição não vem no sitemap e só aparece no enriquecimento.

**Viés — o que esta fonte sistematicamente NÃO mostra.** Diretório vive de tráfego e de listagem paga, então infla wrapper genérico de GPT e SaaS de marketing, e quase nunca remove link morto. Ordena por quem paga ou por quem submeteu, nunca por qualidade. Praticamente não tem ferramenta de pesquisa, acadêmica ou de nicho técnico — o que é exatamente onde simulação de agentes vive. Cobertura enviesada para produto comercial em inglês. Além disso, dois dos maiores (theresanaiforthat, toolify) bloqueiam coleta automatizada com Cloudflare: o recorte comercial que sobra é o dos sites que deixam passar, não o do mercado.

### itchio

**Rendimento medido:** 2159 itens brutos → 774 candidatos únicos.

**Como foi varrida.** Única raspagem de HTML de verdade do conjunto — não há API pública de navegação e o `robots.txt` proíbe `/search`. As páginas `/games/tag-<tag>` não estão na lista de Disallow, então são a via permitida: 8 tags × até 5 páginas de 36 itens, com os seletores `div.game_cell` > `a.title` / `div.game_text` / `div.game_author a`, conferidos na página real antes de escrever o adaptador. Frágil por natureza: se o layout mudar, o coletor emite `sem_itens` em vez de colher em silêncio.

**Viés — o que esta fonte sistematicamente NÃO mostra.** É catálogo de jogo indie, não de ferramenta. Traz mundo simulado e experimento de comportamento emergente que nenhuma outra fonte tem, mas quase nada aqui é 'ferramenta que se usa para trabalhar' — é obra para jogar. A ordenação padrão premia o que é popular e recente na plataforma, e jogo bom sem tag correta simplesmente não aparece, porque a navegação depende do autor ter marcado.

### arxiv

**Rendimento medido:** 52 itens brutos → 57 candidatos únicos.

**Como foi varrida.** API oficial `export.arxiv.org/api/query`, 41 termos entre aspas, até 2 páginas de 100. Além do paper, extrai por expressão regular as URLs de projeto/demo que os autores colam no resumo, ignorando domínios de publicação — é por aí que trabalho de pesquisa vira algo que se abre no navegador. **RESULTADO REAL: praticamente nada.** 65 requisições, 39 respostas 429, 25 falhas de rede e 1 sucesso, mesmo com 12 s entre chamadas (a documentação pede 3 s). O IP ficou limitado e a fonte foi abandonada. O adaptador funciona; o servidor é que não deixou.

**Viés — o que esta fonte sistematicamente NÃO mostra.** Só mostra o que virou publicação. Protótipo comercial, app fechado e produto de empresa não aparecem nunca. A data diz quando o paper saiu, não se o projeto está vivo — muita coisa aqui é código que rodou uma vez para a figura 4. Enviesado para inglês e para instituição com verba de publicação.

### reddit — **NÃO VARRIDA**

**Motivo de não ter sido varrida:** reddit.com/robots.txt: 'User-agent: * / Disallow: /'. Coleta automatizada proibida pelo próprio site; a API oficial exige OAuth. Fonte não varrida.

**Rendimento medido:** 0 itens brutos → 0 candidatos únicos.

**Como foi varrida.** NÃO VARRIDO. O adaptador está escrito e testado — usaria o feed `search.rss` por subreddit (o endpoint `.json` devolve 403 sem OAuth), 10 subreddits × 9 termos, extraindo os links externos citados no corpo dos posts. Ficou desativado ao ler o `robots.txt`, que proíbe coleta automatizada do site inteiro.

**Viés — o que esta fonte sistematicamente NÃO mostra.** Mede o que dá assunto em fórum, não o que é bom: post engraçado e drama sobem, ferramenta útil e discreta some. Cada subreddit tem sua igreja (r/LocalLLaMA só enxerga modelo local, r/gamedev só enxerga jogo). A busca por RSS devolve poucos itens por consulta e não pagina de verdade, então esta fonte é rasa por construção — serve de complemento, não de base.

### producthunt

**Rendimento medido:** 100 itens brutos → 50 candidatos únicos.

**Como foi varrida.** Apenas o feed Atom público `producthunt.com/feed`, que devolveu exatamente 50 entradas: só os lançamentos recentes, sem busca, sem filtro por tópico e sem histórico. A API GraphQL, que teria busca de verdade, exige token de desenvolvedor que não foi obtido. Tratar essas 50 entradas como 'varredura do Product Hunt' seria falso.

**Viés — o que esta fonte sistematicamente NÃO mostra.** Sem token, só o feed dos ~50 lançamentos mais recentes: não há busca nem histórico, então o tema da varredura não é coberto — o que vier é do dia. Mesmo com token, o Product Hunt premia lançamento com boa campanha de marketing: quem tem comunidade sobe, ferramenta sem equipe de divulgação não aparece. É a fonte mais fraca deste conjunto e está aqui como amostra de contraste.

## Incidentes registrados no log

O que quebrou, o que foi bloqueado e o que foi decidido no meio do caminho.

| tipo | fonte/host | detalhe | ocorrências |
|---|---|---|---|
| `robots_excecao` | export.arxiv.org |  | 41 |
| `sem_itens` | itchio |  | 5 |
| `fonte_bloqueada` | diretorios:theresanaiforthat | 403 de proteção anti-bot (Cloudflare) no sitemap | 2 |
| `fonte_bloqueada` | diretorios:toolify | 403 de proteção anti-bot (Cloudflare) no sitemap | 2 |
| `fonte_bloqueada` | reddit | reddit.com/robots.txt: 'User-agent: * / Disallow: /'. Coleta automatizada proibida pelo pr | 1 |

## O arquivo de log entregue: o que ele é e o que aconteceu com ele

**Incidente.** Durante a coleta, duas instâncias de `varrer.py` rodaram ao mesmo tempo
(arXiv em segundo plano enquanto o Hugging Face rodava em primeiro), as duas com o mesmo
arquivo de log aberto para escrita. Ao conferir os números deste relatório contra o log,
ele tinha voltado a conter apenas as execuções mais antigas. **Perdeu-se de vez o registro
dos eventos de falha da varredura original** — as respostas 429 do arXiv, as requisições
bloqueadas por robots e as falhas do Reddit daquela rodada. O log foi refeito num processo
único, com todo o HTTP vindo do cache, e as fontes que falham (arXiv e Reddit) foram
reexecutadas para que o atrito voltasse a ser evento real gravado no momento em que
aconteceu, e não afirmação de memória. Os números deste relatório saem do log atual.

**Ajuste ao limite de 45 MB.** O log bruto tem 89 MB. O arquivo entregue passou por uma
regra única e uniforme, aplicada por `compactar_log.py`: todo valor de texto acima de N
caracteres e toda lista acima de N/40 elementos são truncados **com marca visível dentro
do próprio registro** (`…(+1832 car)`, `…(+47 itens)`). O script procura o MAIOR N que
ainda cabe no limite, de modo que o corte seja o mínimo necessário.

Nada foi removido, deduplicado, ordenado ou consertado: as repetições, os `utm_source`,
os subdomínios do mesmo site, as linhas de erro e as execuções repetidas continuam lá.
A conferência é automática e roda a cada geração — **número de linhas e conjunto de
endereços distintos idênticos antes e depois**, que são exatamente os dois números que o
sistema de entrega exibe.

O corte atingiu onde estava o desperdício: a API do Hugging Face devolve o resumo de cada
paper três vezes (`paper.summary`, `summary` e `highlightedSummary`), e `siblings` — a
listagem de arquivos do repositório de cada Space, irrelevante para julgar a ferramenta —
somava 10 MB sozinha. O arquivo original, sem corte algum, está em `dados/log_bruto.jsonl`.

**Nota sobre a contagem de candidatos.** A reexecução do arXiv descrita acima aconteceu
DEPOIS de a lista das 500 estar fechada e descrita, e acrescentou 57 candidatos ao total.
Por isso o número de candidatos únicos aqui é maior que o que aparece no relatório da
peneira: as 500 foram peneiradas sobre 17.937 candidatos, e o total varrido é o desta
página. Os 57 novos não entraram na lista final.

## Fontes consideradas e NÃO varridas

| fonte | por quê |
|---|---|
| theresanaiforthat.com | sitemap responde 403 (proteção anti-bot Cloudflare). Não contornado. |
| toolify.ai | sitemap responde 403 (proteção anti-bot Cloudflare). Não contornado. |
| reddit.com | `robots.txt` proíbe coleta automatizada de todo o site; API oficial exige OAuth. |
| Product Hunt (busca) | API GraphQL exige token de desenvolvedor. Só o feed dos ~50 lançamentos recentes foi coletado. |
| Tavily / Exa / Brave / SerpAPI | o aluno optou por não usar API de busca paga ou com chave. |

## Onde o tempo foi mal gasto

Registrado porque faz parte do relato de método, e porque a próxima varredura
não deve repetir os mesmos erros.

| o que custou tempo | quanto | o que evitaria |
|---|---|---|
| **arXiv.** Adaptador escrito, testado e afinado três vezes (3,5 s → 12 s de intervalo) para render 1 resposta útil em 65 requisições. | ~35 min | Ter sondado o arXiv com 10 requisições seguidas ANTES de escrever o adaptador. A sondagem inicial fez só uma, que passou — e uma requisição não revela limite de taxa. |
| **Primeira varredura inteira com a regra de dedup errada.** Diretórios renderam 2 candidatos em vez de 7.776, e só se percebeu ao ler a contagem por fonte. | ~25 min | Ter testado a função de dedup com uma URL de diretório junto das de produto. O teste existia, mas só cobria github, huggingface e streamlit. |
| **Enriquecimento com cache de resposta 429.** 50 Spaces gravados como link morto sendo que só tinham esbarrado em limite de taxa; cache teve de ser purgado e a rodada refeita. | ~20 min | Regra óbvia em retrospecto: só cachear status estável. |
| **Log bruto perdeu as execuções do meio.** Duas instâncias de `varrer.py` rodaram ao mesmo tempo (arXiv em segundo plano enquanto o Hugging Face rodava em primeiro), as duas com o mesmo arquivo de log aberto para escrita. Ao conferir os números do relatório contra o log, ele tinha voltado a conter só as duas primeiras execuções. Refeito num processo único, com tudo vindo do cache. | ~15 min | Nunca rodar duas instâncias do coletor gravando no mesmo log. O mecanismo exato não foi apurado; o efeito foi. |
| **Primeira montagem do pool por top-N global.** O topo virou repositório obscuro do GitHub porque todo README de agente escreve 'multi-agent' e 'trace'. Pool descartado e refeito por cota de fonte. | ~15 min | Ter olhado os 20 primeiros do ranking ANTES de mandar 1.950 itens para enriquecimento. |

O padrão dos quatro é o mesmo: **confiar no código antes de olhar o que ele produziu.**
Em todos, o defeito apareceu na contagem por fonte ou no topo do ranking — dois
lugares baratos de conferir, que passaram a ser conferidos a cada etapa.

