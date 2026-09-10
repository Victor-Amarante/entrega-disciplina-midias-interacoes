# DUVIDAS.md — onde a máquina errou

## 1. Autoria trocada — título de paper quase citado de memória, e errado

Ao decidir quais fontes usar para sustentar a disrupção D2 (amostragem sintética), cheguei a
considerar citar, de memória, um paper de Aher et al. com o título "Using Large Language Models
to Simulate Multiple Personas for Human-AI Collaboration".

**Como percebi:** antes de escrever a citação no documento, busquei para confirmar o título
exato — hábito que só ficou possível depois que a busca foi ativada nesta sessão (antes disso,
a mesma citação simplesmente não teria entrado, por precaução, mas também não teria sido
corrigida). O título real é **"Using Large Language Models to Simulate Multiple Humans and
Replicate Human Subject Studies"** ([Aher, Arriaga e Kalai,
arXiv:2208.10264, 2023](https://arxiv.org/abs/2208.10264)) — sobre replicar estudo clássico de
sujeito humano (Jogo do Ultimato, Experimento de Milgram), não sobre "colaboração humano-IA"
com múltiplas personas. A diferença entre os dois títulos é pequena o bastante para não soar
suspeita a quem só lê por cima — é exatamente o tipo de erro que passa despercebido se ninguém
para para abrir a fonte antes de citar. Por não ter dado tempo de confirmar todo o
enquadramento do paper dentro da janela desta rodada de teste, ele acabou nem entrando no corpo
do documento final — só neste registro do erro (detalhe completo na seção 8 do TESTE.md).

## 2. Número específico sem fonte checada (a versão sem busca do mesmo problema)

Antes da busca estar disponível, o primeiro rascunho da seção 3 do documento de teste ia
incluir um número específico de agentes e uma duração de simulação para o experimento de
pesquisa associado à arquitetura de "memória e reflexão" que fundamenta a disrupção D1 — um
número que soava preciso o bastante para passar por citação de fato lida.

**Como percebi:** parei antes de escrever e me perguntei, especificamente, "eu abri essa fonte
agora, nesta sessão, ou estou repetindo algo que lembro de ter lido em algum momento do
treinamento?". A resposta honesta era a segunda, e o número foi cortado por precaução. Depois,
com busca ativada, voltei à mesma fonte: o número de agentes (25) estava certo — não era
alucinação, era memória não verificada que por acaso batia com o real. Já a duração exata em
dias simulados continuou sem confirmação mesmo depois de abrir a fonte, e por isso segue fora
do documento. A lição não é "a memória sempre erra" — é que memória não verificada e fato
verificado só parecem iguais até alguém checar; sem checar, não dá pra saber qual dos dois você
tem.

## 3. Efeito construído por analogia entre setores, não por sinal do domínio

O efeito e2.1.1 da roda ("selo comercial de dado coletado de respondente humano real vira
diferencial de institutos de pesquisa") saiu fácil demais de gerar, porque é basicamente um
padrão já visto em outros lugares — selo orgânico em alimento, rótulo "human-made" em conteúdo
criativo — recolocado no domínio de pesquisa de mercado.

**Como percebi:** ao rodar a auditoria da Fase 4 da skill (o passo que tenta derrubar cada
efeito), a pergunta "o elo causal pula uma etapa?" expôs que eu não tinha nenhum sinal
específico do mercado de pesquisa apontando nessa direção — só a analogia. Analogia entre
setores é uma forma legítima de gerar hipótese, mas não é evidência do domínio em questão; por
isso o efeito ficou no mapa (é uma derivação válida), mas com `sinal: fraco` e
`confianca: baixa`, e citado explicitamente na seção 8 do documento para não ser lido como mais
sólido do que é. Sem o passo de auditoria obrigatório, esse efeito teria saído com confiança
mais alta do que merece — foi o próprio desenho da skill (a exigência de duvidar do resultado)
que forçou a segunda checagem, não uma suspeita que eu já tinha antes de gerar o efeito.

## O que não apareceu

Depois de ativar busca e verificar com fonte real as atribuições que o ESTUDO.md usa
(Glenn/Futures Wheel 1971, Fenn/Gartner Hype Cycle 1995, Sharpe/Three Horizons), nenhuma delas
estava errada — todas bateram com o que eu já tinha de memória. Isso é diferente de "não
precisava verificar": o item 1 acima mostra exatamente o caso em que a memória parecia
igualmente segura e não batia. A verificação não confirmou que a memória era confiável em
geral — confirmou essas três atribuições específicas, e revelou que uma quarta (o paper de
Aher et al.) não era confiável. Sem checar as quatro, não daria pra saber qual delas era qual.
