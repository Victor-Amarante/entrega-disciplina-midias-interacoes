---
name: futurizacao-vafs
description: Use quando for preciso construir um mapa de futuro de um tema de mídia/tecnologia/interação — a skill entrevista o pedido antes de rodar, separa disrupção real de tecnologia madura com um critério explícito, gera uma roda de futuros de três níveis e depois tenta derrubar o próprio resultado, produzindo a saída já no formato padrão `tendencia-<slug>.md` da disciplina CIN0055.
---

# futurizacao-vafs

Testado em: **Claude Code** (modelo Sonnet 5), 09/09/2026, aluno vafs, CIN0055 — Tendências em
Mídia e Interação. Instruções abaixo devem funcionar coladas como prompt de sistema em qualquer
chat que aceite instrução longa e produza Markdown — não dependem de nenhuma ferramenta externa.

Esta skill implementa o **Futures Wheel** (roda dos futuros) com dois freios explícitos —
um contra tecnologia madura disfarçada de disrupção, outro contra efeito inventado por inércia
generativa — e formata a saída no esqueleto de `FORMATO-documento-tendencia.md`.

---

## 0. Quando isto dispara

Dispara quando alguém pede um mapa de futuro, uma "roda dos futuros", uma análise de
disrupção/tendência, ou pedir para "futurizar" um tema — mesmo que o pedido venha resumido em
uma frase ("faça a roda dos futuros de X"). **Nunca produza a saída a partir de uma frase
assim.** O disparo inicia a Fase 1, não a Fase 3.

Se quem pediu já responder tudo da Fase 1 na primeira mensagem (dá para acontecer), não
repita a pergunta — confirme o que foi entendido em uma frase e siga. O objetivo da entrevista
é garantir que a informação existe, não obrigar a pessoa a preencher formulário.

---

## 1. Entrevista — não pule, não assuma

Antes de gerar qualquer efeito, colete resposta (ou "deixe em aberto, decida você" **dito
explicitamente**) para cada um destes pontos. Uma recusa em responder é uma resposta válida,
mas tem que ser pedida:

1. **Tema e recorte** — qual é o ângulo específico dentro do tema amplo? ("IA" é tema amplo demais;
   "modelos de linguagem rodando em dispositivos sem rede" é recorte.)
2. **Horizonte de tempo** — que ano é o ano-alvo do mapa? Sem data, não há como calibrar prazo
   nem confiança nos efeitos de 3ª ordem.
3. **Para quem** — esta análise serve a quem, para decidir o quê? Pode ser `null`, mas pergunte;
   não assuma que é "para ninguém em especial" sem a pessoa dizer isso.
4. **Recorte geográfico** — global, Brasil, outro. Efeitos de adoção variam de forma severa por
   região; sem isso, a roda mistura mercados incompatíveis sem avisar.
5. **O que já está descartado** — que tecnologia, ator, ou cenário quem pediu já decidiu excluir
   do mapa? (Evita gerar 40% do conteúdo para depois descartar.)
6. **Viés desejado** — a pessoa quer um mapa cético, otimista, ou o mais neutro possível? Isso
   não muda os fatos, muda **qual leitura de fatos ambíguos** a skill prioriza quando o sinal é
   fraco. Declare o viés escolhido no documento final — não esconda.

**Regra de corte:** se quem pediu insistir em pular a entrevista ("só roda"), a skill pode
prosseguir, mas precisa (a) declarar por escrito, no topo da seção 12 do documento, quais dos
seis pontos ficaram sem resposta e quais valores ela assumiu no lugar, e (b) rebaixar
`confianca` do documento inteiro para `baixa` no frontmatter. Pular a entrevista tem custo
visível — nunca silencioso.

---

## 2. Critério para separar maduro / emergente / disruptivo

Aplique este teste, **por escrito**, a cada tecnologia candidata a virar disrupção-raiz. O
resultado (aceita ou rejeita, e por quê) entra na seção 4 ou no anexo (seção 12) — nunca
some sem registro.

**Teste 1 — está madura? (critério de exclusão)**
> Consigo citar hoje três implantações em produção, em escala, sem precisar apostar em nada
> sobre o futuro delas? Elas já são a opção padrão em algum fluxo de trabalho real, e o que
> resta é ficar mais barato/rápido/difundido, não mudar de natureza?

Se a resposta é sim às duas perguntas → **madura**. Não entra como disrupção-raiz. Pode entrar
na seção 3 ("onde isso está hoje") como parte do estado atual, nunca na seção 4.

**Teste 2 — é emergente? (condição necessária, não suficiente)**
> Existe fora do laboratório/piloto, mas ainda não é a escolha padrão em nenhum fluxo em
> escala? A curva de capacidade ainda está subindo, e a adoção ainda é early adopter, não
> maioria?

Se não passa neste teste (nem madura nem em uso real crescente) → é especulação, não
tecnologia emergente; tratar como sinal fraco/wildcard (seção 6), nunca como disrupção-raiz.

**Teste 3 — é disruptiva? (o que decide se emergente vira disrupção-raiz)**
> Se isto escalar, o que **deixa de fazer sentido**? Que ator, categoria ou regra do jogo
> perde a razão de existir — não "fica pior", mas deixa de ser necessário?

Se a única resposta possível é "fica mais rápido/barato/acessível" → é **melhoria**, não
disrupção, mesmo que a tecnologia em si seja emergente. Só é disrupção-raiz quando existe um
ator ou prática nomeável cuja razão de existir é ameaçada.

**Registro obrigatório:** toda tecnologia mencionada durante a sessão e **rejeitada** por este
teste (madura demais, ou emergente mas não disruptiva) entra explicitamente no anexo (seção 12)
com o motivo da rejeição. É o que prova que o critério foi aplicado, não só declarado.

---

## 3. Gerar a roda (três níveis, Futures Wheel)

Para cada disrupção-raiz aprovada no passo 2:

- **1ª ordem**: efeito direto e imediato da disrupção — o que muda assim que ela acontece,
  sem precisar de nenhuma outra mudança no meio do caminho. Narrável em uma frase causal direta
  ("X faz Y deixar de precisar de Z").
- **2ª ordem**: efeito que só existe **porque** um efeito de 1ª ordem já aconteceu — mexe com
  estrutura (papéis de trabalho, modelos de negócio, comportamento coletivo), não com o
  fenômeno técnico em si.
- **3ª ordem**: efeito que reorganiza uma instituição, uma categoria cultural ou um sistema
  inteiro — só é sustentável se o efeito de 2ª ordem que o originou também se sustentar.
  Confiança **baixa é a resposta esperada** aqui; se todos os efeitos de 3ª ordem vierem com
  confiança alta, desconfie do próprio trabalho.

**Onde parar de derivar:** pare quando (a) o efeito deixa de ter um mecanismo causal narrável em
uma frase (você só consegue dizer "e aí tudo muda", sem dizer o passo), ou (b) o efeito ultrapassa
o horizonte de tempo declarado na entrevista, ou (c) o efeito de 3ª ordem já é indistinguível de
ficção especulativa geral, do tipo que se aplicaria a qualquer disrupção, não a esta.

Cada efeito recebe, já nesta fase: `sinal` (forte/medio/fraco — força da evidência atual de que
o movimento já começou), `prazo` (ano estimado), `confianca` (alta/media/baixa).

---

## 4. Duvidar do próprio resultado (passo obrigatório, não opcional)

Depois de gerar a roda inteira, rode esta auditoria em **cada efeito**, dos três níveis:

1. **É extrapolação linear?** — o efeito é só "a curva de hoje, só que mais"? Se sim, ele não é
   um efeito de futurização, é uma projeção de tendência já em curso — rebaixe `confianca` e
   marque no comentário em prosa da seção 5.
2. **Assume velocidade de adoção sem precedente?** — existe um caso comparável histórico em que
   uma mudança estrutural parecida aconteceu na velocidade que este efeito supõe? Se não existe
   precedente e o efeito depende disso, ele vai para a seção 7 como item específico
   ("este efeito assume adoção mais rápida que qualquer caso comparável conhecido, que é X").
3. **O elo causal pula uma etapa?** — dá para narrar o passo intermediário entre a causa e o
   efeito sem inventar um verbo mágico ("faz com que", sem detalhe)? Se não dá, o efeito é
   fraco demais para entrar como está — reescreva com o passo que falta, ou corte.

Efeitos que sobrevivem à auditoria mantêm o nível de confiança. Efeitos que não sobrevivem:
ou são reescritos com o mecanismo faltante, ou são rebaixados para `confianca: baixa`, ou saem
da roda e vão para a seção 12 como "efeito cortado, e por quê". **Uma roda em que 100% dos
efeitos sobrevivem sem alteração não passou por este passo de verdade — refaça.**

A seção 7 do documento final ("Contra o próprio mapa") é o produto direto desta auditoria, não
um texto genérico escrito depois. Preencha com os itens específicos encontrados aqui: qual
efeito é extrapolação linear, qual assume adoção sem precedente, qual disrupção-raiz pode
simplesmente não se concretizar (e o que isso derruba no mapa), e qual viés de quem pediu (ou
de quem constrói a skill) influenciou a escolha do tema.

---

## 5. Saída — formato obrigatório

A saída final é um único arquivo `tendencia-<slug>.md`, exatamente neste esqueleto (títulos de
seção literais, com numeração; frontmatter YAML completo; bloco `roda:` também em YAML,
três níveis de profundidade, `id` hierárquico único, todo efeito com `sinal`, `prazo` e
`confianca`). Preencha, nunca deixe placeholder:

```markdown
---
tema: <string>
slug: <slug-do-tema>
autor_login: vafs
zona_de_interesse: <string>
data: <YYYY-MM-DD>
horizonte: <ano>
publico: <string ou null>
recorte_geografico: global | brasil | <outro>
disrupcoes_raiz: <int>
efeitos_ordem_1: <int>
efeitos_ordem_2: <int>
efeitos_ordem_3: <int>
tecnologias_citadas: [<nomes>]
fontes: <int>
confianca: alta | media | baixa
experimento: <string>
skill_usada: futurizacao-vafs
publico_ok: false
---

## 1. Resumo
## 2. O tema
## 3. Onde isso está hoje
## 4. As disrupções-raiz
## 5. A roda dos futuros

```yaml
roda:
  - disrupcao: <string>
    efeitos:
      - id: e1
        ordem: 1
        efeito: <frase afirmativa>
        sinal: forte | medio | fraco
        prazo: <ano>
        confianca: alta | media | baixa
        efeitos:
          - id: e1.1
            ordem: 2
            efeito: <frase afirmativa>
            sinal: forte | medio | fraco
            prazo: <ano>
            confianca: alta | media | baixa
            efeitos:
              - id: e1.1.1
                ordem: 3
                efeito: <frase afirmativa>
                sinal: forte | medio | fraco
                prazo: <ano>
                confianca: alta | media | baixa
```

## 6. Sinais fracos e wildcards
## 7. Contra o próprio mapa
## 8. O que a máquina errou
## 9. Três cenários para <ano do horizonte>
## 10. O experimento
## 11. Fontes
## 12. Anexo — o levantamento bruto
```

Regras de preenchimento que valem a pena repetir porque são fáceis de pular sob pressa:

- `fontes` no frontmatter é a contagem do que foi **de fato lido**, não do que foi citado de
  memória. Se uma fonte não foi aberta, ela não entra na seção 11 nem no contador.
- **Use busca e leitura de página de verdade sempre que a ferramenta existir no agente onde a
  skill está rodando.** A entrevista e a auditoria não substituem checar fato — elas organizam
  o raciocínio, mas número, autoria e ano citados de memória são exatamente o tipo de erro
  plausível que este método existe para pegar (ver seção 8 do documento de saída). Só declare
  `fontes: 0` e rebaixe `confianca` por conta de sourcing quando a ferramenta de busca
  genuinamente não estiver disponível no ambiente — e diga isso explicitamente na seção 12,
  nunca em silêncio. Quando a busca estiver disponível e um número/autoria recuperado de
  memória divergir do que a fonte real diz, corrija e registre a divergência na seção 8 — é
  a prova de que a verificação rodou de verdade, não só foi declarada.
- A seção 12 recebe tudo que não coube nas outras: tecnologias rejeitadas pelo teste da Fase 2
  com o motivo, efeitos cortados pela auditoria da Fase 4, buscas que não deram em nada. Sem
  limite de tamanho, sem edição.
- Nunca marque `publico_ok: true` por conta própria — é decisão de quem entrega, sempre `false`
  por padrão até a pessoa confirmar.
- Se algum dos seis pontos da entrevista (Fase 1) ficou sem resposta, isso tem que aparecer por
  escrito no início da seção 12, não só na sua memória de conversa.

---

## 6. Checklist final antes de entregar

- [ ] A entrevista da Fase 1 aconteceu e está refletida no frontmatter (`horizonte`, `publico`,
      `recorte_geografico`).
- [ ] Toda tecnologia madura mencionada foi explicitamente testada e rejeitada com o critério
      da Fase 2, com o registro no anexo.
- [ ] A roda tem exatamente três níveis, `id`s únicos e hierárquicos, e todo efeito tem `sinal`,
      `prazo`, `confianca`.
- [ ] A auditoria da Fase 4 rodou de verdade — existe pelo menos um efeito rebaixado, reescrito
      ou cortado, e a seção 7 tem itens específicos, não genéricos.
- [ ] As 12 seções existem com os títulos literais, na ordem, e o bloco `roda:` é YAML válido.
