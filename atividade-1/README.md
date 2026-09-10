# Atividade 01 — Hiper Deep Research · Entrega 1 (Ferramentas de Inspiração)

CIN0055 · Tendências em Mídia e Interação · CIn/UFPE · 2026.2
Aluno: Victor Amarante · Modo declarado: **MODO 3** (IA executa, aluno orquestra)

**Recorte:** simulação com agentes de IA entendida como **ambiente que se abre e
se usa** — sandbox hospedado, plataforma multiagente, observabilidade e replay de
agentes, mundo/jogo com NPC de IA, simulação social, usuários sintéticos.
Bibliotecas e frameworks (`pip install`) ficam fora: são Entrega 2.

---

## Como rodar

```bash
uv sync

# 0. sonda cada fonte candidata uma vez e relata o que responde
uv run python atividade-1/sondagem.py

# 1. varredura ampla -> dados/candidatos.jsonl + dados/log_bruto.jsonl
uv run python atividade-1/varrer.py --paginas 5
uv run python atividade-1/varrer.py --fontes arxiv --paginas 2   # arXiv é lento de propósito

# 2. peneira mecânica com os critérios do aluno -> dados/preselecao.jsonl
uv run python atividade-1/peneirar.py --desempate popularidade

# 3. abre e verifica cada pré-selecionado -> dados/enriquecidos.jsonl
uv run python atividade-1/enriquecer.py --trabalhadores 12

# 4. repontua sobre o texto real da página -> dados/para_descrever.jsonl
uv run python atividade-1/julgar.py --quantos 500

# 5. gera o anexo técnico de fontes e viés a partir do log
uv run python atividade-1/relatar.py
```

Tudo é **retomável**. Se cair no meio, rode de novo: `dados/estado.json` guarda
quais `(fonte, consulta, página)` terminaram e `dados/cache/` guarda as
respostas HTTP. A segunda execução não repete requisição nem incomoda servidor.

Para recomeçar do zero: `--limpar-estado` e apague `dados/candidatos.jsonl`.
**Não apague `dados/log_bruto.jsonl`** — ele é o item 2 da entrega e registra
inclusive os erros e os bugs corrigidos no caminho.

**Nunca rode duas instâncias de `varrer.py` ao mesmo tempo.** As duas abrem o
mesmo arquivo de log para escrita e o resultado, medido nesta atividade, foi o
log voltar a conter apenas as execuções mais antigas. Se precisar refazer, rode
um processo por vez — como tudo fica em cache, a repetição custa segundos.

O log tem 93 MB e o sistema de entrega aceita no máximo 45 MB por arquivo, então
`entrega/log/` traz o mesmo conteúdo dividido em três partes, **sem nenhuma linha
alterada, removida ou reordenada**. Concatenar as três na ordem reconstrói o
arquivo original byte a byte.

---

## O que cada arquivo faz

| arquivo | papel |
|---|---|
| `sondagem.py` | bate uma vez em cada fonte candidata e diz o que responde. Roda antes de escrever adaptador, para não construir em cima de suposição. |
| `coletor/normalizacao.py` | forma canônica da URL e **regra de deduplicação**. É o arquivo que decide se 500 viram 700. |
| `coletor/rede.py` | cache em disco, limite de taxa por host, retentativa com backoff, robots.txt, log bruto. Tudo que sai pela rede passa aqui. |
| `coletor/deposito.py` | grava candidatos em JSONL deduplicando, e guarda o estado de retomada. |
| `coletor/consultas.py` | **o vocabulário de busca**. É a especificação do recorte: o que não está aqui não aparece na varredura. |
| `coletor/fontes/*.py` | um adaptador por fonte, cada um com a constante `VIES` declarando o que aquela fonte não mostra. |
| `varrer.py` | executor da varredura. |
| `peneirar.py` | aplica os critérios eliminatórios mecânicos e monta o pool por cota de fonte. |
| `enriquecer.py` | abre cada URL, **verifica que existe**, extrai o texto real e resolve ficha de diretório para o site verdadeiro. |
| `julgar.py` | repontua sobre o texto real e monta a fila das 500. |
| `relatar.py` | gera o anexo técnico de fontes/viés/números a partir do log. Nenhum número é escrito à mão. |

---

## Regra de deduplicação (precisa ser defendida na entrega)

Normalização da URL: força `https`, remove `www.`, remove barra final,
remove `index.html`, apaga o fragmento, apaga ~30 parâmetros de rastreamento
(`utm_*`, `ref`, `fbclid`, `gclid`, …) e ordena os que sobram.

Chave de identidade, em três casos:

1. **Domínio = ferramenta** (caso comum). `midjourney.com/pricing` e
   `midjourney.com/showcase` são a mesma ferramenta.
2. **Host multiprojeto** — um domínio hospeda muitas ferramentas. Aí a chave
   inclui os primeiros segmentos do caminho: `github.com/dono/repo`,
   `huggingface.co/spaces/dono/nome`, `futuretools.io/tools/slug`.
3. **Subdomínio = identidade** — `x.streamlit.app` ≠ `y.streamlit.app`.

O caso 2 foi descoberto quebrando: sem ele, as ~3.000 fichas do futuretools
colapsavam todas na chave `futuretools.io` e a fonte rendia **2** candidatos em
vez de 7.776.

---

## Coleta educada

- `User-Agent` identifica o coletor e dá um e-mail de contato.
- Intervalo mínimo entre requisições **por host**, configurado por fonte.
- `robots.txt` consultado e obedecido. As exceções são poucas, explícitas e
  justificadas em `coletor/rede.py` (hoje: apenas a API oficial do arXiv).
- `429` e `Retry-After` obedecidos; `5xx` com backoff exponencial.
- Cache em disco: reexecutar não refaz requisição.
- Fonte que proíbe coleta **não é varrida** (Reddit) e fonte que bloqueia com
  Cloudflare **não é contornada** (theresanaiforthat, toolify).

---

## Limites conhecidos deste coletor

Escrito aqui de propósito, para não precisar ser descoberto pelo professor.

- **Product Hunt** só entrou pelo feed dos ~50 lançamentos recentes: a API de
  busca exige token. A fonte não cobre o tema; está no conjunto como contraste.
- **Reddit não foi varrido** (robots proíbe). O adaptador existe e está
  desativado, com o motivo no código.
- **Dois diretórios grandes ficaram de fora** por 403 de Cloudflare. O recorte
  comercial que sobrou é o dos sites que deixam passar, não o do mercado.
- **E2 e E3 não são decididos por máquina.** Nenhum regex sabe se há agentes se
  afetando ou se o paywall vem antes da demo. O código marca suspeita; a
  decisão é de leitura.
- **A nota de proxy mede vocabulário, não substância.** Isso foi medido: ao
  ranquear tudo junto pela nota, o topo virou repositório obscuro do GitHub,
  porque todo README de agente escreve "multi-agent", "trace" e "metrics".
  Por isso o pool é montado por cota de fonte, não por top-N global.
- **A varredura vê o que o vocabulário deixa ver.** `coletor/consultas.py` tem
  nove facetas; o que não está nelas não existe nesta lista.
