# ESTUDO.md — o método, estudado por vafs

CIN0055 · Tendências em Mídia e Interação · 2026.2

---

## Futures Wheel (roda dos futuros)

Proposto por **Jerome Glenn**, em 1971, enquanto estudante na Antioch Graduate School of
Education ([confirmado na Wikipédia, "Futures wheel"](https://en.wikipedia.org/wiki/Futures_wheel))
— a ideia era dar forma visual a
uma pergunta simples: "se X acontece, o que isso causa, e o que a causa causa?". O centro do
diagrama é a disrupção; a primeira camada de raios são efeitos diretos (1ª ordem); cada raio
gera novos raios (2ª ordem), e assim por diante. É uma técnica de **ideação estruturada em
grupo**, não um algoritmo — o valor está em obrigar quem participa a continuar perguntando
"e daí, o que isso causa" além do óbvio.

Onde parar de derivar não é regra fixa do método original; na prática, para-se quando (a) o
elo causal deixa de ser narrável em uma frase — vira "e aí tudo muda", sem mecanismo — ou
(b) o efeito ultrapassa o horizonte de tempo que a análise se propôs a cobrir, ou (c) o efeito
já seria o mesmo para qualquer disrupção genérica, isto é, deixou de ser específico ao tema.

**Para que não serve:** não serve para estimar probabilidade nem para priorizar onde investir
recurso — é ferramenta de mapeamento de possibilidades, não de previsão quantificada. Uma roda
bem feita não diz "isto vai acontecer", diz "isto é logicamente derivável se aquilo acontecer".

---

## Hype Cycle da Gartner

Curva proposta pela analista **Jackie Fenn**, em 1995, com cinco fases: gatilho tecnológico,
pico de expectativas infladas, vale da desilusão, rampa de esclarecimento, platô de
produtividade ([Wikipédia, "Gartner hype cycle"](https://en.wikipedia.org/wiki/Gartner_hype_cycle)).
A afirmação implícita da curva é que **toda tecnologia nova passa por excesso de expectativa
antes de qualquer adoção estável** — e que dá para posicionar uma tecnologia específica num
ponto dessa curva hoje.

A crítica mais citada ([Dedehayir & Steinert, 2016, *Technological Forecasting and Social
Change*](https://hypestudies.org/resources/the-hype-cycle-model-a-review-and-future-directions))
testou o modelo contra os próprios bancos de dados históricos da Gartner e encontrou
incongruência entre o que a curva prevê e o que os dados mostram — a Gartner nunca publicou os
dados brutos por trás da curva, e o formato é herdado de heurística de mercado, não de medição.
Um levantamento posterior do *The Economist* (citado na mesma página da Wikipédia) reforça o
ponto de forma concreta: só cerca de **um quinto** das tecnologias analisadas percorre o ciclo
inteiro, de gatilho a adoção ampla, e **seis em cada dez** presas no vale da desilusão nunca se
recuperam dali. Isso não invalida usar a curva como **linguagem compartilhada** para discutir
estágio de maturidade; invalida tratá-la como instrumento preditivo calibrado.

**Para que não serve:** não serve para prever *quando* uma tecnologia especificamente vai
atingir o platô — não há validação de tempo de trânsito entre fases — e não serve como
argumento de autoridade ("a Gartner colocou aqui, logo é isso") sem declarar que é
posicionamento qualitativo.

---

## Quadrante Mágico (Magic Quadrant)

Também da Gartner: posiciona fornecedores de um mercado específico em dois eixos —
**capacidade de execução** (o quão bem entrega hoje) e **completude de visão** (o quão bem
antecipa onde o mercado vai). Os quatro quadrantes (líderes, desafiantes, visionários,
nicho) comparam **empresas entre si, num mercado já definido**, não tecnologias entre si nem
o futuro de uma categoria.

**Para que não serve:** não serve como mapa de futuro de tecnologia — mede posição competitiva
atual de fornecedores, com metodologia paga por quem é avaliado, e não diz nada sobre se a
categoria de mercado inteira ainda vai existir daqui a dez anos.

---

## Emergente × disruptivo (e maduro)

A distinção que a disciplina cobra, e a mais fácil de errar por vir sempre em conjunto com
entusiasmo: nem toda tecnologia emergente é disruptiva, e tecnologia madura não é nem uma
coisa nem outra, mesmo quando ainda está evoluindo.

Critério adotado (detalhado com os testes completos em `SKILL.md`, seção 2):
- **Madura** — já tem casos de uso em produção, em escala, como opção padrão de algum fluxo
  real; o que resta é melhorar, não mudar de natureza.
- **Emergente** — existe fora do laboratório, mas não é escolha padrão em escala; a curva de
  capacidade ainda sobe.
- **Disruptiva** — subconjunto do emergente onde, se escalar, um ator ou prática nomeável
  **perde a razão de existir** — não só fica mais lento/caro por comparação.

**Para que não serve:** o critério não mede qualidade nem valor da tecnologia — só decide se
ela entra como raiz de um mapa de futuro. Uma tecnologia madura pode ser extremamente
importante e ainda assim não pertencer à seção 4 de um documento de tendência.

---

## Efeitos de 1ª, 2ª e 3ª ordem

O que separa uma ordem da seguinte, na prática, não é o assunto do efeito — é **de que ele
depende**. 1ª ordem depende só da disrupção. 2ª ordem só existe porque um efeito de 1ª ordem já
aconteceu, e mexe com estrutura (papel de trabalho, modelo de negócio), não com o fenômeno
técnico isolado. 3ª ordem reorganiza instituição ou categoria cultural, e só se sustenta se o
efeito de 2ª ordem que a originou também se sustentar — por isso confiança baixa na 3ª ordem é
o resultado esperado, não uma falha da análise.

**Para que não serve:** o número da ordem não é medida de importância — um efeito de 3ª ordem
não é "mais grave" que um de 1ª, é só mais distante causalmente e mais incerto. Tratar ordem
como ranking de relevância é o erro mais comum de quem aplica o método pela primeira vez.

---

## Método adicional: Three Horizons Framework

Proposto por **Bill Sharpe** (International Futures Forum), formalizado no livro *Three
Horizons: The Patterning of Hope* (2013/2016). Descreve a transição entre três "horizontes"
coexistentes — confirmado na [página oficial do IFF](https://www.internationalfuturesforum.com/three-horizons):
H1, o sistema dominante hoje ("business as usual"); H2, inovações já em andamento, algumas das
quais só prolongam H1 e outras preparam H3; e H3, "inovações radicais que introduzem formas
completamente novas de fazer as coisas" e só se tornam dominantes décadas depois. A utilidade
prática para este trabalho: força a pergunta "esta inovação prolonga o presente ou prepara
outra coisa?" — uma segunda peneira para os candidatos a disrupção-raiz, complementar ao teste
emergente/disruptivo.

**Para que não serve:** não data eventos nem gera prazo — é qualitativo sobre a forma da
transição entre sistemas, não sobre quando ela acontece; não substitui a roda dos futuros para
derivar efeitos específicos, só ajuda a filtrar o que entra nela.
