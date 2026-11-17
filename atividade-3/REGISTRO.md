# Registro do teste

*CIN0055 · Tendências em Mídia e Interação · 2026.2 · Movimento 3 · vafs*

Teste do experimento [Caça ao respondente sintético](src/README.md), feito com a turma em 4 de novembro de 2026,
pelo link publicado no Render.

**Configuração da sala.** 5 humanos, 4 agentes infiltrados (2 com busca na web e 2 sem), 5 perguntas no
questionário: as duas fixas (a genérica e a checagem de atenção) e três armadilhas escritas pela turma.

## O que a turma fez que eu não esperava

- **Todo mundo acertou tudo.** Cada cartão foi classificado corretamente, humano ou máquina, inclusive os dos
  agentes que podiam pesquisar na web. Ninguém foi acusado por engano.
- **A turma respondeu ao questionário cheia de erros de digitação de propósito.** Palavras trocadas, letras
  faltando, abreviações e erros bem específicos, do tipo que um modelo de fronteira não comete. Na caçada, a
  pista passou a ser a forma da resposta, não o conteúdo: texto limpo e bem pontuado era máquina, texto torto
  era gente.
- **As respostas dos agentes eram parecidas entre si.** Mesmo com personas diferentes, os quatro escreviam
  no mesmo registro: frases completas, ortografia correta, tom educado. Faltava a variação que existe entre
  cinco pessoas escrevendo no celular.
- **A discussão foi parar nos filtros dos modelos.** A turma levantou que modelos de fronteira passam por
  muito ajuste de segurança e de estilo, e que isso os deixa “certinhos” demais. A sugestão foi testar modelos
  com menos guardrails, que falem mais parecido com uma pessoa.
- **A enquete do segundo ato não engajou.** Depois do placar, a votação e a injeção de respostas sintéticas
  pareceram outro experimento, desligado do que tinha acabado de acontecer na caçada.

## O que mudei por causa disso

- **Tirei a enquete.** *(Por causa da última observação.)* O segundo ato desviava a atenção do que rendeu
  mais na aula, que foi a caçada. O experimento termina no placar.
- **Um placar que explica e que dá para conferir.** *(Por causa do acerto total.)* Com todo mundo acertando,
  o que interessava era saber como cada um acertou, e o placar antigo só mostrava taxas. Agora ele abre com
  frases que dizem o que os números significam (acerto comparado ao chute, humanos acusados, efeito da busca,
  a pergunta que mais entregou agentes e a que mais confundiu, e um aviso quando há poucos vereditos). Mostra
  também onde caiu cada veredito: agente pego, agente que passou, humano acusado, humano reconhecido. Por
  último, uma grade com o veredito de cada jogador em cada cartão e a pergunta marcada como pista, com acesso
  às respostas completas. No celular, cada pessoa vê o que disse em cada cartão, o que ele era de verdade e
  a pista que usou.
- **Agentes com modelos de poucos filtros.** *(Por causa das respostas homogêneas e da discussão sobre os
  guardrails.)* Além do Claude Haiku, a sala pode colocar agentes rodando modelos *abliterated*, versões
  abertas em que o comportamento de recusa foi removido dos pesos. A pergunta é se, sem a camada de ajuste,
  o agente se aproxima do jeito de escrever de uma pessoa ou continua reconhecível. Uma ressalva: a técnica
  tira a recusa, não necessariamente o polimento do texto, então vale comparar também com modelos base, sem
  ajuste de instrução.
- **Perguntas mais capciosas.** *(Por causa do acerto total, que veio da forma e não do conteúdo.)* As
  orientações da fase de armadilhas passam a puxar perguntas que não se resolvem pela ortografia: contexto
  local, experiência vivida, coisas que aconteceram na própria aula. A ideia é que a caçada dependa do que a
  resposta diz.

## O que decidi não mudar, e por quê

- **Não mandei os agentes errarem de propósito.** Seria o jeito mais rápido de esconder os agentes, mas
  daria uma caricatura de erro humano escrita por mim, não um teste do modelo. O que interessa é saber se
  algum modelo produz essa variação sozinho.
- **Mantive o Claude Haiku na sala.** Ele vira a referência: sem ele não dá para dizer se um modelo de poucos
  filtros engana mais ou menos.
- **Mantive as duas perguntas fixas.** A genérica e a checagem de atenção existem para comparação com as
  armadilhas da turma. Elas continuam fazendo esse papel.
- **Não mexi na proporção de agentes com busca.** Os dois com busca foram pegos como os outros. A busca
  ajuda a sustentar o conteúdo da persona, e nesta rodada o que denunciou os agentes foi a forma. Mudar a
  proporção agora não explicaria nada.
- **Não tratei o acerto total como resultado definitivo.** Foram 9 respondentes numa turma que sabia que
  havia máquinas no meio e se esforçou para parecer humana. Numa pesquisa real ninguém escreve errado de
  propósito para provar que é gente.

---

A pergunta mudou: deixou de ser “o que distingue gente de máquina quando a resposta é coerente” e virou “o
que sobra para distinguir quando a máquina também puder escrever do jeito torto e variado que a gente
escreve”.
