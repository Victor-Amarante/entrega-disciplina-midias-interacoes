---
tema: "Sociedades simuladas: a simulação como instrumento de investigação"
slug: sociedades-simuladas
autor_login: vafs
zona_de_interesse: Simulação social com agentes de IA como instrumento de pesquisa em mídia, comportamento e sociedade
data: 2026-09-28
horizonte: 2031
publico: Público em geral conectado com tecnologia
recorte_geografico: global
disrupcoes_raiz: 3
efeitos_ordem_1: 6
efeitos_ordem_2: 10
efeitos_ordem_3: 10
tecnologias_citadas: [modelos de linguagem (LLMs), agentes generativos, amostras de silício, painéis sintéticos, gêmeos comportamentais de indivíduos, modelagem baseada em agentes, OASIS, AgentSociety, Concordia, Project Sid (PIANO), Centaur, Qualtrics Edge Audiences, Simile, Aaru, Moltbook, respondente sintético autônomo, painéis online opt-in, algoritmo de feed por ponte (bridging)]
fontes: 31
confianca: media
experimento: "Painel espelho — a turma contra seus próprios gêmeos sintéticos"
skill_usada: futurizacao-vafs
publico_ok: true
---

## 1. Resumo

Modelos de linguagem passaram a ser usados como "pessoas simuladas". Hoje eles respondem questionários no lugar de humanos, reproduzem indivíduos a partir de entrevistas e povoam redes sociais artificiais com milhares ou até um milhão de agentes. Isso já é mercado: Simile (US$ 2 bi de valuation em 2026), Aaru e os painéis sintéticos da Qualtrics. O mapa sai de três rupturas: populações sintéticas substituindo amostras humanas, sociedades multiagente como laboratório de política e de plataforma, e agentes que respondem pesquisas sem ser detectados. As três convergem no mesmo ponto: em 2031, a pergunta "isso foi medido em humanos?" pesa mais que a margem de erro. A leitura é cética moderada. A literatura mostra que a simulação acerta médias e erra variância, subgrupos e efeitos de tratamento. Por isso o cenário provável é de coexistência tensa, sem substituição, e o dado humano verificado fica mais escasso e mais caro.

## 2. O tema

**O que é.** Chamo de "sociedades simuladas" o uso de agentes baseados em modelos de linguagem para representar pessoas e grupos. O objetivo é estudar como esses grupos pensariam, responderiam ou agiriam. São três escalas:

- **O respondente.** Um LLM condicionado por um perfil demográfico ou por uma história de vida responde a um questionário. É a "amostra de silício" de Argyle et al. [3].
- **O indivíduo.** Um agente ancorado em uma entrevista de duas horas ou em respostas a questionários de uma pessoa real tenta prever o que aquela pessoa responderia a perguntas novas. É o "gêmeo comportamental" de Park et al. [2], hoje produto da Simile [28].
- **A sociedade.** Milhares de agentes interagem num ambiente com memória, rede social e algoritmo de recomendação, e fenômenos coletivos emergem: polarização, câmaras de eco, difusão de boatos. Exemplos são Smallville [1], OASIS [7], AgentSociety [8], Project Sid [14] e Concordia [15].

**Onde encosta em mídia e interação.** Em quatro pontos:

1. **Mídia como objeto de teste.** Algoritmos de feed, estratégias de moderação e campanhas passam a ser testados em redes simuladas antes de chegar a pessoas [12][13].
2. **Pesquisa com usuário.** UX e pesquisa de mercado já oferecem "usuários sintéticos" no lugar de entrevistas e testes [24][25][26].
3. **Pesquisa de opinião.** A pesquisa de opinião também é mídia: é notícia, move eleição e expectativa de mercado. Ela está sendo pressionada pelos dois lados. Há empresas vendendo "pesquisas" sintéticas [29][30], e há agentes capazes de se passar por respondentes humanos em pesquisas reais [19].
4. **Simulação como forma narrativa.** Mundos com agentes (Smallville, Project Sid, a rede só de agentes Moltbook [23]) são consumidos como espetáculo, e não só como ciência.

**Por que um mapa de futuro, e não um estado da arte.** O estado da arte responderia se a simulação é válida. A resposta honesta hoje é "depende da tarefa, e ninguém sabe bem onde fica o limite" [9][10][11][18]. O interessante é outra coisa: o mercado já decidiu adotar antes que a ciência decidisse se deve [28][29][26]. Quando adoção e validação andam em velocidades diferentes, os efeitos estruturais aparecem antes do veredito. Os papéis mudam (quem faz pesquisa, quem é "participante"), mudam as regras (o que conta como pesquisa, o código da AAPOR [27]) e muda a confiança pública nos números. É isso que o mapa tenta antecipar.

## 3. Onde isso está hoje

### O que já existe e funciona (com ressalvas)

- **Médias populacionais em perguntas de atitude.** Desde 2022 se mostra que LLMs condicionados por perfis reproduzem distribuições de subgrupos, a chamada "fidelidade algorítmica" [3]. Bisbee et al. confirmam que as médias de "termômetro de sentimento" do ChatGPT batem de perto com as da ANES 2016–2020 [5]. No Chile, respostas sintéticas sobre confiança institucional passam de 0,90 de acurácia e F1 [21].
- **Previsão do sinal e da ordem de grandeza de efeitos experimentais.** Hewitt, Ashokkumar, Ghezae e Willer usaram 70 experimentos de survey pré-registrados nos EUA (476 efeitos, 105.165 participantes). Nesse arquivo, previsões simuladas com GPT-4 correlacionam r = 0,85 com os efeitos reais, com precisão parecida com a de previsores humanos agregados [17].
- **Economia comportamental clássica.** Horton, Filippas e Manning reproduzem qualitativamente experimentos como Charness & Rabin (2002), Kahneman et al. (1986) e Samuelson & Zeckhauser (1988) com "Homo silicus" [4].
- **Gêmeos de indivíduos.** Agentes ancorados em entrevistas e surveys de 1.052 norte-americanos chegam a 83–86% do limite de consistência teste-reteste das próprias pessoas. A linha de base só com dados demográficos fica em 74%. A disparidade de acurácia entre grupos raciais e ideológicos também cai [2]. A NN/g resume estudos parecidos: gêmeos com 78% de acurácia em dados faltantes e 67% em perguntas novas, e correlação de r = 0,98 em efeitos populacionais [24].
- **Modelos de cognição.** O Centaur (Llama 3.1 70B ajustado no Psych-101, com 160 experimentos, 60.092 participantes e 10,68 milhões de escolhas) prevê comportamento em tarefas cognitivas melhor que modelos de domínio e generaliza para tarefas novas [16].
- **Sociedades em escala.** O OASIS simula até um milhão de agentes em plataformas modeladas a partir do X e do Reddit, e reproduz difusão de informação, polarização de grupo e efeito manada [7]. O AgentSociety simula mais de 10 mil agentes e 5 milhões de interações, e estuda polarização, mensagens inflamatórias, renda básica e choques externos como furacões [8]. O Project Sid põe de 10 a mais de 1.000 agentes no Minecraft, onde surgem papéis especializados, regras coletivas e transmissão "religiosa" [14]. O Smallville, com 25 agentes, coordena uma festa a partir de uma única instrução [1].
- **Plataformas simuladas como laboratório de mídia.** Um feed por "ponte", que destaca o que é curtido por quem pensa diferente, gera conversa menos tóxica entre polos numa rede simulada [12]. Um estudo seguinte testou seis intervenções pró-sociais, entre elas feed cronológico e ponte. As melhorias foram modestas e às vezes houve piora, o que sugere que o problema está na arquitetura das plataformas [13].

### O que existe e não funciona (ou não funciona ainda)

- **Variância.** A distribuição sintética é comprimida: há menos variação que em surveys reais, e coeficientes de regressão diferem significativamente dos da ANES [5]. Usuários sintéticos da NN/g também mostram variabilidade menor que a humana [24]. O exemplo típico: aprendizes reais abandonam cursos, e os sintéticos dizem que terminaram todos.
- **Reprodutibilidade.** A mesma instrução gerou resultados significativamente diferentes num intervalo de três meses, e pequenas mudanças de redação mudam a distribuição [5].
- **Identidade e grupos minoritários.** LLMs retratam grupos demográficos de forma errada e achatada. O estudo teve 3.200 participantes humanos, 16 identidades e 4 modelos [6]. As técnicas de mitigação reduzem o problema, mas não o eliminam.
- **Viés WEIRD e viés de idade.** O próprio Centaur admite viés forte para populações ocidentais, escolarizadas, industrializadas, ricas e democráticas [16]. No caso chileno, o alinhamento é máximo na faixa de 45 a 59 anos e pior nas outras [21].
- **Realismo não é validade causal.** Li & Ji mostram, com 59.508 participantes em 62 países, que parecer estatisticamente realista tem correlação fraca com acertar efeitos de tratamento. Otimizar realismo chegou a piorar a estimativa de efeito [18].
- **Colapso de persona.** Em tarefas de raciocínio, o GPT-5 abandona as personas e converge para uma identidade "ótima". O Claude Sonnet 4.5 mantém alguma variação. Em tarefas afetivas, os três modelos testados preservam diferenças [22].
- **Validação de sociedades simuladas.** A revisão crítica de Larooij & Törnberg conclui que a literatura de ABM generativo ignora debates históricos de validação. Muitos estudos se apoiam em "credibilidade" subjetiva, e mesmo os melhores não demonstram validade operacional [11].
- **Redes só de agentes.** O Moltbook, rede social povoada por agentes, é mais homogêneo, menos coerente e tem trocas de difusão, menos recíprocas que as do Reddit [23]. Uma sociedade artificial não se organiza como uma humana só porque tem muitos agentes.
- **Previsão eleitoral.** Na véspera da eleição de 2024, a Aaru apontava Harris à frente em Michigan, Nevada, Pensilvânia e Wisconsin. Depois disse que o resultado estava "dentro da margem de erro", conceito que não se aplica a amostra sintética [30].

### Quem está construindo

- **Academia.** Stanford (Park, Bernstein, Liang, Willer [1][2][17]), BYU (Argyle et al. [3]), MIT/Horton [4], Helmholtz Munich (Binz et al. [16]), Tsinghua e colaboradores (AgentSociety [8]), um consórcio de laboratórios em torno do CAMEL/OASIS [7] e a Universidade de Amsterdã (Törnberg [11][12][13]).
- **Empresas.** A Simile (fundada por Park, Bernstein, Liang e Yallen) levantou US$ 100 mi em fevereiro de 2026 e US$ 200 mi em julho de 2026, com valuation de US$ 2 bi. Os clientes incluem CVS Health, Wealthfront, Deloitte e **Gallup**, um instituto de pesquisa tradicional [28]. A Aaru levantou mais de US$ 50 mi com valuation "de manchete" de US$ 1 bi em dezembro de 2025, com ARR abaixo de US$ 10 mi e clientes como Accenture, EY, Interpublic e campanhas políticas [29]. A Qualtrics lançou o Edge Audiences em março de 2025 [25] e ampliou os painéis sintéticos em março de 2026, dizendo ter "12 vezes mais acurácia que LLMs genéricos" [26]. A Altera fez o Project Sid [14].
- **Ferramentas abertas.** Concordia [15], OASIS [7] e AgentSociety [8].
- **Normas.** Desde junho de 2026, o código de ética da AAPOR diz que respostas geradas por IA ("silicon responses, digital twins, synthetic responses") **não são participantes de pesquisa** e precisam ser identificadas. Amostras mistas também precisam ser declaradas [27].
- **O lado adversarial.** Westwood (Dartmouth) construiu um respondente sintético autônomo que passa em 99,8% de 6.000 checagens de atenção. Cada resposta custa cerca de US$ 0,05, e bastariam de 10 a 52 respostas falsas para inverter a previsão de grandes pesquisas de 2024 [19]. Painéis como a Verasight respondem com verificação por telefone, cruzamento com cadastro eleitoral e localização [20].

## 4. As disrupções-raiz

As três disrupções abaixo passaram pelos três testes da skill: maduro, emergente e disruptivo. As tecnologias rejeitadas estão registradas no anexo (seção 12), com o motivo.

### D1 — Populações sintéticas como substituto de amostra humana

*Painéis sintéticos e gêmeos comportamentais de indivíduos.*

- **Teste 1 (madura?).** Não. Existem implantações comerciais (Qualtrics [25][26], Simile com a CVS [28], Aaru [29]), mas nenhuma é o padrão de um fluxo inteiro. O que existe é early access, pilotos e uso exploratório. A Qualtrics só previa disponibilidade geral para o fim de 2025 [25], e só nos EUA na virada de 2026 [26].
- **Teste 2 (emergente?).** Sim. Já saiu do laboratório, com clientes pagantes e rodadas de US$ 100–200 mi, mas a adoção ainda é de early adopters. O próprio campo acadêmico reconhece que a adoção entre cientistas sociais é baixa [9].
- **Teste 3 (disruptiva?).** Sim. Se escalar, **deixa de fazer sentido o painel online pago para estudo exploratório**, o de concept test, mensagem e grupo focal rápido. E deixa de fazer sentido a premissa de que é preciso perguntar à pessoa para saber o que ela responderia. O "participante" deixa de ser quem responde e vira quem **fornece a matriz** de um modelo.
- **Por que agora e não há cinco anos.** Em 2021 não havia modelos capazes de sustentar persona com coerência. A fidelidade algorítmica só foi demonstrada em 2022 [3], os gêmeos ancorados em entrevista em 2024 [2], e o capital só entrou em escala entre 2025 e 2026 [28][29].
- **O que ainda falta.** Falta resolver três problemas: a compressão de variância [5][24], o erro em subgrupos [6][21] e a divergência entre realismo e efeito causal [18]. Falta também um protocolo de validação aceito, que a AAPOR ainda não tem; o código dela só exige rotular [27]. E falta provar que o gêmeo continua fiel com o tempo, já que as pessoas mudam.

### D2 — Sociedades multiagente generativas como laboratório de intervenção

- **Teste 1 (madura?).** Não. Nenhuma plataforma ou governo usa, até onde as fontes lidas mostram, simulação generativa como etapa padrão de decisão.
- **Teste 2 (emergente?).** Passa, mas **por pouco**. As ferramentas são abertas e usadas fora do laboratório de origem (Concordia [15], OASIS [7], AgentSociety [8]), e o Concordia foi desenhado também para "avaliação de serviços digitais" [15]. Mas o uso ainda é quase só acadêmico. Registro esta fragilidade: a D2 é a raiz com menor confiança.
- **Teste 3 (disruptiva?).** Sim. Se escalar, perdem a razão de existir duas coisas. Uma é a modelagem baseada em agentes com regras codificadas à mão como principal forma de simular sociedade. A outra é a necessidade de testar mudanças de desenho em populações humanas reais (A/B test em escala) como **primeira** etapa. A pergunta "o que acontece se mudarmos o feed?" passa a ter uma resposta preliminar antes de envolver pessoas.
- **Por que agora.** A escala só ficou viável recentemente, e a custo acadêmico: um milhão de agentes [7], 5 milhões de interações [8]. Os primeiros estudos de algoritmo de feed com agentes são de 2023 [12] e 2025 [13].
- **O que ainda falta.** Falta validade operacional [11]. Há a caixa-preta: não dá para explicar o mecanismo causal que emerge [11]. E as redes só de agentes não se organizam como as humanas [23]. Sem isso, a D2 fica como ferramenta de ilustração, e não de decisão (ver seção 7).

### D3 — Agentes autônomos indistinguíveis de respondentes humanos

- **Teste 1 (madura?).** Não. A capacidade foi demonstrada em 2025 [19], mas não há evidência pública de uso em escala para fraude.
- **Teste 2 (emergente?).** Sim. Custa cerca de US$ 0,05 por resposta, precisa de uma instrução de uns 500 palavras e usa modelos comerciais [19]. A barreira de entrada é mínima. Os painéis já reagem [20], o que indica que a ameaça é tratada como real.
- **Teste 3 (disruptiva?).** Sim. Perde o sentido a premissa de que **uma resposta coerente é uma resposta humana** [19]. Com ela vai o painel online opt-in não verificado como instrumento de medida confiável.
- **Por que agora.** Os bots antigos erravam checagens de atenção. Agentes com LLM passam em 99,8% delas e acertam 0% das perguntas-armadilha sobre eventos impossíveis. O erro nesse tipo de pergunta era justamente o que denunciava bots [19].
- **O que ainda falta.** Falta evidência de exploração real e sistemática, e falta saber se a verificação forte [20] fecha a porta ou só encarece o ataque.

**Nota.** A D3 é o espelho escuro da D1. É a mesma capacidade técnica, usada para contaminar a coleta humana em vez de substituí-la. Juntas, elas empurram o dado humano verificado para a escassez (efeitos e1.1.1 e e5.1.1).

## 5. A roda dos futuros

```yaml
roda:
  - disrupcao: Populações sintéticas como substituto de amostra humana (painéis sintéticos e gêmeos comportamentais)
    efeitos:
      - id: e1
        ordem: 1
        efeito: Pesquisa exploratória de conceito, mensagem e produto passa a rodar primeiro em respondentes sintéticos e só depois, se rodar, em humanos
        sinal: forte
        prazo: 2028
        confianca: media
        efeitos:
          - id: e1.1
            ordem: 2
            efeito: O painel online pago de baixo custo perde o mercado de estudos rápidos e se reposiciona como fornecedor de dados humanos de calibração para modelos
            sinal: medio
            prazo: 2029
            confianca: media
            efeitos:
              - id: e1.1.1
                ordem: 3
                efeito: Resposta humana verificada vira insumo escasso e caro, tratada como dado de treino premium e não como produto final de pesquisa
                sinal: fraco
                prazo: 2031
                confianca: baixa
          - id: e1.2
            ordem: 2
            efeito: Decisões de produto e de mídia passam a se apoiar em distribuições de opinião comprimidas, com menos variância que a população real
            sinal: medio
            prazo: 2029
            confianca: media
            efeitos:
              - id: e1.2.1
                ordem: 3
                efeito: Produtos e campanhas testados em populações sintéticas convergem para o gosto médio e o público de nicho passa a ser descoberto só depois do lançamento
                sinal: fraco
                prazo: 2031
                confianca: baixa
      - id: e2
        ordem: 1
        efeito: Gêmeos comportamentais construídos a partir de entrevistas passam a ser consultados no lugar de clientes, pacientes e funcionários em decisões corporativas
        sinal: medio
        prazo: 2029
        confianca: media
        efeitos:
          - id: e2.1
            ordem: 2
            efeito: A entrevista qualitativa longa vira método de captura de matriz para gêmeos, e o participante passa a ceder um modelo de si em vez de uma resposta
            sinal: medio
            prazo: 2030
            confianca: media
            efeitos:
              - id: e2.1.1
                ordem: 3
                efeito: Surge um regime de consentimento e remuneração pelo uso continuado do gêmeo, análogo ao direito de imagem
                sinal: fraco
                prazo: 2031
                confianca: baixa
          - id: e2.2
            ordem: 2
            efeito: Grupos sub-representados nos dados de treino são simulados com mais erro e, por já estarem simulados, são menos consultados diretamente
            sinal: medio
            prazo: 2030
            confianca: media
            efeitos:
              - id: e2.2.1
                ordem: 3
                efeito: Organizações de grupos minoritários passam a exigir consulta humana obrigatória em decisões públicas que os afetam, recusando representação sintética
                sinal: fraco
                prazo: 2031
                confianca: baixa
  - disrupcao: Sociedades multiagente generativas como laboratório de intervenção em plataformas e políticas
    efeitos:
      - id: e3
        ordem: 1
        efeito: Mudanças em algoritmos de feed e moderação passam a ser pré-testadas em redes sociais simuladas antes do teste A/B com pessoas
        sinal: medio
        prazo: 2029
        confianca: media
        efeitos:
          - id: e3.1
            ordem: 2
            efeito: Avaliações de risco de plataformas passam a citar simulações como evidência, o que abre disputa pública sobre como validá-las
            sinal: fraco
            prazo: 2030
            confianca: baixa
            efeitos:
              - id: e3.1.1
                ordem: 3
                efeito: Surge uma prática de auditoria independente de simuladores sociais com protocolos de validação padronizados
                sinal: fraco
                prazo: 2031
                confianca: baixa
          - id: e3.2
            ordem: 2
            efeito: Resultados de simulação mostrando que ajustes de feed mudam pouco deslocam o debate de reforma do algoritmo para a arquitetura da plataforma
            sinal: fraco
            prazo: 2030
            confianca: baixa
            efeitos:
              - id: e3.2.1
                ordem: 3
                efeito: Plataformas sociais novas nascem com um gêmeo social rodando continuamente como banco de testes de decisões de desenho
                sinal: fraco
                prazo: 2031
                confianca: baixa
      - id: e4
        ordem: 1
        efeito: Estudos exploratórios de política pública trocam agentes de regras codificadas à mão por agentes em linguagem natural
        sinal: medio
        prazo: 2028
        confianca: media
        efeitos:
          - id: e4.1
            ordem: 2
            efeito: A ciência social computacional se divide entre simulação exploratória, aceita sem validação forte, e simulação preditiva, que exige validação operacional
            sinal: medio
            prazo: 2030
            confianca: media
            efeitos:
              - id: e4.1.1
                ordem: 3
                efeito: A simulação generativa passa a circular também como gênero de mídia para o público, narrativa de futuros possíveis consumida como se fosse evidência
                sinal: fraco
                prazo: 2031
                confianca: baixa
  - disrupcao: Agentes autônomos indistinguíveis de respondentes humanos em pesquisas online
    efeitos:
      - id: e5
        ordem: 1
        efeito: Pesquisa online opt-in sem verificação de identidade deixa de ser aceita como medida confiável porque resposta coerente deixa de provar humanidade
        sinal: forte
        prazo: 2027
        confianca: alta
        efeitos:
          - id: e5.1
            ordem: 2
            efeito: Painéis migram para verificação forte de identidade e localização, o que encarece a coleta e exclui quem não pode ou não quer se identificar
            sinal: medio
            prazo: 2028
            confianca: media
            efeitos:
              - id: e5.1.1
                ordem: 3
                efeito: Amostragem probabilística verificada volta a ser padrão-ouro, e medir opinião pública com qualidade fica caro a ponto de se concentrar em poucas instituições
                sinal: fraco
                prazo: 2031
                confianca: baixa
          - id: e5.2
            ordem: 2
            efeito: A exigência de rotular dados sintéticos sai dos códigos de ética associativos e entra em regras legais de divulgação de pesquisas eleitorais
            sinal: medio
            prazo: 2029
            confianca: media
            efeitos:
              - id: e5.2.1
                ordem: 3
                efeito: Pesquisa de opinião se divide publicamente em dois produtos com graus de confiança distintos e o público pergunta se o dado é humano antes de perguntar a margem de erro
                sinal: fraco
                prazo: 2031
                confianca: baixa
      - id: e6
        ordem: 1
        efeito: Atores interessados passam a manipular pesquisas publicadas injetando respondentes sintéticos baratos
        sinal: medio
        prazo: 2028
        confianca: media
        efeitos:
          - id: e6.1
            ordem: 2
            efeito: Pesquisas publicadas perdem peso na formação de expectativas eleitorais e de mercado
            sinal: fraco
            prazo: 2030
            confianca: baixa
            efeitos:
              - id: e6.1.1
                ordem: 3
                efeito: Mercados de previsão e simulações proprietárias ocupam o espaço de termômetro público deixado pelas pesquisas
                sinal: fraco
                prazo: 2031
                confianca: baixa
```

### O que o bloco não consegue dizer

**Efeitos cruzados.** A roda é uma árvore, mas o mapa real é uma rede. Três cruzamentos importam:

- **e1.1.1 e e5.1.1 são o mesmo efeito por caminhos diferentes.** Pela D1, o dado humano fica escasso porque o mercado deixa de comprá-lo como produto. Pela D3, fica escasso porque passa a exigir verificação cara. É o achado central do mapa: **a simulação e a fraude sintética empurram na mesma direção**. O dado humano verificado se valoriza e se concentra.
- **Há um laço de contaminação.** A D1 depende de dados humanos para calibrar gêmeos. A D3 contamina esses dados, porque respondentes sintéticos entram em painéis humanos. Se painéis contaminados alimentarem o treino de gêmeos, o sistema passa a simular simulações. Não pus isso na roda porque não achei evidência de que já aconteça. Está na seção 6 como sinal fraco.
- **e6.1.1 depende de e1.** Simulações proprietárias só ocupam o espaço das pesquisas se a D1 tiver ganhado credibilidade. Se a D1 estagnar, e6.1.1 cai para mercados de previsão apenas.

**Auditoria da Fase 4 (o que mudou na roda).**

- **e1** teve a confiança **rebaixada de alta para média**. É em boa parte extrapolação linear do que Qualtrics, Aaru e Simile já fazem [25][26][28][29]. Vai para a seção 7.
- **e2** teve o prazo **adiado de 2028 para 2029**. A versão original supunha uma adoção de gêmeos individuais mais rápida do que a de qualquer mudança de método de pesquisa de que eu tenha evidência. Vai para a seção 7.
- **e5.2 foi reescrito.** A versão original dizia "distinguir pesquisa humana de sintética vira exigência ética". Isso **já aconteceu** em junho de 2026 com a AAPOR [27], então não é efeito futuro, é presente. A versão final projeta o passo seguinte, a migração para a regra legal.
- **e3.1** teve a confiança **rebaixada de média para baixa**. O elo pulava uma etapa: nada nas fontes mostra regulador aceitando simulação como evidência.
- **e4** foi mantido com sinal médio, com uma ressalva. Troca de ABM clássico por generativo é o que a literatura já faz [7][8][15], mas a revisão crítica [11] diz que isso não resolve os problemas do ABM. O efeito é a troca de ferramenta, não a melhora de validade.
- **e5** foi mantido com confiança alta. É o único efeito com demonstração empírica direta [19] e reação de mercado já visível [20]. Mesmo assim, "deixa de ser aceita" é mais forte que "deixa de ser confiável", e essa diferença de prazo entre o problema técnico e a reação institucional pode ser grande.
- **Cinco efeitos foram cortados** (detalhes na seção 12). "Institutos de pesquisa tradicionais fecham" foi contrariado pela evidência: o Gallup é cliente da Simile [28]. "Governos simulam a população antes de cada lei" não tinha elo causal. "Agentes votam ou representam cidadãos" é ficção genérica. "Centaur substitui experimentos de psicologia" é especulação e foi para a seção 6. "Gêmeos sintéticos substituem ensaios clínicos" está fora do recorte e sem evidência.
- **Todos os efeitos de 3ª ordem estão com confiança baixa.** Era o esperado.

**Sobre o viés cético moderado.** Nos pontos ambíguos, escolhi a leitura cética. Onde a evidência mostra acerto em médias e erro em variância, derivei efeitos do erro de variância (e1.2, e2.2), e não do acerto na média. Com viés otimista, o ramo e1.2 seria "decisões ficam mais rápidas e baratas", e a D2 teria confiança maior.

## 6. Sinais fracos e wildcards

### Sinais fracos

- **Redes só de agentes (Moltbook).** Uma rede social inteira povoada por agentes já existe e foi estudada [23]. Hoje ela é mais homogênea e menos recíproca que o Reddit. Se passar a reproduzir a organização humana, a D2 ganha um laboratório "natural" e barato. Se continuar diferente, vira evidência forte contra a D2.
- **Modelos-fundação de comportamento humano.** O Centaur [16] foi rejeitado como raiz porque ainda não passa do teste 2 (ver seção 12). Mesmo assim, é o sinal de que a simulação pode deixar de ser "LLM genérico com persona" e passar a ser "modelo treinado em dados comportamentais". O preprint "Small Foundation Models of Human Cognition and Behaviour" (arXiv 2608.05224) apareceu na busca, mas **não foi lido** e não entra como fonte.
- **Laço de contaminação.** Respondentes sintéticos entrando em painéis humanos [19] cujos dados depois calibram gêmeos [2][26]. Nenhuma fonte lida mostra isso acontecendo. Mas nada impede, e a detecção atual falha [19].
- **Pesquisas híbridas não declaradas.** Em março de 2026, o Public Sentiment Institute misturou 373 respondentes reais com 114 agentes sem declarar com clareza [30]. É um caso isolado, mas é exatamente o comportamento que a AAPOR proibiu três meses depois [27].
- **Colapso de persona dependente do modelo.** Modelos mais recentes colapsam personas em tarefas de raciocínio [22]. Se o alinhamento dos modelos de fronteira empurrar para uma "identidade ótima", a simulação de diversidade pode **piorar** com modelos melhores. Isso inverte a premissa de que a D1 melhora com o tempo.

### Wildcards (baixa probabilidade, alto impacto)

- **W1 — A simulação acerta um choque eleitoral grande que as pesquisas humanas erraram**, de forma pública, pré-registrada e verificável. Se isso acontecer antes de 2031, a D1 salta anos de adoção de uma vez. A simulação passa a ser tratada como oráculo e e6.1.1 vira efeito de 1ª ordem. O mapa inteiro se desloca para o otimista.
- **W2 — Uma política pública desenhada com base em simulação dá errado de forma visível**, com dano real atribuído ao modelo. Pode ser uma política de renda básica, de resposta a desastre ou de moderação testada em algo como o AgentSociety [8]. Se acontecer, a D2 congela e surge regulação restritiva de simulação em decisões públicas.
- **W3 — Proibição legal de pesquisas sintéticas em período eleitoral** em alguma grande democracia. Isso tiraria a Aaru e similares [29] do mercado político e aceleraria e5.2.
- **W4 — Escândalo de gêmeo não consentido.** Alguém descobre que o próprio gêmeo comportamental foi construído e consultado sem autorização. Isso aceleraria e2.1.1 de forma brusca.

## 7. Contra o próprio mapa

Esta seção vem da auditoria da Fase 4 (seção 5), não de um exercício genérico.

### Efeitos que são só extrapolação linear

- **e1** ("pesquisa exploratória roda primeiro em sintéticos") é a curva de hoje mais longa. A Qualtrics já vende isso [25][26], a Simile já tem a CVS no lugar de grupos focais [28] e a Aaru já vende a campanhas [29]. Não é futurização, é projeção. Mantive porque é a base de e1.1 e e1.2, mas com confiança rebaixada.
- **e4** (troca de ABM clássico por generativo) também é o que a literatura acadêmica já faz [7][8][13][15]. O efeito interessante está em e4.1, não em e4.

### Efeitos que assumem adoção sem precedente

- **e2** supõe que empresas passem a consultar gêmeos individuais no lugar de pessoas até 2029. O caso comparável seria a migração de pesquisa por telefone para painel online, mas **não li fonte que date essa migração**, então não cito números. O que sei das fontes: a Simile tem cerca de sete meses de operação pública e quatro clientes nomeados [28]. Extrapolar isso para "prática corrente" em três anos exige mais velocidade do que qualquer mudança metodológica em pesquisa de que eu tenha evidência. Adiei o prazo, mas o efeito continua otimista em velocidade.
- **e5** diz que o opt-in não verificado "deixa de ser aceito" até 2027. A demonstração técnica é de novembro de 2025 [19], mas instituições de medida costumam reagir devagar. É possível que o problema continue conhecido e ignorado até um escândalo (W3) forçar a mudança.
- **e3.2.1** (plataformas nascem com um gêmeo social) supõe que simulações ganhem credibilidade para decisão de produto. Hoje nem os melhores estudos demonstram validade operacional [11].

### Disrupção que pode simplesmente não se concretizar

- **A D2 é a mais frágil.** Passou no teste 2 por pouco. Se a validade operacional nunca vier [11], as sociedades simuladas continuam como ilustração: bonitas, citáveis e sem peso de decisão. Nesse caso todo o ramo e3 cai. Resta só e4.1.1, a simulação como gênero de mídia. **Um resultado contrário ao meu próprio mapa:** se a D2 falhar como ciência, e4.1.1 fica **mais** provável. Simulação sem validade que circula como evidência é exatamente o cenário indesejável.
- **A D1 pode estagnar** se o resultado de Li & Ji [18] se generalizar. Realismo que não prevê efeito de tratamento serve para "como as pessoas respondem", mas não para "o que acontece se fizermos X", que é o que as empresas compram. Nesse caso, e1 continua, mas e2 e o ramo de gêmeos regridem para nicho.

### Vieses que entraram aqui

- **Viés de quem escolheu o tema.** O tema foi escolhido por interesse, e a zona de interesse é mídia e interação. Isso me puxou para as aplicações em mídia (feeds, pesquisa de opinião como mídia) e deixou de fora saúde, defesa e planejamento urbano, onde a simulação pode estar mais avançada.
- **Viés de quem escreveu.** O mapa foi gerado por um LLM (Claude) sobre o uso de LLMs para simular pessoas. É a ferramenta analisando a si mesma. Um erro previsível é superestimar a capacidade técnica e subestimar a resistência institucional. Tentei compensar com o viés cético declarado, mas não tenho como garantir que compensei.
- **Viés de fonte.** Quase tudo é anglófono e dos EUA (ANES, GSS, empresas americanas). O único caso fora dos EUA e da Europa é o Chile [21]. O recorte é "global", mas a evidência é norte-americana. Os efeitos e5 e e6 dependem da estrutura de pesquisa eleitoral dos EUA e podem não valer em países com regime diferente de registro e divulgação de pesquisas.
- **Viés de disponibilidade.** Várias fontes são preprints revisados em 2026 [2][4][8][18], e os números mudam entre versões (ver seção 8). O "estado atual" da seção 3 é um alvo em movimento.

## 8. O que a máquina errou

Registro dos erros da IA (eu, e as ferramentas de busca e resumo que usei) que a verificação pegou.

1. **Título e números trocados no estudo dos 1.000 gêmeos.** De memória, eu citaria Park et al. como "Generative Agent Simulations of 1,000 People", com agentes que replicam respostas do GSS "85% tão bem quanto as próprias pessoas". A versão atual no arXiv, revisada em 28/06/2026, se chama "LLM Agents Grounded in Self-Reports Enable General-Purpose Simulation of Individuals" e reporta 83% (só entrevista), 82% (só survey), 86% (combinado) e 74% (só demografia) do limite de teste-reteste [2]. **Como percebi:** li o abstract atual antes de citar. O número de memória era redondo demais e não batia com nenhuma das quatro condições. Usei os números da versão lida.
2. **Autoria do "Homo silicus".** De memória, eu atribuiria o paper só a John Horton. A versão lida, revisada em fevereiro de 2026, lista Horton, Filippas e Manning [4]. **Como percebi:** conferência direta da página.
3. **A ferramenta de busca misturou dois estudos.** O resumo automático sobre Hewitt et al. incluiu "276 experimentos de campo com 78% de acurácia", que não aparece na página do projeto em Stanford. Esse dado parece vir de outro trabalho, sobre experimentos de campo em economia. O mesmo resumo dava 469 efeitos e 119.330 participantes, e a página de Stanford diz 476 efeitos e 105.165 participantes [17]. **Como percebi:** pedi explicitamente à página se "276" e "78%" apareciam, e não apareciam. Uso os números da página lida. A divergência 469/476 pode vir de versões diferentes (preprint ou Nature), mas não verifiquei qual.
4. **Afirmação de acerto eleitoral sem fonte (Aaru).** A matéria do 36kr diz que a Aaru previu "a primária democrata de 2024 no estado de Nova York com diferença de menos de 371 votos" [31]. A matéria não traz link nem verificação independente, alterna entre "371" e "menos de 400" votos no mesmo texto e é declaradamente promocional. **Motivo da desconfiança:** número preciso demais, sem fonte e inconsistente no próprio texto. Não uso como evidência de acerto. Uso como exemplo de como a narrativa comercial da D1 circula.
5. **A ferramenta fundiu 2025 e 2026 na Qualtrics.** O resumo da busca juntou o lançamento do Edge em março de 2025 [25] com as afirmações de março de 2026 ("200 milhões de respondentes", "12x mais acurácia") [26], como se fossem um anúncio só. Pela página de 2025, o Edge Audiences estava em early access, com disponibilidade geral prevista para o fim de 2025. **Como percebi:** li as duas páginas separadamente e as datas não batiam.
6. **Afiliação do Concordia.** Eu escreveria de memória que o Concordia é do Google DeepMind. A página que li lista os autores, mas **não** a instituição [15]. Não afirmo a afiliação no texto.
7. **Os cinco desafios de Anthis et al.** O paper diz ter "cinco desafios tratáveis", mas a página lida não os enumera [9]. A tentação de preencher a lista de forma plausível foi grande. Não preenchi.
8. **"12 vezes mais acurácia" (Qualtrics).** Não é erro da máquina, mas é o tipo de número que ela repetiria sem crítica. É uma afirmação de marketing sem método publicado na matéria lida [26]. Aparece no texto só como afirmação da empresa.

## 9. Três cenários para 2031

**Provável.** Em 2031, quase toda pesquisa de mercado exploratória começa em populações sintéticas. Concept test, teste de mensagem e triagem de ideias raramente passam por um humano na primeira rodada. Os grandes institutos não morreram: absorveram a tecnologia, como o Gallup já sinalizava ao virar cliente da Simile em 2026. Agora vendem um pacote híbrido em que o painel humano verificado é a parte cara, pequena e usada para calibrar. A pesquisa eleitoral publicada precisa declarar se houve componente sintético, em código de ética e, em alguns países, em lei. Painéis online opt-in sem verificação perderam credibilidade depois de dois ou três episódios de contaminação. Sociedades simuladas com milhares de agentes aparecem em artigos, relatórios de ONGs e matérias de jornal, mas nenhuma plataforma ou governo admite ter tomado uma decisão grande com base nelas. A disputa de validação continua aberta. O público conectado já se acostumou a perguntar "isso foi com gente de verdade?".

**Desejável.** Em 2031, a simulação virou o que a literatura crítica pedia: um instrumento **exploratório com escopo declarado**. Serve para gerar hipóteses, pilotar questionários e testar desenhos antes de gastar dinheiro e tempo de pessoas, e é sempre validada contra dados humanos pré-registrados antes de virar decisão. Existem benchmarks públicos de validação por subgrupo, inclusive fora dos EUA, e os provedores publicam onde seus modelos erram. Quem cede uma entrevista para virar gêmeo assina um consentimento específico, pode revogá-lo e é remunerado por uso. Para chegar aqui, três coisas teriam de ter acontecido entre 2026 e 2029. Associações como a AAPOR teriam de ter passado de "rotular" para "validar", com protocolo mínimo. Financiadores públicos de pesquisa teriam de ter pago por bases humanas abertas e diversas para calibração, e não só as empresas. E plataformas teriam de ter aberto dados para que simulações de feed pudessem ser confrontadas com efeitos reais.

**Indesejável.** Em 2031, pesquisas sintéticas baratas e pesquisas humanas contaminadas por agentes são indistinguíveis para quem lê a notícia. A opinião pública medida virou mercadoria disputada: cada campanha tem sua simulação favorável, e ninguém sabe o que os eleitores de fato pensam. Grupos minoritários, mal representados nos modelos, deixaram de ser consultados porque "já foram simulados". Decisões de produto e de mídia calibradas em populações de variância comprimida produziram uma cultura mais homogênea. Medir opinião com qualidade ficou tão caro que só governos e grandes plataformas conseguem, e esses atores têm interesse no resultado. **Sinal precoce:** pesquisas híbridas sem declaração clara aparecendo em veículos de grande circulação, como o caso do Public Sentiment Institute em março de 2026. Outro sinal seria uma empresa de simulação dizendo acertar uma eleição "dentro da margem de erro".

## 10. O experimento

**O que é.** *Painel espelho: a turma contra seus próprios gêmeos sintéticos.* Cada aluno que aceitar dá uma entrevista curta, de 15 a 20 minutos, a um agente de IA sobre hábitos de mídia, confiança em fontes e uso de redes. Com a transcrição, cada entrevista vira um gêmeo, um LLM ancorado na entrevista, no estilo de Park et al. [2] em miniatura. Também se monta um painel sintético "demográfico", condicionado só a idade, curso e cidade, como linha de base. Depois, **turma, gêmeos e painel demográfico respondem ao mesmo questionário novo**, com três partes:

1. Perguntas de atitude sobre mídia.
2. Um pequeno experimento de enquadramento, em que metade vê uma manchete com enquadramento A e metade com B.
3. Duas perguntas abertas.

Por fim, a turma tenta identificar quais respostas abertas são humanas e quais são sintéticas.

**Que pergunta sobre o futuro ele ajuda a responder.** Onde a população sintética erra: na média, na variância, no subgrupo ou no efeito de tratamento? E uma resposta coerente ainda permite distinguir humano de máquina? A primeira pergunta testa a D1 (e1.2 e e2.2). A segunda testa a D3 (e5).

**Que tecnologia emergente ele usa, e por que não dá com tecnologia madura.** Usa agentes ancorados em entrevista, os gêmeos comportamentais. Um formulário online ou um modelo estatístico clássico não prevê a resposta de um indivíduo a uma pergunta que ele nunca viu, a partir de uma conversa livre. É exatamente isso que o gêmeo promete e o que se quer testar. Também não dá para fazer o teste de detecção sem um gerador de respostas abertas plausíveis.

**O que a turma vai fazer quando testar isso em sala.**

1. Dar a entrevista, de forma opcional e anonimizada.
2. Responder ao questionário novo.
3. Ver lado a lado a distribuição humana, a dos gêmeos e a do painel demográfico, com histogramas, desvio-padrão e o efeito de enquadramento em cada grupo.
4. Jogar o teste de detecção.
5. Discutir se aceitariam que uma empresa ou campanha consultasse seus gêmeos no lugar delas (e2.1.1).

**O que seria um resultado que me faria mudar de ideia.**

- Os gêmeos reproduzem a **variância** da turma, com desvio-padrão próximo do humano, e o efeito de enquadramento com sinal e magnitude corretos. Nesse caso, meu ceticismo sobre e1.2 estava exagerado. Rebaixo o ramo e1.2 e aumento a confiança em e2.
- A turma identifica as respostas sintéticas bem acima do acaso. Nesse caso, D3 e e5 estão superestimados, pelo menos para respostas abertas em contexto conhecido.
- O painel só demográfico empata com os gêmeos. Nesse caso, o valor da entrevista longa, que sustenta e2.1, não aparece em população homogênea, e o ramo de gêmeos perde força.

## 11. Fontes

Todas foram abertas nesta sessão, pela página do resumo, pela página do periódico, pelo PMC ou pela matéria.

1. **Park, O'Brien, Cai, Morris, Liang, Bernstein — "Generative Agents: Interactive Simulacra of Human Behavior" (2023).** https://arxiv.org/abs/2304.03442 — Sustenta: Smallville, 25 agentes, comportamento coletivo emergente (a festa). Confiabilidade: alta. É um trabalho fundador e muito citado, mas a evidência de "credibilidade" é avaliação subjetiva, exatamente o que [11] critica.
2. **Park, Zou, Kamphorst, Egan, Shaw, Hill, Cai, Morris, Liang, Willer, Bernstein — "LLM Agents Grounded in Self-Reports Enable General-Purpose Simulation of Individuals" (2024, rev. 06/2026).** https://arxiv.org/abs/2411.10109 — Sustenta: gêmeos de 1.052 pessoas, 83–86% do teste-reteste, redução de disparidade entre grupos. Confiabilidade: alta como dado, mas os autores fundaram a Simile [28]. Há conflito de interesse a considerar.
3. **Argyle, Busby, Fulda, Gubler, Rytting, Wingate — "Out of One, Many: Using Language Models to Simulate Human Samples" (2022).** https://arxiv.org/abs/2209.06899 — Sustenta: os conceitos de fidelidade algorítmica e amostras de silício. Confiabilidade: alta. É um trabalho fundador feito com GPT-3, e os modelos mudaram muito desde então.
4. **Horton, Filippas, Manning — "Large Language Models as Simulated Economic Agents: What Can We Learn from Homo Silicus?" (2023, rev. 02/2026).** https://arxiv.org/abs/2301.07543 — Sustenta: réplicas qualitativas de experimentos clássicos de economia comportamental. Confiabilidade: média-alta. As réplicas são qualitativas, não quantitativas.
5. **Bisbee, Clinton, Dorff, Kenkel, Larson — "Synthetic Replacements for Human Survey Data? The Perils of Large Language Models", Political Analysis 32(4):401–416 (2024).** https://ideas.repec.org/a/cup/polals/v32y2024i4p401-416_2.html — Sustenta: médias corretas, variância menor, coeficientes divergentes, instabilidade em três meses. Confiabilidade: alta, com revisão por pares em periódico de referência. A página da Cambridge devolveu 429 e li o registro no RePEc.
6. **Wang, Morgenstern, Dickerson — "Large language models that replace human participants can harmfully misportray and flatten identity groups" (Nature Machine Intelligence).** https://arxiv.org/abs/2402.01908 — Sustenta: achatamento e retrato errado de identidades, 3.200 participantes, 16 identidades. Confiabilidade: alta, com revisão por pares.
7. **Yang, Zhang, Zheng et al. — "OASIS: Open Agent Social Interaction Simulations with One Million Agents" (2024, rev. 03/2025).** https://arxiv.org/abs/2411.11581 — Sustenta: escala de um milhão de agentes e réplica de difusão, polarização e efeito manada. Confiabilidade: média. É um preprint, e a "réplica" é qualitativa.
8. **Piao, Yan, Zhang et al. — "AgentSociety" (2025, rev. 04/2026).** https://arxiv.org/abs/2502.08691 — Sustenta: mais de 10 mil agentes, 5 milhões de interações e cinco temas sociais. Confiabilidade: média. É preprint e se autoavalia.
9. **Anthis, Liu, Richardson, Kozlowski, Koch, Evans, Brynjolfsson, Bernstein — "LLM Social Simulations Are a Promising Research Method" (ICML 2025).** https://arxiv.org/abs/2504.02234 — Sustenta: baixa adoção entre cientistas sociais e viabilidade para pilotos. Confiabilidade: média-alta. É um *position paper*, portanto argumento e não evidência nova.
10. **Madden — "Evaluating the Use of Large Language Models as Synthetic Social Agents in Social Science Research" (2025).** https://arxiv.org/abs/2509.26080 — Sustenta: o enquadramento como "interpolação quase-preditiva com escopo explícito" e as salvaguardas. Confiabilidade: média. É um preprint conceitual de autora única.
11. **Larooij, Törnberg — "Do Large Language Models Solve the Problems of Agent-Based Modeling? A Critical Review of Generative Social Simulations" (2025).** https://arxiv.org/abs/2504.03274 — Sustenta: a falta de validade operacional, o problema da caixa-preta e a D2 como raiz frágil. Confiabilidade: média-alta. É revisão crítica, em preprint.
12. **Törnberg, Valeeva, Uitermark, Bail — "Simulating Social Media Using Large Language Models to Evaluate Alternative News Feed Algorithms" (2023).** https://arxiv.org/abs/2310.05984 — Sustenta: o feed por ponte reduz toxicidade em rede simulada. Confiabilidade: média. É preprint, e o resultado é só em simulação.
13. **Larooij, Törnberg — "Can We Fix Social Media? Testing Prosocial Interventions using Generative Social Simulation" (2025).** https://arxiv.org/abs/2508.03385 — Sustenta: seis intervenções com melhora modesta ou piora (e3.2). Confiabilidade: média. É preprint e está sujeito às mesmas críticas de validade de [11], dos mesmos autores.
14. **Altera.AL et al. — "Project Sid: Many-agent simulations toward AI civilization" (2024).** https://arxiv.org/abs/2411.00114 — Sustenta: de 10 a mais de 1.000 agentes no Minecraft, com papéis, regras e cultura emergentes. Confiabilidade: média-baixa como ciência social. É preprint de empresa, e "religião" e "civilização" são enquadramentos fortes.
15. **Vezhnevets, Agapiou, Aharon, Ziv, Matyas, Duéñez-Guzmán, Cunningham, Osindero, Karmon, Leibo — "Generative agent-based modeling … using Concordia" (2023).** https://arxiv.org/abs/2312.03664 — Sustenta: a biblioteca aberta, o conceito de Game Master e o uso previsto em avaliação de serviços digitais. Confiabilidade: alta como descrição de ferramenta.
16. **Binz, Akata, Bethge et al. — "A foundation model to predict and capture human cognition", Nature (02/07/2025).** https://pmc.ncbi.nlm.nih.gov/articles/PMC12390832/ — Sustenta: o Centaur, o Psych-101 e o viés WEIRD admitido. Confiabilidade: alta, com revisão por pares na Nature. A página da Nature redirecionou para login, então li no PMC.
17. **Hewitt, Ashokkumar, Ghezae, Willer — "Predicting results of social science experiments using large language models" (página do projeto, Stanford).** https://ai4pb.stanford.edu/projects/predicting-results-of-social-science-experiments-using-large-language-models — Sustenta: 70 experimentos, 476 efeitos, 105.165 participantes, r = 0,85. Confiabilidade: alta, mas há divergência de números entre versões (seção 8, item 3). Os resultados de busca indicam publicação na Nature em 2026, mas a página do PubMed não carregou e não confirmei o volume.
18. **Li, Ji — "Statistical realism is not evidence that LLMs can estimate treatment effects in social science experiments" (2026, v3 07/2026).** https://arxiv.org/abs/2604.02458 — Sustenta: realismo e efeito de tratamento são alvos diferentes, com 59.508 participantes em 62 países. Confiabilidade: média-alta. É preprint recente com amostra grande e multinacional.
19. **Westwood — "The potential existential threat of large language models to online survey research", PNAS (20/11/2025).** https://pmc.ncbi.nlm.nih.gov/articles/PMC12663962/ — Sustenta: toda a D3 (99,8%, US$ 0,05, de 10 a 52 respostas para inverter previsões). Confiabilidade: alta, com revisão por pares na PNAS.
20. **Verasight — "Solving the existential threat of large language models to online survey research" (11/2025, atual. 09/2026).** https://www.verasight.io/post/solving-the-existential-threat-of-large-language-models-to-online-survey-research — Sustenta: as contramedidas de verificação (e5.1). Confiabilidade: média. É uma empresa de painel promovendo a própria solução.
21. **González-Bustamante, Verelst, Cisternas — "Emulating Public Opinion: … the Chilean Case" (2025).** https://arxiv.org/abs/2509.09871 — Sustenta: bom desempenho em confiança institucional, heterogeneidade por item e por idade, e o único caso latino-americano. Confiabilidade: média. É preprint.
22. **Suresh — "Two-Faced Social Agents: Context Collapse in Role-Conditioned Large Language Models" (2025).** https://arxiv.org/abs/2511.15573 — Sustenta: o colapso de persona em tarefas de raciocínio (seção 6). Confiabilidade: média-baixa. É preprint de autor único com 15 personas.
23. **Di Ciocco, Díaz Celauro, Pinto, Kuperman, Balenzuela — "Weaker Coherence, Weaker Reciprocity: … Moltbook and Reddit" (08/2026).** https://arxiv.org/abs/2608.14893 — Sustenta: redes só de agentes diferem das humanas. Confiabilidade: média. É preprint muito recente.
24. **Budiu (NN/g) — "Evaluating AI-Simulated Behavior: Insights from Three Studies on Digital Twins and Synthetic Users" (15/08/2025).** https://www.nngroup.com/articles/ai-simulations-studies/ — Sustenta: a síntese para UX, a variabilidade menor e o "complementar, não substituir". Confiabilidade: média-alta. É fonte secundária respeitada em UX, que resume estudos de terceiros.
25. **Qualtrics — "Qualtrics Introduces New Market Intelligence Capabilities…" (19/03/2025).** https://www.qualtrics.com/news/qualtrics-introduces-new-market-intelligence-capabilities-for-the-next-generation-of-market-insights/ — Sustenta: o lançamento do Edge Audiences, "até 70%" de redução de custo e o early access. Confiabilidade: baixa para afirmações de desempenho (é comunicado da empresa), alta para o fato do lançamento.
26. **SiliconANGLE — "Qualtrics adds AI-powered synthetic data and research tools…" (18/03/2026).** https://siliconangle.com/2026/03/18/qualtrics-adds-ai-powered-synthetic-data-research-tools-speed-customer-insights/ — Sustenta: a expansão de 2026, as afirmações de "200 milhões de respondentes" e "12x" e o fato de só atender os EUA no anúncio. Confiabilidade: média, porque a imprensa reproduz a fala da empresa.
27. **AAPOR — Standards and Ethics (código revisado, 06/2026).** https://aapor.org/standards-and-ethics/ — Sustenta: dados sintéticos não são participantes, rótulo obrigatório e declaração de amostras mistas. Confiabilidade: alta, é a fonte primária normativa.
28. **Tech Funding News — "Simile bags $200M at $2B…" (31/07/2026).** https://techfundingnews.com/simile-bags-200m-at-2b-five-months-after-100m-series-a-to-predict-what-humans-will-do-before-ai-gets-it-wrong/ — Sustenta: as rodadas, os investidores, os clientes (CVS, Wealthfront, Deloitte, Gallup) e os fundadores. Confiabilidade: média, porque é imprensa de negócios baseada em anúncio da empresa.
29. **TechCrunch via Yahoo Finance — "Sources: AI synthetic research startup Aaru raised a Series A at a $1B 'headline' valuation" (05/12/2025).** https://finance.yahoo.com/news/sources-ai-synthetic-research-startup-233859223.html — Sustenta: a rodada da Aaru, o valuation misto, ARR abaixo de US$ 10 mi e os clientes. Confiabilidade: média-alta. É jornalismo com fontes anônimas, mas com ressalvas explícitas.
30. **McKown-Dawson (Silver Bulletin) — "'AI polls' are fake polls" (11/04/2026).** https://www.natesilver.net/p/ai-polls-are-fake-polls — Sustenta: o desempenho da Aaru em 2024, o caso do Public Sentiment Institute e as críticas de pollsters. Confiabilidade: média-alta. É análise de uma casa de previsão eleitoral com interesse concorrente declarado implicitamente.
31. **36kr — "16-Year-Old CTO Leads Team to Accurately Predict US Election with 5,000 AIs…"** https://eu.36kr.com/en/p/3596704428556551 — Sustenta: **só** o exemplo de narrativa comercial não verificada (seção 8, item 4). Confiabilidade: baixa. É promocional, sem fontes e com números inconsistentes.

## 12. Anexo — o levantamento bruto

### Entrevista da Fase 1 (respostas de quem pediu)

Todos os seis pontos foram respondidos, e nenhum valor foi assumido pela skill.

1. **Recorte:** aceito como proposto. Simulação multiagente com LLMs (agentes generativos) usada como instrumento de pesquisa social e de mídia: amostras sintéticas no lugar de surveys, simulação de difusão de informação e desinformação, teste de políticas públicas e teste de produtos e interfaces com populações sintéticas.
2. **Horizonte:** 2031.
3. **Público:** público em geral conectado com tecnologia.
4. **Recorte geográfico:** global.
5. **Descartes:** nenhum.
6. **Viés:** cético moderado.

Como não houve descarte, gêmeos digitais industriais, simulação militar e a hipótese filosófica da simulação não foram excluídos por decisão de quem pediu. Eles saíram pelo critério da Fase 2 ou por não terem relação com o recorte, como registrado abaixo.

### Fase 2 — tecnologias testadas e rejeitadas como disrupção-raiz

| Tecnologia | Resultado | Motivo |
|---|---|---|
| Modelos de linguagem (LLMs) em geral | **Rejeitada, madura** | Teste 1: há dezenas de implantações em produção em escala, e é a opção padrão em vários fluxos. O que muda é custo e capacidade. É infraestrutura da seção 3, não raiz. |
| Modelagem baseada em agentes clássica (regras codificadas, tipo NetLogo e Mesa) | **Rejeitada, madura** | Teste 1: é método estabelecido há décadas em ciências sociais e epidemiologia. Aparece como o que a D2 desloca (e4). |
| Painéis online opt-in | **Rejeitada, madura** | É o padrão atual da pesquisa comercial. É o **alvo** da D1 e da D3, não uma disrupção. |
| Dados sintéticos tabulares para privacidade e treino de ML | **Rejeitada, melhoria** | Teste 3: "fica mais barato e mais privado", mas nenhum ator perde a razão de existir. Além disso, não é simulação de comportamento social e está fora do recorte. |
| Gêmeos digitais industriais (fábrica, cidade física) | **Rejeitada, madura e fora do recorte** | Teste 1: há implantação industrial ampla. O "gêmeo" desse mapa é o comportamental (D1). |
| Centaur e modelos-fundação de cognição humana | **Rejeitada como raiz, virou sinal fraco** | Teste 2: existe, é aberto e está publicado na Nature [16], mas não encontrei uso fora do laboratório. É especulação de uso, não tecnologia emergente em adoção. Foi para a seção 6. |
| Redes sociais só de agentes (Moltbook) | **Rejeitada como raiz, virou sinal fraco** | Teste 2: existe e é estudada [23], mas não é usada como instrumento de pesquisa, só como objeto. Teste 3: não está claro o que deixaria de fazer sentido. |
| "Civilizações" de agentes (Project Sid) | **Absorvida na D2** | Não é raiz separada. É instância da D2 em ambiente de jogo [14]. |
| Mercados de previsão | **Rejeitada, fora do escopo como raiz** | Não é simulação. Aparece como efeito de 3ª ordem (e6.1.1). Não li fonte sobre mercados de previsão nesta sessão, então o efeito tem confiança baixa. |
| Hipótese filosófica da simulação (Bostrom) | **Rejeitada, fora do recorte** | Não é tecnologia nem instrumento de investigação. |
| Simulação militar e de defesa (wargaming com LLM) | **Não testada a fundo** | Pode ser relevante, mas não fiz busca específica. Fica registrado como lacuna. |

### Fase 4 — efeitos cortados da roda, e por quê

1. **"Institutos de pesquisa tradicionais (Gallup, Ipsos etc.) fecham ou encolhem drasticamente até 2031."** Cortado. A evidência vai na direção contrária: o Gallup aparece como **cliente** da Simile [28], ou seja, os incumbentes estão absorvendo a tecnologia. Além disso, o efeito supunha velocidade de adoção sem precedente. Substituído por e1.1 (reposicionamento em vez de fechamento).
2. **"Governos passam a simular a população antes de aprovar cada lei."** Cortado. O elo causal pula etapas: não há uma única fonte lida mostrando governo usando simulação generativa em processo legislativo. É o "e aí tudo muda" que a skill manda cortar.
3. **"Agentes sintéticos passam a votar ou representar cidadãos em consultas públicas."** Cortado. É ficção especulativa genérica, que valeria para qualquer tecnologia de IA, e não para esta disrupção.
4. **"O Centaur ou similares substituem experimentos de laboratório em psicologia."** Cortado da roda e movido para sinal fraco. A tecnologia não passou no teste 2 (acima), então não pode gerar efeito de 1ª ordem.
5. **"Gêmeos sintéticos de pacientes substituem braços de controle em ensaios clínicos."** Cortado. Fica fora do recorte de mídia e interação e não tem evidência nas fontes lidas. A CVS usa a Simile para varejo, e não para ensaio clínico [28].
6. **Versão original de e5.2** ("distinguir pesquisa humana de sintética vira exigência de ética e divulgação", 2027, sinal forte, confiança alta). Reescrita porque **já é presente**: a AAPOR a adotou em junho de 2026 [27].
7. **Versão original de e1** (confiança alta). Rebaixada para média por ser extrapolação linear.
8. **Versão original de e2** (prazo 2028). Adiada para 2029 por supor adoção sem precedente.
9. **Versão original de e3.1** (confiança média). Rebaixada: faltava o passo intermediário, porque nada indica regulador aceitando simulação.

### Efeitos considerados e não incluídos por falta de espaço estrutural

Estes não foram cortados por falha na auditoria. Não entraram porque a roda precisa de três níveis limpos por ramo.

- "Agências de publicidade passam a testar criativos em audiências sintéticas antes de cada veiculação." Isso é quase o mesmo que e1. Ficou implícito.
- "Cursos de metodologia de pesquisa passam a ensinar validação de simulação como disciplina." Seria uma terceira ordem plausível de e4.1, mas é pouco específica para este tema.
- "Candidatos passam a treinar debates contra eleitorados simulados." É plausível, mas não achei evidência de uso.
- "Jornalismo de dados passa a checar se uma pesquisa é humana antes de publicar." Cabe em e5.2.1.

### Registro de buscas e leituras

**Leituras bem-sucedidas.** São as 31 da seção 11.

**Leituras que falharam, e o que fiz:**

- Várias chamadas de leitura feitas **em paralelo** foram negadas pelo controle de permissões do ambiente. As mesmas páginas foram lidas depois, uma de cada vez: Park 2023, Park 2024, Argyle, Wang, Horton, AgentSociety, Anthis, Madden e RePEc/Bisbee. A busca sobre a Simile também foi negada em paralelo e refeita depois.
- `cambridge.org` (Bisbee): HTTP 429 (limite de requisições). Li o registro no RePEc [5].
- `nature.com` (Centaur): redirecionou para login. Li no PMC [16].
- `pubmed.ncbi.nlm.nih.gov/42420458` (Hewitt, versão Nature): a página só mostrou aviso de cookies. **Não li.** Usei a página do projeto em Stanford [17].

**Resultados de busca vistos e não abertos**, por isso fora da seção 11 e do contador:

- "Small Foundation Models of Human Cognition and Behaviour" (arXiv 2608.05224), só mencionado como sinal na seção 6.
- "Arti-'fickle' Intelligence: Using LLMs as a Tool for Inference in the Political and Social Sciences" (arXiv 2504.03822).
- "Generating Public Health Responses using Survey-Augmented Large Language Models" (arXiv 2606.21820).
- "Polypersona: Persona-Grounded LLM for Synthetic Survey Responses" (arXiv 2512.14562).
- "AI Contextual Measurement for Recovering Individual and Group-Level Effects…" (arXiv 2609.02821).
- "Beyond Static Responses: Multi-Agent LLM Systems as a New Paradigm for Social Science Research" (arXiv 2506.01839).
- "Synthetic Founders: AI-Generated Social Simulations for Startup Validation Research" (arXiv 2509.02605).
- AAPOR, "Responsible AI Integration in Survey Research" (PDF, 05/2026).
- AAPOR Presidential Address, "That Ain't the Way I Heard It…".
- 404 Media, "A Researcher Made an AI That Completely Breaks the Online Surveys…".
- Turing Post, "Can AI Simulate 8 Billion People? Inside Simile's $2B Bet".
- Bain Capital Ventures, "The Human Layer of AI: Why We're Investing in Simile".
- RealClearMarkets, "For Investors Trying to Price Risk, AI Polling Is Long Overdue" (04/2026).
- Campaign Innovation, "What Campaigns Need To Know About AI Polling".
- NN/g, vídeo "Synthetic Users: AI 'Participants'" e "A Research Agenda for Generative AI in UX".
- Maze, IxDF, PM Toolkit, Radical Product e Medium (Liz Dugan), textos sobre usuários sintéticos em UX.
- Investing.com, Taipei Times, MLQ e Fundraise Insider, outras coberturas da rodada da Simile.
- AI CERTs, FishDog e TechBuzz, coberturas da Aaru.

**Buscas que não foram feitas e deveriam** (lacunas conhecidas):

- Uso de simulação generativa por governos e reguladores. O DSA europeu e as avaliações de risco sistêmico sustentariam ou derrubariam e3.1.
- Regulação de pesquisas eleitorais sintéticas fora dos EUA. Para o Brasil, seria o TSE; o recorte é global, mas vale para um desdobramento.
- A história da migração de telefone para painel online, com datas, para ter um caso comparável de velocidade de adoção (seção 7).
- Mercados de previsão (e6.1.1).
- Wargaming e simulação militar com LLMs.
- Estudos com populações não anglófonas além do Chile.

### Notas brutas de leitura (não editadas)

- Park 2024: "reduced accuracy disparities across racial and ideological groups compared to demographics-only". Última revisão em 28/06/2026. O título mudou em relação à versão que eu lembrava.
- Bisbee: "same prompt yields significantly different results over a 3-month period". Termômetros para 11 grupos sociopolíticos. ANES 2016–2020.
- Wang: "epistemic injustice against the value of lived experiences". Recomenda suplementar, não substituir. Técnicas de inferência reduzem, mas não eliminam, o dano.
- Westwood: persona definida em uma instrução de uns 500 palavras. Recusa estratégica de 97,7% das tarefas de "shibboleth reverso", que é a tática de evasão. Margem de lucro acima de 96,8% para quem frauda pesquisas que pagam US$ 1,50. De 55 a 97 respondentes sintéticos movem sete pesquisas nacionais para além da margem de erro.
- Hewitt (resumo da busca, não confirmado): "tended to overestimate effect sizes". Não confirmei na página de Stanford, então não uso no corpo.
- Centaur: 253.597.411 tokens de texto. Representações internas mais alinhadas com atividade cerebral sem treino neural. Tempos de resposta previstos via entropia.
- Simile: "revenue grew fivefold since launch", mais de 50 funcionários, mais de US$ 300 mi em menos de 6 meses. A série A de US$ 100 mi foi liderada pela Index Ventures. Anjos: Karpathy, Fei-Fei Li, Adam D'Angelo. A CVS usava a Simile havia cinco meses no lugar de grupos focais, segundo o resumo de busca da matéria de fevereiro, que não abri diretamente.
- Aaru: fundada em março de 2024. Fundadores Cameron Fink, Ned Koh e John Kessler. Investidores anteriores: A*, Abstract, General Catalyst, Accenture Ventures e Z Fellows. A matéria do 36kr diz que o CTO tem 16 anos, o que não verifiquei.
- Silver Bulletin: a Aaru dava 50,5% de chance para Harris em 02/11/2024, contra 48,2% do Silver Bulletin. O pollster democrata John Hagner diz: "you're asking the machine to tell you what you already believe". Os LLMs dão menos respostas "não sei" e superestimam a favorabilidade de políticos.
- Qualtrics 2025: Instant Insights para restaurantes, hotelaria, seguros nos EUA e bancos nos EUA e Reino Unido, com parceria NPS Prism (Bain). Clientes citados no resumo de busca: Loop Earplugs, Zip, Booking.com e Google Labs. Não confirmei na página lida, então não uso no corpo.
- Qualtrics 2026: "only about 2% of the feedback companies gather triggers a tangible response" (Brad Anderson). Expansão para Reino Unido, Irlanda, Canadá, Austrália e Nova Zelândia no primeiro semestre de 2026.
- Larooij & Törnberg (revisão): "limited awareness of historical debates". A validação depende de "believability" subjetiva.
- Li & Ji: o viés é pior em desfechos comportamentais, porque os modelos extrapolam efeitos de atitude para comportamento. A réplica em 12 e 27 países teve 20.785 participantes.
- Suresh: GPT-5, Claude Sonnet 4.5 e Gemini 2.5 Flash, com 15 personas socioeconômicas, em itens de SAT e tarefas de preferência.
- Moltbook: trocas "broadcast-like", não recíprocas. Comunidades mal alinhadas com os próprios nomes.
- NN/g: os estudos são Kim & Lee (2024, GSS), a equipe Stanford–Google (entrevistas de 2 h) e Arora et al. (2025, ração para pets). O viés político e racial caiu de 36% a 62% em relação a modelos demográficos. Os usuários sintéticos acertam a direção e erram a magnitude.
- Chile: 128 combinações de prompt, modelo e pergunta, com cerca de 190 mil perfis sintéticos. GPT-4o, GPT-4o-mini e Llama 4 Maverick ficaram equivalentes.
- AgentSociety: os temas foram polarização, mensagens inflamatórias, renda básica universal, choques externos (furacão) e sustentabilidade urbana.

### Rodada descartada de desenho das raízes

A primeira versão do mapa tinha **quatro** raízes. "Gêmeos comportamentais individuais" era separada de "painéis sintéticos". Fundi as duas na D1 porque passam nos testes pelo mesmo motivo (substituir a pergunta à pessoa) e porque as mesmas empresas oferecem as duas coisas [26][28]. A separação duplicava efeitos de 1ª ordem. A distinção sobrevive dentro da D1: e1 é o painel, e2 é o gêmeo.

Também considerei "simulação como mídia e entretenimento" (Smallville como espetáculo, Project Sid e Moltbook) como raiz. Rejeitei porque o recorte escolhido é *instrumento de investigação*. O tema sobrevive como efeito de 3ª ordem (e4.1.1) e como sinal fraco.
