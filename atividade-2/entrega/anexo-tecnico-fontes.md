# Anexo técnico — Entrega 2: fontes varridas, viés e números medidos

> **Como este arquivo foi produzido.** Gerado por `relatar.py` a partir de
> `dados/log_bruto.jsonl` e `dados/candidatos.jsonl`. Todo número foi medido,
> nenhum estimado. Método e viés de cada fonte estão declarados nas constantes
> `METODO` e `VIES` dentro do adaptador correspondente, em `garimpo/fontes/` —
> são a leitura do coletor. O julgamento sobre aceitar esse recorte é do aluno
> e não está neste arquivo.

Gerado em 2026-09-09T21:26:12-03:00

## O que esta unidade coleta

APIs, bibliotecas, SDKs, frameworks, componentes e código aberto que possam ser
instalados, importados ou chamados de dentro do código. Aplicativo usado à mão
é Entrega 1 — e foi entregue separadamente, com o mesmo tema visto pelo outro lado.

## Números da varredura

- itens brutos colhidos (antes da deduplicação): **64844**
- requisições HTTP feitas: **1005**
- candidatos únicos após deduplicação: **58987**
- candidatos vistos em mais de uma fonte: **0**

### Requisições por host

| host | requisições |
|---|---|
| `raw.githubusercontent.com` | 282 |
| `pypi.org` | 258 |
| `api.github.com` | 128 |
| `registry.npmjs.org` | 50 |
| `crates.io` | 50 |
| `azuresearch-usnc.nuget.org` | 50 |
| `packagist.org` | 50 |
| `rubygems.org` | 50 |
| `huggingface.co` | 50 |
| `hn.algolia.com` | 37 |

### Códigos de resposta

| status | ocorrências |
|---|---|
| 200 | 961 |
| 404 | 44 |

_status -1 = falha de rede/timeout; 999 = requisição não feita por robots.txt._

### Itens brutos por rótulo de coleta

| rótulo | itens brutos | candidatos únicos |
|---|---|---|
| awesome | 20042 | 17203 |
| crates | 4460 | 3693 |
| github | 11199 | 10061 |
| herdado:arxiv:projeto | 0 | 3 |
| herdado:github | 0 | 2259 |
| herdado:hn | 0 | 193 |
| herdados | 2455 | 0 |
| hn | 557 | 338 |
| huggingface | 2272 | 2227 |
| npm | 4624 | 4338 |
| nuget | 2800 | 2545 |
| packagist | 2593 | 2338 |
| pypi | 13008 | 13008 |
| rubygems | 834 | 781 |

### Candidatos por faceta do vocabulário

A faceta vem de `garimpo/consultas.py`. Faceta com número baixo significa que
aquele recorte rendeu pouco — pode ser que o assunto seja raro, ou que os termos
estejam errados. As duas hipóteses são do aluno.

| faceta | candidatos |
|---|---|
| curadoria | 17203 |
| ? | 15954 |
| pacote_python | 13008 |
| modelo | 2227 |
| multiagente_llm | 847 |
| avaliacao_bench | 535 |
| abm_framework | 499 |
| topico:multiagent-systems | 472 |
| topico:agent-based-modeling | 468 |
| topico:multi-agent-reinforcement-learning | 468 |
| topico:reinforcement-learning-environments | 467 |
| topico:multi-agent-systems | 466 |
| topico:discrete-event-simulation | 463 |
| topico:llm-observability | 457 |
| topico:ai-agents | 452 |
| topico:llm-agents | 449 |
| topico:game-ai | 448 |
| topico:complex-systems | 445 |
| topico:agent-evaluation | 434 |
| topico:agent-framework | 406 |
| topico:npc | 384 |
| topico:agent-based-simulation | 345 |
| memoria_estado | 342 |
| topico:simulation-framework | 307 |
| topico:behavior-tree | 302 |
| topico:emergent-behavior | 238 |
| simulacao_social | 165 |
| observabilidade_sdk | 153 |
| ambiente_rl | 84 |
| topico:social-simulation | 79 |
| npc_jogos | 74 |
| sandbox_ambiente | 73 |
| topico:crowd-simulation | 69 |
| observabilidade_replay | 63 |
| topico:generative-agents | 56 |
| sandbox_execucao | 39 |
| sociedade_simulada | 20 |
| avaliacao_arena | 8 |
| robotica_mundo | 6 |
| economia_mercado | 6 |
| economia_negociacao | 3 |
| abm_classico | 2 |
| usuarios_sinteticos | 1 |

## Método e viés de cada fonte

Cada bloco abaixo sai do próprio adaptador: **como** aquela fonte foi varrida e
**o que ela sistematicamente não mostra**.

### herdados

**Rendimento medido:** 2455 itens brutos → 2455 candidatos únicos.

**Como foi varrida.** Lê `atividade-1/dados/candidatos.jsonl` e reaplica a função `eliminar()` da peneira daquela entrega, mantendo apenas os itens que ela rejeitou com motivo de Entrega 2 — 'repositório sem homepage', 'link aponta para hospedagem de código' e link de registro de pacote. Paper e página de publicação são descartados, porque reprovam também no critério E1 desta entrega. Nenhuma requisição de rede é feita: são endereços já coletados, já normalizados e já deduplicados pela mesma regra, e cada um entra com fonte `herdado:<fonte original>` para poder ser separado da coleta nova a qualquer momento.

**Viés — o que esta fonte sistematicamente NÃO mostra.** Carrega inteiro o viés da varredura da Entrega 1, porque é a mesma coleta vista pelo avesso: mesmo vocabulário de nove facetas, mesmas fontes (Hacker News, GitHub, Hugging Face, itch.io, diretórios), mesmos cegos. Como o vocabulário de lá mirava AMBIENTE e não biblioteca, o que sobra aqui é enviesado para projeto que se apresenta como produto — e sub-representa biblioteca de infraestrutura, que ninguém descreve como 'ambiente de simulação'. Não substitui varredura nova; complementa.

### registros

**Rendimento medido:** 15311 itens brutos → 13695 candidatos únicos.

**Como foi varrida.** Uma API pública de busca por registro, sem chave, todas conferidas por sondagem antes de o adaptador existir: npm (`registry.npmjs.org/-/v1/search`, paginação por `from`), crates.io (`/api/v1/crates`, paginação por `page`), NuGet (`azuresearch-usnc.nuget.org/query`, paginação por `skip`), Packagist (`/search.json`) e RubyGems (`/api/v1/search.json`). São varridos 50 TERMOS CURTOS, não frases: registro casa substring de nome, descrição e palavra-chave, e frase longa devolve quase nada — lição medida na Entrega 1, quando a busca do Hugging Face rendeu 3 itens em 41 consultas frasais. De cada pacote saem nome, descrição do autor, contagem de download, versão, licença quando declarada e link do repositório.

**Viés — o que esta fonte sistematicamente NÃO mostra.** Só enxerga o que foi EMPACOTADO E PUBLICADO. Código de pesquisa que fica no GitHub sem release — que é a maior parte do que existe sobre simulação de agentes — é invisível aqui. Cada registro carrega o viés da sua linguagem: crates.io só tem Rust, NuGet só .NET, e por isso o Python, que domina simulação científica, aparece sub-representado, já que o PyPI não pôde ser varrido. A busca ordena por relevância textual e por popularidade, então pacote novo e bom afunda, e nome genérico ('agents', 'simulation') traz muito homônimo de outro domínio. Contagem de download infla com dependência transitiva e com CI: número alto mede quantas máquinas baixaram, não quantas pessoas usaram.

### pypi

**Rendimento medido:** 13008 itens brutos → 13008 candidatos únicos.

**Como foi varrida.** Percorre o índice de sitemaps publicado no `robots.txt` do PyPI: 257 arquivos com cerca de 7.900 URLs de projeto cada. A busca do site não foi usada porque responde com desafio JavaScript, e contornar proteção anti-bot está fora do que esta coleta faz. Como o sitemap traz só o endereço, o filtro é por TOKEN do slug — o nome é quebrado em `-`, `_` e `.` e precisa conter um token forte do vocabulário (agent, abm, simul, swarm, mesa, netlogo, pettingzoo, marl, npc, boids…). Filtrar por substring foi medido antes e dá 1,4% com muito falso positivo. A confirmação de descrição e licença acontece depois, no enriquecimento, em `pypi.org/pypi/<nome>/json`.

**Viés — o que esta fonte sistematicamente NÃO mostra.** O sitemap não tem descrição, categoria nem popularidade: a seleção aqui é feita pelo NOME do pacote e mais nada. Isso favorece quem batizou o projeto de forma descritiva e é cego para a biblioteca bem nomeada de outro jeito — uma simulação de agentes chamada 'Orion' não aparece por nenhum caminho. Também entra muito homônimo: 'agent' é palavra comum em monitoramento, automação comercial e antivírus, domínios que nada têm a ver com este recorte. E, por vir do índice completo, não há ordenação por qualidade nem por uso: pacote abandonado com nome bom passa, e pacote ativo com nome ruim não.

### github

**Rendimento medido:** 11199 itens brutos → 10061 candidatos únicos.

**Como foi varrida.** Search API autenticada por token pessoal (30 requisições/minuto contra 10 sem token), em duas passadas: 10 consultas de TEXTO e 21 consultas por TÓPICO (`topic:<nome>`), cada uma até 5 páginas de 100 resultados, ordenadas por estrelas — a API limita a 1000 resultados por consulta. A passada por tópico existe porque tópico é curadoria do próprio autor e alcança repositório cuja descrição não usa as palavras do meu vocabulário. De cada repositório saem estrelas, licença declarada, linguagem, data do último push, se está arquivado, os tópicos e a homepage.

**Viés — o que esta fonte sistematicamente NÃO mostra.** Só código aberto, e só o que está no GitHub — GitLab, Codeberg e código corporativo fechado não existem aqui. Estrela mede aprovação de desenvolvedor, não qualidade nem uso: repositório de tutorial e lista de links acumulam mais estrela que biblioteca séria de nicho. Ordenar por estrela enterra projeto novo e bom. A busca por tópico depende de o autor ter marcado o repositório, então quem não marca fica invisível por esse caminho. E repositório arquivado ou parado aparece igual a projeto ativo se ninguém olhar a data.

### awesome

**Rendimento medido:** 20042 itens brutos → 17203 candidatos únicos.

**Como foi varrida.** Duas etapas. Primeiro a Search API do GitHub acha as listas com 8 consultas do tipo `awesome <tema> in:name,description`. Depois o README cru de cada lista é baixado de `raw.githubusercontent.com/<repo>/HEAD/README.md` (com queda para `master` e `main`) e os links de markdown `[nome](url)` são extraídos por expressão regular, ficando só os que apontam para repositório ou registro de pacote. O texto que segue o link na linha da lista é guardado como descrição — é a palavra do curador, normalmente mais útil que a autodescrição do autor da biblioteca.

**Viés — o que esta fonte sistematicamente NÃO mostra.** É curadoria, com todos os vícios de curadoria: reflete o gosto e a data de quem manteve a lista. Lista awesome envelhece mal e quase nunca remove link morto, então traz projeto abandonado com naturalidade. Há forte efeito de bola de neve — quem já está na lista ganha estrela e continua na lista — e listas se copiam entre si, o que faz o mesmo punhado de bibliotecas famosas aparecer em todas. Cobre bem o que é popular em inglês e mal o que é recente, regional ou de nicho sem porta-voz.

### huggingface

**Rendimento medido:** 2272 itens brutos → 2227 candidatos únicos.

**Como foi varrida.** `huggingface.co/api/models?search=<termo>&full=true`, sem chave, com os 50 termos CURTOS do vocabulário e ordenação por downloads. A escolha por termo curto não é estilo: o parâmetro `search` do HF casa substring do identificador do modelo, e frase longa devolve quase nada — medido na Entrega 1. De cada modelo saem downloads, curtidas, biblioteca de origem, tarefa, licença declarada nas tags e data de atualização.

**Viés — o que esta fonte sistematicamente NÃO mostra.** Só modelo hospedado na própria Hugging Face: peso fechado de laboratório comercial não aparece. Modelo não é biblioteca de simulação — é peça que uma simulação chama —, então esta fonte tende a trazer o INSUMO do tema e não o tema. A ordenação por download concentra tudo nos mesmos modelos genéricos de uso geral, e a busca por substring traz muito homônimo: 'agent' casa com qualquer coisa que tenha a palavra no nome do repositório, inclusive fine-tune sem relação com agentes.

### hn

**Rendimento medido:** 557 itens brutos → 338 candidatos únicos.

**Como foi varrida.** API de busca do Algolia (`hn.algolia.com/api/v1/search`), sem chave, com as 35 frases do vocabulário, até 5 páginas de 100 resultados por consulta, filtrando `tags=story`. O item colhido é a URL externa que a pessoa postou, não a página da discussão. Diferença em relação à Entrega 1: lá `github.com` entrava na lista de lixo porque repositório não era o alvo; aqui é o alvo, e só continuam descartados agregador, rede social e imprensa.

**Viés — o que esta fonte sistematicamente NÃO mostra.** Bolha do Vale do Silício e anglófona. Premia lançamento sobre maturidade: biblioteca boa que nunca foi postada simplesmente não existe aqui, e uma mesma ferramenta reaparece em vários posts. Post com muito voto costuma indicar polêmica, não qualidade. Nada é indexado sem que um humano tenha submetido, então a cobertura é do que a comunidade resolveu comentar, não do que existe.

## Incidentes registrados no log

O que quebrou, o que foi bloqueado e o que foi decidido no meio do caminho.

| tipo | fonte/host | detalhe | ocorrências |
|---|---|---|---|
| `awesome_lista_lida` |  |  | 222 |
| `sem_itens` | awesome | README não encontrado em HEAD/master/main | 20 |
| `robots` | api.github.com |  | 2 |
| `herança` |  |  | 1 |
| `robots` | registry.npmjs.org |  | 1 |
| `robots` | crates.io |  | 1 |
| `robots` | azuresearch-usnc.nuget.org |  | 1 |
| `robots` | packagist.org |  | 1 |
| `robots` | rubygems.org |  | 1 |
| `robots` | pypi.org |  | 1 |
| `pypi_indice` |  |  | 1 |
| `pypi_varredura` |  |  | 1 |
| `awesome_listas` |  |  | 1 |
| `robots` | raw.githubusercontent.com |  | 1 |
| `robots` | huggingface.co |  | 1 |
| `robots` | hn.algolia.com |  | 1 |

## Fontes consideradas e NÃO varridas

| fonte | por quê |
|---|---|
| **PyPI (busca)** | `pypi.org/search/` responde 200 mas devolve desafio JavaScript (proteção anti-bot). Não contornado — mesma decisão tomada na Entrega 1 com theresanaiforthat e toolify. O PyPI **foi** varrido pelo sitemap, que o próprio `robots.txt` publica. |
| **Papers with Code** | a API `paperswithcode.com/api/v1/` devolve HTML em vez de JSON: está desativada. |
| **libraries.io** | a API exige chave (401 sem ela). |
| **pkg.go.dev** | `robots.txt` proíbe `/search?*`; sobraria só o sitemap, que não foi varrido por falta de tempo — buraco declarado, não resolvido. |
| **ecosyste.ms** | `ConnectTimeout` em todas as chamadas a partir desta rede. |
| **OpenAlex** | funciona e foi testada, mas foi descartada de propósito: devolve artigo científico, e artigo reprova no critério E1 desta entrega (não se instala nem se importa). |
| **Reddit** | `robots.txt` proíbe coleta automatizada de todo o site, como já medido na Entrega 1. |
| **Maven, CocoaPods, pub.dev, Hex** | não varridos por escolha de escopo: o tema quase não vive nesses ecossistemas. Buraco conhecido. |

