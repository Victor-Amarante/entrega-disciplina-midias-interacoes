# Registro de decisões — o que foi decidido, por quem, e o que a decisão custou

> **Como este documento foi produzido — leia antes de usar.**
>
> Este é o item 4 da entrega, no formato "diretrizes": o critério escrito, os
> cortes duros, as regras de desempate e o que o critério deixou passar.
>
> A **estrutura e a redação** são da IA. A **substância de cada decisão é minha**:
> cada bloco de justificativa abaixo foi escrito a partir de uma escolha que eu
> fiz explicitamente na sessão, entre alternativas que a IA colocou na mesa com
> as consequências declaradas antes da escolha. Onde eu não tinha dado o motivo,
> a IA se recusou a inventar e me perguntou — as respostas dessas perguntas são
> o que está redigido em D4, D5, D6 e D7.
>
> As decisões D1 e D3 foram derivadas do que eu escrevi na abertura da sessão,
> antes de qualquer varredura: que o que me interessa é colocar uma sociedade
> simulada de agentes num ambiente controlado, simular possibilidades e analisar
> o comportamento emergente. Os quatro critérios positivos são as quatro
> condições dessa frase, e a tabela em D3 mostra o mapeamento.
>
> **Nada em aberto.** Os pesos numéricos dos critérios positivos (3,0 / 2,0 /
> 2,0 / 1,5) foram propostos pela IA e ficaram pendentes até eu decidir; estão
> assumidos por mim em D3, e valem também na Entrega 2.

Data da sessão: 02–03/09/2026 · Ferramenta: Claude Code (Opus 5)
Modo declarado: **MODO 3** — a IA executou o coletor, o aluno definiu recorte,
critérios e cortes.

---

## D1 · Recorte: o tema era Entrega 2 disfarçado de Entrega 1

**Situação.** O interesse declarado foi "tecnologias e ferramentas para
desenvolver/criar/analisar simulações com agentes de IA". A IA contestou antes
de escrever a primeira consulta: isso descreve biblioteca e framework, que é
Entrega 2. A Entrega 1 pede aplicativo/plataforma que se abre e usa.

**Alternativas postas na mesa.**
1. Alargar o alvo para *simulação como ambiente* — sandbox hospedado,
   plataforma no-code, observabilidade e replay, mundo/jogo com NPC de IA,
   simulação social, usuários sintéticos. (recomendada pela IA)
2. Manter estrito em "simulação multiagente", com o aviso de que a lista não
   fecharia 500 itens de inspiração e acabaria virando lista de repositório.
3. Trocar o eixo da Entrega 1 e guardar simulação inteira para a Entrega 2.

**Escolhido:** alternativa 1.

**Consequência assumida.** O recorte passou a incluir categorias adjacentes
(jogo, observabilidade, pesquisa de usuário sintético) que não estavam no
entusiasmo original. Em troca, a lista fica de fato na categoria certa.

**Justificativa.** O que me interessa não é a biblioteca — é a possibilidade de
colocar uma sociedade simulada de agentes dentro de um **ambiente controlado**,
rodar possibilidades e olhar o comportamento emergente que aparece. Isso foi o
que eu escrevi antes de qualquer varredura começar, e "ambiente controlado" é
literalmente a Entrega 1: a coisa que se abre e se usa.

Trocar de eixo seria abrir mão do assunto que eu quero apresentar. Manter
estrito seria insistir em chamar de aplicativo aquilo que é biblioteca, e
entregar uma lista de repositório na categoria errada. Alargar para o ambiente
é a única das três que preserva o meu tema **e** respeita a categoria da
entrega — o framework não sai da minha vida, ele volta na Entrega 2, que é o
lugar dele.

O custo que eu aceito: entram categorias que não estavam no meu entusiasmo
original — jogo com NPC, observabilidade, pesquisa com usuário sintético. Aceito
porque todas elas são a mesma pergunta vista de outro ângulo: como é que se
observa um monte de agentes se afetando.

---

## D2 · Fontes varridas

**Escolhido:** os quatro blocos oferecidos — (a) Hugging Face + GitHub,
(b) Product Hunt + Hacker News, (c) arXiv + HF Papers, (d) diretórios de IA +
itch.io + Reddit.

**Sem chave de API de busca.** Tavily, Exa, Brave e SerpAPI foram apresentados
com camada gratuita e trade-off; a opção foi não usar nenhum. Só entrou o
`GITHUB_TOKEN`, que eleva o limite da busca do GitHub de 10 para 30
requisições por minuto.

**Consequência assumida.** Sem API de busca, a varredura não alcança o índice
geral da web: ela vê o que as APIs de nicho indexam. Ferramenta comercial que
não está em diretório, não foi postada no HN e não tem repositório aberto é
invisível para este coletor.

**Justificativa.** Marquei os quatro blocos porque nenhum deles sozinho cobre o
que eu procuro: HF e GitHub mostram o que é aberto, HN mostra o que a comunidade
técnica achou digno de postar, arXiv mostra a pesquisa de onde esse assunto
nasceu, e os diretórios mostram o lado comercial que os outros três ignoram.
Simulação de agentes vive espalhada entre pesquisa, código aberto e jogo — se eu
varresse só um bloco, entregaria uma lista com um sotaque só.

Sobre não usar API de busca: eu não tinha chave de nenhuma e não quis parar a
atividade para criar conta e configurar cota em quatro serviços.

**O que isso me custa, e eu sei que custa:** sem API de busca eu não alcanço o
índice geral da web. A varredura vê o que as APIs de nicho indexam. Ferramenta
comercial que não está em diretório, não foi postada no Hacker News e não tem
repositório aberto é invisível para este coletor — e esse tipo de ferramenta
existe. Se eu fosse refazer com mais tempo, a primeira coisa que eu mudaria era
essa: pegar uma chave gratuita do Tavily ou do Brave e rodar o mesmo vocabulário
contra o índice geral, nem que fosse só para medir o quanto eu perdi.

---

## D3 · Critérios de peneira

Postos como pergunta direta, porque sem regra a peneira é chute.

**Eliminatórios escolhidos (reprova na hora):**
- **E1** não se abre e usa — repositório/biblioteca/PDF puro, sem app;
- **E2** agente único, sem interação entre agentes;
- **E3** paywall antes de ver qualquer coisa.

**Recusado como eliminatório:** "link morto ou projeto parado". A consequência
declarada na hora era que esse critério mataria os marcos fundadores de 2023 do
próprio tema. Foi deixado de fora **de propósito**.

**Positivos escolhidos (todos os quatro):**
- **P1** múltiplos agentes se afetando (peso 3,0);
- **P2** dá para ver por dentro — log, replay, timeline, visualização (2,0);
- **P3** ambiente configurável por quem usa (2,0);
- **P4** produz resultado analisável — dado, métrica, exportação (1,5).

Os pesos foram propostos pela IA na implementação e **assumidos por mim** ao
fim do processo (ver adiante). Estão em `peneirar.py`, na constante `PESOS`, e
mudá-los muda o ranking.

**Justificativa dos quatro positivos.** Eles não são quatro critérios soltos:
são as quatro condições para a frase que eu escrevi no começo — "colocar uma
sociedade simulada de agentes num ambiente controlado, simular possibilidades e
analisar o comportamento emergente" — funcionar de verdade.

| critério | a parte da frase que ele garante |
|---|---|
| P1 múltiplos agentes se afetando | é o que faz ser **sociedade**, e não um agente sozinho |
| P2 dá para ver por dentro | sem log, replay ou visualização não dá para **analisar** o emergente — só assistir |
| P3 ambiente configurável | é o **controlado**: se eu não mexo nas regras, não é experimento, é demo |
| P4 produz resultado analisável | é o **testar possibilidades**: sem dado saindo, não dá para comparar duas rodadas |

Tirar qualquer um deles quebra uma palavra da frase. Por isso marquei os quatro,
e não por querer ser abrangente.

**Justificativa dos eliminatórios.** E1 é o que me mantém na Entrega 1 em vez de
entregar Entrega 2 por engano. E2 cai fora porque agente único não produz
emergência — emergência é efeito de interação, e um chatbot sozinho não tem com
quem interagir. E3 porque se eu não consigo ver a coisa funcionando, eu não
consigo julgar nenhum dos quatro positivos: o cartão viraria chute.

**Por que recusei "link morto/projeto parado" como eliminatório.** Foi
deliberado, e assumo a consequência. Esse critério mataria os marcos fundadores
do meu próprio tema — o Generative Agents de 2023 é código de paper que rodou
para a figura e ficou parado, e é o trabalho que originou o assunto todo.
Reprovar por inatividade seria reprovar exatamente aquilo que eu quero
apresentar. Aceito, em troca, ter link morto na lista e ter que conferir isso na
mão nas 50.

**Sobre os pesos (3,0 / 2,0 / 2,0 / 1,5).** Foram propostos pela IA e ficaram
pendentes até eu decidir. **Mantenho como estão, e a ordem passa a ser minha:**
multiagente pesa mais porque é a condição de existência do tema — sem vários
agentes se afetando, os outros três critérios não têm sobre o que incidir. Os
demais entram como qualificadores. Os mesmos pesos valem na Entrega 2.

---

## D4 · Desempate — decisão contestada pela IA

**Escolhido:** popularidade (estrela, like, voto).

**A IA contestou, e este é o argumento registrado:** as 50 são exclusivas na
turma. Popularidade é o critério que a maioria dos colegas usa por ser o mais
fácil de justificar, então ordenar por ela leva à colisão na mesma cabeça de
lista. Além disso, ela entra em contradição com D3: ao recusar "projeto parado"
como eliminatório, projeto antigo e famoso continua na disputa — e é exatamente
onde popularidade empata coisa morta com SaaS novo e raso.

**Alternativa oferecida:** raridade (número de fontes distintas em que a
ferramenta apareceu), que o depósito já contabiliza no campo `fontes_extras` e
que é tão mecânica quanto popularidade.

**Estado da decisão:** o parâmetro ficou em `--desempate` e as duas ordenações
podem ser geradas e comparadas.

**Justificativa — mantive popularidade, e o contra-argumento não me convenceu.**

O campo que eu estou varrendo é o campo mais infestado de vaporware que existe:
demo de paper que rodou uma vez para gerar a figura, Space que subiu num fim de
semana, repositório com README bonito e três commits. Nesse cenário, estrela,
like e voto são o **único sinal barato de que outra pessoa abriu a coisa e ela
funcionou**. Eu não tenho como abrir 500 ferramentas e testar; popularidade é
uma prova indireta de existência que eu consigo obter de graça.

Isso amarra com D3: eu recusei "projeto parado" como reprovação porque quero
manter os marcos de 2023 na disputa. Justamente por isso preciso de **algum**
filtro de realidade — e popularidade é o que sobra quando atividade recente
está fora.

**O risco que eu assumo, explicitamente:** as 50 são exclusivas na turma, e
popularidade é o desempate que meus colegas provavelmente vão usar por ser o
mais fácil de defender. Ordenar por ela aumenta a chance de eu chegar na hora
de fixar as 50 e encontrar a cabeça de lista já tomada. Aceito porque prefiro
disputar ferramenta que eu sei que funciona a ficar sozinho com ferramenta rara
que talvez nem abra. Se a colisão acontecer, o plano B é descer no ranking, que
está todo gerado — não é um beco sem saída, é uma fila.

_(Alternativa oferecida pela IA e recusada: raridade — nº de fontes distintas em
que a ferramenta apareceu, campo `fontes_extras`, já calculado. Fica registrada
porque a decisão foi tomada sabendo dela, não por desconhecimento.)_

---

## D5 · Fontes que a IA se recusou a varrer

Três decisões técnicas tomadas pela IA e submetidas ao aluno:

| fonte | o que foi medido | decisão |
|---|---|---|
| **Reddit** | `robots.txt` responde `User-agent: * / Disallow: /`; API oficial exige OAuth | **não varrido.** Adaptador escrito e desativado, motivo no código |
| **theresanaiforthat, toolify** | sitemap responde **403** (Cloudflare) | **não contornado**, embora houvesse caminho via proxy de leitura |
| **arXiv** | `export.arxiv.org/robots.txt` responde `Disallow: /`, mas o arXiv publica API oficial no mesmo host com Termos de Uso que autorizam acesso programático | **exceção explícita**, isolada em `EXCECOES_ROBOTS`, removível numa linha |

**Justificativa — mantenho a exceção do arXiv, e ela não contradiz o Reddit.**

As duas situações parecem iguais e não são. No Reddit, o `robots.txt` proíbe e
**não existe outra porta**: a via oficial é OAuth, que eu não tenho. Só me
restaria raspar contra a vontade declarada do site — então não raspei.

No arXiv existe outra porta, e ela é do próprio arXiv. Eles publicam uma API
oficial, documentada, com Termos de Uso próprios que autorizam acesso
programático e pedem 1 requisição a cada 3 segundos. Quando o dono do serviço
publica uma interface para uso automatizado e diz o ritmo que aceita, usar essa
interface nesse ritmo é fazer o que ele pediu — não é burlar. O `Disallow: /` do
`export.arxiv.org` mira quem quer espelhar o site inteiro, que não é o meu caso.

O critério que eu aplico nos dois é o mesmo: **respeitar a vontade declarada do
serviço**. No Reddit, a vontade declarada é "não colete". No arXiv, a vontade
declarada — no documento mais específico, que são os Termos da API — é "colete
assim, nesse ritmo".

**E deu errado mesmo assim.** 65 requisições, 39 respostas 429, 25 falhas de
rede, 1 sucesso, mesmo depois de eu subir o intervalo para 12 segundos — quatro
vezes o que os Termos pedem. O IP ficou limitado e eu abandonei a fonte. A
exceção continua no código (`EXCECOES_ROBOTS`, removível numa linha) porque a
decisão foi tomada e precisa ficar auditável, mas o arXiv **não contribuiu com
nada** para as 500. Perder essa fonte custa: era ela que traria os protótipos de
pesquisa, que é onde "sociedade simulada de agentes" nasceu.

---

## D6 · Bugs encontrados rodando (não teorizando)

Três defeitos reais, achados por olhar o log, e o que cada correção mudou nos
números. Estão aqui porque o processo é o que está sendo avaliado.

| # | defeito | efeito | depois da correção |
|---|---|---|---|
| 1 | regra de dedup tratava domínio de diretório como identidade única | 3.000 fichas do futuretools viraram 1 item; fonte rendeu **+2** | **+7.776** |
| 2 | busca do HF Spaces recebia frases longas; o parâmetro `search` casa substring de id | Spaces rendeu **3** itens em 41 consultas | **+3.478** com 44 termos curtos |
| 3 | intervalo de 3,5 s no arXiv (o que a documentação pede) | **24 respostas 429** seguidas, fonte rendeu zero | intervalo subido para 12 s |

O defeito 1 é o mais instrutivo: a regra de deduplicação **decide quantas
ferramentas existem**. Ela não é detalhe de implementação, é premissa da lista.

**O que eu tiro disso: nenhum dos quatro eu teria pego sozinho.**

Sendo honesto, se a IA tivesse me entregado "17.937 candidatos únicos varridos"
no primeiro relatório, eu teria achado ótimo e seguido em frente. O número
agregado estava excelente **em todos os quatro momentos em que o coletor estava
quebrado**. Ele nunca acusou nada, porque total grande esconde componente
zerado: 7.774 itens faltando nos diretórios sumiam dentro de um total de catorze
mil e pouco.

O que me protege não é desconfiança genérica — "conferir tudo" não é método, é
ansiedade. É ter **dois lugares fixos de conferência obrigatória depois de cada
etapa**, e os dois são baratos:

1. **A contagem por fonte.** Os quatro bugs apareceram aí, e apareceram
   gritando: "+2 candidatos de um sitemap com 3.000 URLs", "3 Spaces em 41
   consultas", "1 sucesso em 65 requisições". Nenhum desses precisa de análise —
   precisa de alguém olhando a proporção.
2. **Os 20 primeiros do ranking.** O quinto problema (pool tomado por
   repositório obscuro do GitHub) não aparecia em contagem nenhuma: os números
   estavam todos certos. Só apareceu quando alguém leu os nomes do topo.

A lição que eu levo para além desta atividade: **o total agregado não é
verificação, é conforto.** Verificação é a decomposição por origem e a amostra
concreta do topo — as duas coisas que a máquina não me dá espontaneamente e que
eu tenho que pedir toda vez.

---

## D7 · O que a IA mediu e que muda a narrativa

**Diretórios comerciais de IA praticamente não cobrem este tema.** Dos 7.776
anúncios varridos em futuretools e aixploria, **2** casam com o tema pelo slug
(0,03%). Uma amostra foi aberta e lida para medir a taxa sobre o texto real das
páginas — o número está em `dados/relatorio_julgamento.md`.

Isso é achado, não buraco: o segmento comercial de IA lista assistente,
gerador e wrapper, e quase não lista ambiente de simulação.

**Minha conclusão: é o formato do mercado, não falha da varredura.**

Diretório de IA vive de tráfego de busca de quem procura "ferramenta para fazer
X mais rápido". O produto que se lista bem ali é o que resolve uma tarefa
conhecida em menos tempo: gerador de texto, de imagem, de legenda, de
apresentação. Simulação de agentes não é produtividade — é **instrumento de
investigação**. Não promete economizar seu tempo, promete te mostrar uma coisa
que você não sabia. Isso não vende do jeito que se vende num catálogo, e por
isso não está no catálogo.

O número, então, não é buraco na minha varredura: é uma **medida do recorte
comercial**. Dos 7.776 anúncios de dois dos maiores diretórios de IA, o meu tema
aparece em fração desprezível.

Reconheço a limitação da medida: o sitemap só dá URL e slug, e um produto
chamado "Sumzy" poderia ser um simulador de agentes sem que o slug entregasse.
Por isso uma amostra foi aberta e lida página a página, e a taxa medida sobre o
texto real está em `dados/relatorio_julgamento.md` — é ela que sustenta a
afirmação, não o slug.

**O que isso quer dizer para a minha lista:** as minhas 500 vêm de onde o assunto
efetivamente mora — pesquisa, código aberto, jogo, comunidade técnica — e não de
onde ferramenta de IA é anunciada. Isso dá um sotaque à lista, e o sotaque é o
do próprio campo.

---

## As sete perguntas do enunciado — estado de cada uma

| # | pergunta | onde está respondida |
|---|---|---|
| 1 | quais fontes, e o que cada uma NÃO mostra | `entrega/anexo-tecnico-fontes.md`, seção "Viés declarado" — medido |
| 2 | o que reprova na hora | D3 acima — decidido |
| 3 | o que conta como interessante, em regra | D3 acima — decidido (P1..P4) |
| 4 | o que decide o empate | D4 acima — **decidido e contestado; pendente de justificativa** |
| 5 | como sabe que o link existe | `enriquecer.py` abre cada URL e grava status, URL final e tamanho |
| 6 | que ferramenta boa o seu critério derruba | `dados/relatorio_peneira.md`, seção "Amostra do que o SEU critério derrubou" |
| 7 | por que essas 50 e não outras | **só você pode responder** — e é o teste final da atividade |
