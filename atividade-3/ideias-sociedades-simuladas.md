# Ideias do experimento — Sociedades simuladas

*CIN0055 · Tendências em Mídia e Interação · 2026.2 · Movimento 3 · vafs*

Ponto de partida: [`tendencia-sociedades-simuladas.md`](tendencia-sociedades-simuladas.md), o
mapa do movimento 2. Os números entre colchetes, como [19], apontam para as fontes da seção 11
daquele documento. Os códigos D1–D3 e e1–e6 são as disrupções e os efeitos da roda (seção 5).

---

## 1. Como fiz o brainstorming

**Com quem.** Com Claude (Claude Code, modelo Opus 5.5), numa sessão, tendo o documento de
tendência inteiro como contexto. Vale o mesmo aviso da seção 7 do mapa: é um LLM propondo
experimentos sobre LLMs simulando pessoas. Por isso o filtro abaixo pergunta, de propósito,
onde a simulação pode **falhar** à vista da turma, e não onde ela impressiona.

**Método, em quatro passos.**

1. **Partir das dúvidas do mapa, não da tecnologia.** Listei os pontos em que o mapa tem
   confiança baixa ou depende de um "se" que dá para testar em pequena escala:
   - a variância comprimida (e1.2);
   - o erro em subgrupos (e2.2);
   - a detectabilidade do respondente sintético (e5);
   - o custo de manipular uma pesquisa (e6);
   - a validade da D2, a raiz mais frágil do mapa;
   - o consentimento sobre o gêmeo (e2.1.1);
   - o rótulo "sintético" (e5.2.1);
   - a simulação como gênero de mídia (e4.1.1).
2. **Gerar ideias por raiz.** Pelo menos três por disrupção, mais as que saíram dos sinais
   fracos. Saíram **14 ideias**.
3. **Filtrar com cinco perguntas eliminatórias.**
   - (a) Usa tecnologia emergente, ou daria para fazer com formulário ou com modelagem baseada
     em agentes clássica?
   - (b) Responde uma pergunta que está na roda?
   - (c) Cabe num teste presencial de cerca de 50 minutos com a turma?
   - (d) Uma pessoa consegue construir no prazo, usando APIs que já existem?
   - (e) Pode ficar no ar depois, para quem não é da turma?

   E uma pergunta de desempate: **o resultado aparece na tela, na hora, para a turma discutir?**
4. **Escolher três ideias que testem raízes diferentes**, uma por disrupção. Assim, a conversa
   de 15/10 também decide qual parte do mapa vale mais a pena testar.

**Confronto com o mapa do professor e conversa da aula.**
> **[A PREENCHER]** O que o mapa do professor tinha que o meu não tinha, o que a turma e o
> professor questionaram na apresentação de tendência, e como isso mudou a lista abaixo.

### As 14 ideias e o que aconteceu com cada uma

| # | Ideia | Testa | Resultado |
|---|---|---|---|
| 1 | **Painel espelho completo** (seção 10 do mapa): entrevista de 15–20 min com cada aluno, gêmeos e painel demográfico | D1 · e1.2, e2 | **Fundida na ideia 1**, em versão enxuta. A entrevista longa não cabe no teste e exigiria coleta extensa antes. |
| 2 | **A turma prevista**: um painel sintético prevê as respostas da turma antes de ela responder | D1 · e1.2, e2.2 | **Selecionada (ideia 1)** |
| 3 | **Caça ao respondente sintético**: a turma cria armadilhas para pegar agentes infiltrados numa pesquisa | D3 · e5 | **Selecionada (ideia 2)** |
| 4 | **Pesquisa contaminada ao vivo**: quantas respostas falsas viram o resultado de uma enquete | D3 · e6 | **Fundida na ideia 2.** Usa a mesma infraestrutura e vira o segundo ato. |
| 5 | **Feed misto**: a turma e agentes na mesma rede social, com o algoritmo de feed trocando entre rodadas | D2 · e3 | **Selecionada (ideia 3)** |
| 6 | **Moltbook da turma**: uma rede só de agentes, com perfis da turma, rodando por uma semana | D2 · sinal fraco | **Cortada.** Sem comparação com humanos, o resultado é espetáculo e não responde nada que [23] não mostre. |
| 7 | **Usuários sintéticos de UX**: agentes com navegador testam um protótipo, e a turma testa o mesmo | D1 aplicada a UX [24] | **Cortada por pouco.** Puxa o tema para UX, e o agente com navegador é frágil de montar. Fica de reserva. |
| 8 | **O gêmeo que envelhece**: um gêmeo criado hoje é comparado com a mesma pessoa semanas depois | D1 · o que falta | **Cortada.** Precisa de um intervalo maior que o calendário. |
| 9 | **Leilão do gêmeo**: cada aluno vê o que o próprio gêmeo diz e decide se o licenciaria, e por quanto | e2.1.1 | **Fundida na ideia 1**, como discussão final. |
| 10 | **Rótulo "sintético"**: a turma lê pesquisas com e sem rótulo e diz quanto confia em cada uma | e5.2.1 | **Cortada no filtro (a).** A manipulação é o rótulo, e a tecnologia emergente seria só cenário. |
| 11 | **Simulação como notícia**: a turma lê uma matéria sobre simulação social e julga se aquilo é evidência | e4.1.1 | **Cortada** pelo mesmo motivo da 10. |
| 12 | **Debate contra um eleitorado simulado** | — | **Cortada.** Testa persuasão, não o instrumento, e já estava no mapa como sem evidência de uso. |
| 13 | **Troca de modelo**: a mesma persona em três modelos, para ver o colapso de persona | sinal fraco [22] | **Fundida na ideia 1**, como variável: o painel roda em mais de um modelo. |
| 14 | **O gêmeo minoritário**: medir o erro só para quem é minoria na turma | e2.2 | **Fundida na ideia 1**, como recorte da análise. |

Resumo: 14 ideias, 3 selecionadas, 5 fundidas nas selecionadas e 6 cortadas.

---

## 2. As três ideias

### Ideia 1 — A turma prevista

**O que é.** Um app web em que uma população sintética tenta adivinhar a turma antes de a
turma falar.

- **Antes do teste.** Cada aluno preenche um formulário anônimo de 1 minuto com idade, curso,
  período, cidade de origem e gênero. Com essa distribuição, o app gera um **painel
  demográfico** de cerca de 100 personas. Quem quiser conversa também por 5 minutos com um
  entrevistador de IA sobre hábitos de mídia, e a transcrição vira um **gêmeo** dessa pessoa
  (Park et al. [2] em miniatura). A participação é opcional e anônima, e as transcrições são
  apagadas depois do teste.
- **No dia, primeiro as máquinas.** Painel e gêmeos respondem a um questionário que nenhum
  deles viu, e o resultado fica escondido. O questionário tem três partes:
  - cerca de oito perguntas de atitude sobre mídia, em escala;
  - um experimento de enquadramento, em que metade vê uma manchete com enquadramento A e a
    outra metade com B;
  - duas perguntas abertas.
- **Depois a turma.** A turma responde pelo celular. Antes da revelação, cada um **aposta**
  onde a simulação vai errar.
- **A revelação.** Humanos, gêmeos e painel demográfico aparecem lado a lado: médias,
  desvio-padrão, efeito do enquadramento e erro por subgrupo. O painel roda em dois modelos
  (por exemplo, Claude e um modelo aberto), para ver se um colapsa mais as personas que o
  outro [22].
- **Fecho.** Cada aluno vê o que o próprio gêmeo respondeu e diz se aceitaria que uma empresa
  o consultasse no lugar dele, e em que condições (e2.1.1).

**A pergunta sobre o futuro.** Quando populações sintéticas substituírem a amostra humana em
pesquisa exploratória, onde elas vão errar primeiro: na média, na variância, no subgrupo ou no
efeito de tratamento? (Testa e1.2 e e2.2.)

**Tecnologia emergente.** Painéis sintéticos e gêmeos comportamentais ancorados em entrevista,
o que a Qualtrics [25][26] e a Simile [28] vendem hoje em early access. **Por que não dá com
tecnologia madura:** um modelo estatístico clássico, como uma regressão sobre dados
demográficos, estima a média de um item que já conhece. Ele não gera uma resposta aberta a uma
pergunta inédita, nem reage a uma manchete que nunca viu. O que se testa é justamente essa
promessa.

**Por que é rápida de construir.** Um formulário, chamadas de API a um LLM, um banco simples e
uma tela de gráficos. Não tem treino de modelo. O custo é de centavos por persona.

**O que espero observar.**
- Médias próximas das da turma na maioria dos itens, como em [3][5].
- Desvio-padrão sintético **menor** que o humano. Aposto numa razão entre 0,5 e 0,8 [5][24].
- O efeito de enquadramento com o sinal certo e a magnitude errada [18].
- Erro maior para quem é minoria na turma [6].
- Gêmeos melhores que o painel demográfico nas perguntas abertas, mas empatados nas escalas,
  porque a turma é homogênea.
- **O que me faria mudar de ideia:** os gêmeos reproduzirem a variância da turma e o efeito de
  enquadramento. Nesse caso, meu ceticismo sobre e1.2 estava exagerado.

---

### Ideia 2 — Caça ao respondente sintético

**O que é.** Um jogo de *red team* sobre pesquisa online, em dois atos.

- **Ato 1: a turma é o instituto de pesquisa.** Em grupos, a turma escreve **perguntas-armadilha**
  para pegar bots. Podem ser checagens de atenção, perguntas sobre algo local (o RU, uma linha
  de ônibus do Recife, uma piada interna do CIn), perguntas sobre eventos impossíveis ou
  perguntas que exigem experiência vivida. Essas perguntas entram num questionário que a turma
  responde **ao mesmo tempo** que vários agentes autônomos com persona de aluno do CIn. Os
  agentes seguem o estilo de Westwood [19]: persona de cerca de 500 palavras e instrução para
  parecer humano. Uma parte dos agentes também tem acesso a busca na web. Depois, a turma vê as
  respostas misturadas e anônimas e marca quais são de máquina. O placar mostra qual armadilha
  pegou mais agentes e quantos humanos foram acusados injustamente.
- **Ato 2: a turma é o atacante.** A turma vota numa enquete sobre um tema que a divide. O app
  mostra, ao vivo, quantas respostas sintéticas bastam para virar o resultado e se as armadilhas
  do ato 1 as teriam barrado.

Os agentes só respondem a esse questionário interno. Nada é injetado em pesquisas reais.

**A pergunta sobre o futuro.** Quando uma resposta coerente deixar de provar que há um humano do
outro lado, o que ainda distingue gente de máquina numa pesquisa? E quanto custa virar um
resultado? (Testa e5 e e6.)

**Tecnologia emergente.** O respondente sintético autônomo baseado em LLM [19]. **Por que não dá
com tecnologia madura:** bots antigos, como scripts ou preenchimento aleatório, falham nas
checagens de atenção, e era isso que os denunciava. A capacidade nova é passar em 99,8% delas
[19], e é exatamente ela que o jogo coloca à prova. As defesas contra isso ainda estão sendo
inventadas [20].

**Por que é rápida de construir.** É a mais simples das três: um questionário próprio, agentes
que leem as perguntas e respondem pela API, e uma tela de votação com placar.

**O que espero observar.**
- Detecção perto do acaso nas perguntas genéricas e nas checagens de atenção: o agente passa.
- Detecção acima do acaso nas perguntas de contexto local ou de experiência vivida. É a hipótese
  mais interessante: a defesa que sobra seria o **contexto**, e não a lógica. Se o agente com
  busca também passar nessas perguntas, nem essa defesa sobra.
- **Falsos positivos.** Humanos acusados de ser bots por responderem "certinho demais" ou curto
  demais. Esse é, em pequena escala, o custo de exclusão que a verificação forte cria (e5.1).
- Poucas respostas falsas bastam para virar uma enquete dividida. O número exato depende do
  tamanho da turma, e é o dado que a turma leva para casa.
- **O que me faria mudar de ideia:** a turma identificar os agentes bem acima do acaso mesmo nas
  perguntas genéricas. Nesse caso, e5 está superestimado, pelo menos para respostas abertas.

---

### Ideia 3 — Feed misto

**O que é.** Uma rede social mínima, em que se pode postar, curtir e responder, e que só existe
durante o teste.

- **Quem está nela.** A turma, pelo celular, e cerca de 40 agentes com perfis gerados a partir da
  mesma distribuição da turma. Ninguém sabe quem é quem.
- **O assunto.** É semeado um tema que divide, como o uso de IA nas avaliações da universidade.
- **As rodadas.** São três rodadas de cerca de 8 minutos, cada uma com um algoritmo de feed:
  1. cronológico;
  2. por engajamento;
  3. por ponte, que destaca o que é curtido por quem discorda [12].
- **O que o app mede.** Em cada rodada, e separando humanos de agentes, o app mede toxicidade
  (com um classificador), polarização (quem curte quem) e reciprocidade (quem responde a quem).
- **No fim.** O app revela quem era agente e mostra os gráficos das três rodadas.

**A pergunta sobre o futuro.** Se plataformas passarem a testar mudanças de feed em sociedades
simuladas antes de testar em pessoas, o efeito que aparece nos agentes é o mesmo que aparece nos
humanos? (Testa e3 e, principalmente, a validade da D2, que é a raiz mais frágil do mapa [11].)

**Tecnologia emergente.** Simulação social generativa, como OASIS [7], AgentSociety [8] e os
estudos de feed de Törnberg [12][13]. **Por que não dá com tecnologia madura:** a modelagem
baseada em agentes com regras codificadas à mão não lê nem escreve posts em linguagem natural e,
por isso, não consegue dividir um feed com pessoas reais. O experimento só existe porque os
agentes conversam.

**Construção.** É a mais trabalhosa das três: exige tempo real, um loop de agentes e três
ordenações de feed. As ordenações, porém, são simples (por tempo, por curtidas e por curtidas de
quem discorda), e a escala é pequena: cerca de 70 participantes por 25 minutos. O risco técnico
é a latência e o custo de 40 agentes agindo a cada poucos segundos. Para reduzir, os agentes
agem em lotes.

**O que espero observar.**
- Agentes mais homogêneos e menos recíprocos que os humanos. Eles postam "para todos" e se
  respondem pouco, como no Moltbook [23].
- Diferenças pequenas entre os algoritmos [13], e sem o mesmo sinal em humanos e agentes.
- Humanos tratando os agentes de forma diferente sem saber que são agentes: respondendo menos a
  eles, ou curtindo mais.
- Com cerca de 30 humanos, o resultado é **ilustrativo**, não estatístico. O que conta é se a
  direção do efeito bate.
- **O que me faria mudar de ideia:** o feed por ponte ter o mesmo sinal e magnitude parecida nos
  dois grupos. Seria a primeira evidência a favor da D2 que eu mesmo produzo, e eu subiria a
  confiança de e3.

---

## 3. Comparação das três ideias

| | Ideia 1 · A turma prevista | Ideia 2 · Caça ao respondente | Ideia 3 · Feed misto |
|---|---|---|---|
| Raiz testada | D1 (populações sintéticas) | D3 (respondentes indetectáveis) | D2 (sociedades multiagente) |
| Esforço de construção | Médio | Baixo | Alto |
| Risco técnico | Baixo | Baixo | Médio (tempo real e custo) |
| Preparo antes do teste | Formulário de 1 min e entrevistas opcionais de 5 min | Nenhum | Nenhum |
| O resultado aparece na hora? | Sim, na revelação | Sim, no placar | Sim, no fim das rodadas |
| O que fica no ar depois | Qualquer grupo monta o painel da própria turma e compara | Jogo de detecção jogável sozinho, com respostas gravadas | Replay da rede e um modo só com agentes |

**Leitura.** A ideia 2 é a mais rápida e a que deve gerar mais reação em sala. A ideia 1 é a que
conversa com o centro do mapa (a variância e o dado humano). A ideia 3 é a mais original e a mais
arriscada. As ideias 1 e 2 compartilham quase toda a infraestrutura (questionário, agentes com
persona e tela de comparação). Se a ideia escolhida parecer pequena para o movimento, dá para
juntar as duas numa sessão só.
