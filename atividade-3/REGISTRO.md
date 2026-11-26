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
- **Todos os agentes num modelo sem filtros.** *(Por causa das respostas homogêneas e da discussão sobre os
  guardrails.)* O Claude Haiku saiu da sala. Todos os agentes agora rodam no `abliterated-model-large-v2`, do
  abliteration.ai, um GLM-5.3 aberto em que o comportamento de recusa foi removido dos pesos. A pergunta é se,
  sem a camada de ajuste, o agente se aproxima do jeito de escrever de uma pessoa ou continua reconhecível. A
  referência é a primeira rodada, toda em Claude, em que nenhum agente passou. Num teste curto, com duas
  pessoas, os agentes sem filtros passaram por gente em metade dos vereditos. É pouco para concluir, e as
  armadilhas mudam de uma rodada para outra, mas aponta na direção da hipótese.
- **Sem busca na web.** *(Por causa do que denunciou os agentes.)* O modelo sem filtros não pesquisa, e a
  busca não fez falta na primeira rodada: os dois agentes com busca foram pegos como os outros, porque o que
  os entregou foi a forma, não o conteúdo.
- **Agentes que escrevem como gente comum.** *(Por causa dos erros de digitação da turma.)* Eu tinha decidido
  não pedir erro de propósito, para testar só o modelo. Voltei atrás: a turma escreveu errado de propósito
  para parecer gente, e quem opera uma fazenda de bots faria o mesmo com os seus. Cada agente agora tem um
  jeito próprio de escrever, tirado de como a turma escreveu: resposta de duas palavras, tudo em minúsculas,
  sem acento ("reuniao", "voce"), abreviando, com preguiça ("sei la") ou deixando passar um erro de
  digitação. O prompt também pede o contrário de ser interessante. No teste com duas pessoas, o que ainda
  entregava os agentes era o esforço: para "qual é a cor do Sol?", os humanos responderam "Amarelo" e os
  quatro agentes, coisas como "amarela, mais pra laranja se vc olha direto, mas n devia olhar rs". Agora,
  pergunta boba leva de uma a três palavras, sem "mas", sem piada e sem referência esperta. Quando o modelo
  solta um caractere fora do alfabeto ou corta uma resposta, como aconteceu nesse teste ("Com驿... não sei"), o
  agente responde de novo.
- **Agentes que não se repetem.** *(Por causa das respostas homogêneas.)* Mesmo com personas e estilos
  diferentes, os agentes caíam na resposta mais provável do modelo: num teste com oito agentes, seis disseram
  que a prática que todo mundo finge seguir é "code review de verdade". Agora eles respondem em fila, dois de
  cada vez, e cada um vê o que os anteriores já disseram, com a instrução de não repetir a ideia nem o jeito de
  começar a frase. O contrário de uma coxinha virou "salada", "suco verde", "tapioca" e "acarajé".
- **Perguntas que os dois lados conseguem responder.** *(Por causa do acerto total, que veio da forma e não
  do conteúdo.)* Se só um lado sabe a resposta, a caçada fica fácil demais e não diz nada sobre o jeito de
  escrever. "Quantas pessoas tem na sala agora?" ou "o que foi dito no começo da apresentação?" entregam o
  agente porque ele não tem como saber e inventa qualquer coisa. O evento impossível ("o que achou do Python
  4?") é uma armadilha montada para a máquina inventar. O *só máquina sabe* (uma conta grande, o alfabeto de
  trás pra frente), que cheguei a criar depois do teste junto com o *aqui na sala*, inverte o problema e
  obriga o agente a fingir que não sabe. O contexto local ("onde a galera de tecnologia almoça perto do Porto
  Digital?") depende de pesquisar na web, e os agentes não pesquisam mais. Os cinco saíram das opções da
  turma. Ficaram experiência vivida e *sem filtro* (opinião forte ou reclamação, que uma pessoa dá sem
  cerimônia e um modelo educado tende a amaciar), e entrou a *pegadinha*: uma pergunta boba que todo mundo sabe
  responder. Aí a pista está na atitude, e não em quem tem a informação. Se alguém da turma ainda mandar uma
  pergunta sobre a sala, troco no painel por outra.
- **Um banco de perguntas no lugar das fixas.** *(Por causa das perguntas que não separavam ninguém.)* A da
  macaxeira mostrou que seguir uma instrução escondida é mais fácil para a máquina do que para gente, e todo
  mundo responde igual. A genérica, "como foi seu último dia de trabalho?", convidava a uma resposta
  burocrática. As duas deram lugar a um banco de nove perguntas do instituto, três de cada tipo, como "qual é o
  contrário de uma coxinha?", "qual frase de LinkedIn te dá vergonha alheia?" e "conte a última vez que você
  fingiu estar ocupado". Cada sala sorteia uma de cada tipo e completa o questionário com as armadilhas da
  turma; se faltarem armadilhas, o banco completa.
- **Um placar que explica e que dá para conferir.** *(Por causa do acerto total.)* Com todo mundo acertando,
  o que interessava era saber como cada um acertou, e o placar antigo só mostrava taxas. Agora ele abre com
  frases que dizem o que os números significam (acerto comparado ao acaso, humanos acusados, a pergunta que
  mais entregou agentes e a que mais confundiu, e um aviso quando há poucos vereditos). Mostra também onde
  caiu cada veredito (agente pego, agente que passou, humano acusado, humano reconhecido) e uma grade com o
  veredito de cada jogador em cada cartão, com acesso às respostas completas. No celular, cada pessoa vê o que
  disse em cada cartão, o que ele era de verdade e a pista que usou. No fim, um cartão explica a régua do
  acaso: quanto daria dizendo "máquina" para todos os cartões, sem ler nada. A régua muda com a sala. Com
  cartões meio a meio, fica em 50%, mas no teste com duas pessoas cada uma recebeu quatro agentes e um humano,
  e a régua foi a 80%. Os 60% de acerto daquele teste, que pareciam bons perto de uma moeda, estavam abaixo
  do acaso. Quando só uma pessoa joga, todos os cartões são agentes, a régua vai a 100% e o placar avisa que
  não há o que medir, em vez de dizer que os agentes se disfarçaram.

## O que decidi não mudar, e por quê

- **Não mandei os agentes zoarem.** Na pegadinha, o prompt pede a resposta óbvia, e não uma piada. No teste
  com duas pessoas, os humanos responderam seco ("Tio", "Amarelo"). Zoeira forçada viraria a caricatura de
  gente que já entregava os agentes.
- **Mantive oito agentes por sala.** Com seis ou sete pessoas, cada uma recebe quatro agentes e quatro
  humanos, a régua do acaso fica em 50% e o placar fica fácil de ler.
- **Não tratei o acerto total como resultado definitivo.** Foram 9 respondentes numa turma que sabia que
  havia máquinas no meio e se esforçou para parecer humana. Numa pesquisa real ninguém escreve errado de
  propósito para provar que é gente.

---

A pergunta mudou: deixou de ser “o que distingue gente de máquina quando a resposta é coerente” e virou “o
que sobra para distinguir quando a máquina também puder escrever do jeito torto e variado que a gente
escreve”.
