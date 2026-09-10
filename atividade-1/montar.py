"""Fase E — monta os artefatos da entrega.

Produz, em `entrega/`:
  500-ferramentas.jsonl   nome, url, descricao, categoria, imagem  (formato preferido)
  500-ferramentas.csv     mesmo conteúdo, com cabeçalho
  500-ferramentas.md      mesmo conteúdo, com links clicáveis

SOBRE A DESCRIÇÃO — leia antes de confiar no arquivo
----------------------------------------------------
O enunciado exige três frases nesta ordem: (a) o que entra e o que sai,
(b) onde encaixa no trabalho de quem usa, (c) qual é o limite. E proíbe
adjetivo de propaganda.

Este script monta a descrição de DUAS fontes, e marca qual foi usada no campo
`descricao_origem`:

  "redigida"   — escrita à mão em `descricoes/*.jsonl`, a partir do texto da
                 página. É a versão boa.
  "composta"   — montada mecanicamente a partir de fatos VERIFICADOS que a
                 coleta trouxe (SDK, estado do runtime, autor, tags, meta tag
                 da própria página, status HTTP). Não inventa nada, mas é seca
                 e às vezes a alínea (c) vira "não consegui apurar".

Item com `descricao_origem: composta` ainda não recebeu leitura humana. O
número dos dois aparece no fim da execução, de propósito: se a maioria estiver
"composta", o documento das 500 ainda não está pronto, por mais que exista.

O favicon sai do HTML já em cache (`<link rel="icon">`), sem nenhuma requisição
nova. Quando a página não declara um, cai para `/favicon.ico` do domínio — que
pode não existir. Nenhum serviço de terceiros é usado para gerar ícone.

Uso:
    uv run python atividade-1/montar.py
    uv run python atividade-1/montar.py --quantos 500
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from datetime import datetime
from pathlib import Path
from urllib.parse import urljoin, urlsplit

from selectolax.parser import HTMLParser

RAIZ = Path(__file__).parent
DADOS = RAIZ / "dados"
CACHE = DADOS / "cache_paginas"
SAIDA = RAIZ / "entrega"
DESCRICOES = RAIZ / "descricoes"

# Categoria = faceta do vocabulário, traduzida para rótulo de catálogo.
ROTULO_FACETA = {
    "sociedade_simulada": "Sociedade simulada de agentes",
    "sandbox_ambiente": "Sandbox e ambiente de simulação",
    "observabilidade_replay": "Observabilidade e replay de agentes",
    "avaliacao_arena": "Avaliação e arena de agentes",
    "npc_jogos": "NPC e mundo de jogo com IA",
    "usuarios_sinteticos": "Usuários sintéticos e pesquisa",
    "abm_classico": "Modelagem baseada em agentes (ABM)",
    "economia_negociacao": "Simulação de mercado e negociação",
    "robotica_mundo": "Agentes corporificados e robótica",
    "amplo_comercial": "Catálogo comercial de IA",
    "amostra_de_contraste": "Amostra de contraste (Product Hunt)",
}


# Fallback de categoria para candidatos coletados antes de a faceta existir no
# adaptador. Deriva da consulta que trouxe o item — que está gravada no log.
FACETA_POR_CONSULTA = {
    "generative agents": "sociedade_simulada", "ai town": "sociedade_simulada",
    "social simulation": "sociedade_simulada", "agent society": "sociedade_simulada",
    "artificial society": "sociedade_simulada", "emergent": "sociedade_simulada",
    "sandbox": "sandbox_ambiente", "playground": "sandbox_ambiente",
    "environment": "sandbox_ambiente", "virtual world": "sandbox_ambiente",
    "no-code": "sandbox_ambiente", "platform": "sandbox_ambiente",
    "observability": "observabilidade_replay", "trace": "observabilidade_replay",
    "replay": "observabilidade_replay", "visualiz": "observabilidade_replay",
    "timeline": "observabilidade_replay",
    "benchmark": "avaliacao_arena", "arena": "avaliacao_arena",
    "evaluation": "avaliacao_arena", "leaderboard": "avaliacao_arena",
    "competition": "avaliacao_arena",
    "npc": "npc_jogos", "game": "npc_jogos", "villager": "npc_jogos",
    "synthetic user": "usuarios_sinteticos", "persona": "usuarios_sinteticos",
    "focus group": "usuarios_sinteticos", "customer": "usuarios_sinteticos",
    "agent based model": "abm_classico", "crowd": "abm_classico",
    "social science": "abm_classico",
    "market": "economia_negociacao", "negotiation": "economia_negociacao",
    "auction": "economia_negociacao", "supply chain": "economia_negociacao",
    "embodied": "robotica_mundo", "robot": "robotica_mundo", "3d": "robotica_mundo",
}


def faceta_de(c: dict) -> str:
    f = c.get("faceta")
    if f:
        return f
    alvo = " ".join([str((c.get("sinais") or {}).get("tag", "")),
                     str(c.get("consulta", "")), c.get("nome", "")]).lower()
    for chave, faceta in FACETA_POR_CONSULTA.items():
        if chave in alvo:
            return faceta
    if c.get("fonte") == "itchio":
        return "npc_jogos"
    if c.get("fonte", "").startswith("diretorios"):
        return "amplo_comercial"
    return "sandbox_ambiente"


def nome_bom(c: dict) -> str:
    """Prefere o nome do PRODUTO ao identificador do repositório.

    `dtyq/magic` é o caminho do repositório; a página se chama MagiCrew. Para o
    catálogo da turma vale o nome que a ferramenta usa, não o do dono do repo.
    """
    bruto = (c.get("nome") or "").strip()
    titulo = (c.get("titulo_pagina") or "").strip()
    # "Show HN: Neural Abyss – PyTorch multi-agent combat simulator" é título de
    # post, não nome de ferramenta. No catálogo da turma vale o nome do produto.
    for prefixo in ("Show HN:", "Ask HN:", "Launch HN:", "Tell HN:",
                    "Show PH:", "Ask PH:", "Show:", "Launch:"):
        if bruto.startswith(prefixo):
            bruto = bruto[len(prefixo):].strip()
            for sep in (" – ", " — ", " - ", ": ", ", "):
                if sep in bruto and len(bruto.split(sep)[0]) >= 3:
                    bruto = bruto.split(sep)[0].strip()
                    break
            break
    # corta sufixo de site: "MagiCrew — plataforma X" -> "MagiCrew"
    for sep in (" — ", " – ", " | ", " - ", " · ", ": "):
        if titulo.count(sep) and len(titulo.split(sep)[0]) >= 3:
            titulo = titulo.split(sep)[0].strip()
            break
    parece_repo = "/" in bruto and " " not in bruto
    if (parece_repo or not bruto) and 2 < len(titulo) <= 60:
        return titulo
    # nome do itch.io às vezes vem grudado com uma URL de devlog
    if "http" in bruto:
        bruto = bruto.split("http")[0].strip()
    return bruto or titulo or c.get("url", "")


def carregar_redigidas() -> dict[str, str]:
    """Descrições escritas à mão, chaveadas por URL coletada."""
    fora: dict[str, str] = {}
    if not DESCRICOES.exists():
        return fora
    for arq in sorted(DESCRICOES.glob("*.jsonl")):
        for linha in arq.read_text(encoding="utf-8").splitlines():
            if not linha.strip():
                continue
            try:
                d = json.loads(linha)
            except json.JSONDecodeError:
                continue
            if d.get("url_coletada") and d.get("descricao"):
                fora[d["url_coletada"]] = d["descricao"].strip()
    return fora


def favicon(url_final: str) -> str:
    """Tira o ícone do HTML que já está em cache. Zero requisição nova."""
    arq = CACHE / (hashlib.sha256(url_final.encode()).hexdigest() + ".json")
    if arq.exists():
        try:
            html = json.loads(arq.read_text()).get("html", "")
        except Exception:
            html = ""
        if html:
            a = HTMLParser(html)
            for sel in ("link[rel='icon']", "link[rel='shortcut icon']",
                        "link[rel='apple-touch-icon']", "link[rel='icon shortcut']"):
                n = a.css_first(sel)
                if n and n.attributes.get("href"):
                    return urljoin(url_final, n.attributes["href"])
            og = a.css_first("meta[property='og:image']")
            if og and og.attributes.get("content"):
                return urljoin(url_final, og.attributes["content"])
    partes = urlsplit(url_final)
    if partes.netloc:
        return f"{partes.scheme or 'https'}://{partes.netloc}/favicon.ico"
    return ""


def compor(c: dict) -> str:
    """Descrição mecânica a partir de fatos verificados. Não inventa.

    Segue a ordem exigida: (a) o que é/o que dá, (b) onde encaixa, (c) limite.
    Quando um dos três não foi apurado, diz que não foi apurado — o enunciado é
    explícito de que isso é melhor que preencher.
    """
    fonte = c.get("fonte", "")
    sinais = c.get("sinais") or {}
    hf = c.get("hf") or {}
    meta = (c.get("meta_pagina") or "").strip()
    titulo = (c.get("titulo_pagina") or "").strip()
    ev = c.get("evidencia") or {}

    # (a) o que entra e o que sai
    if meta:
        a = meta.rstrip(".") + "."
    elif titulo:
        a = f"Página se identifica como “{titulo}”; a descrição do que entra e do que sai não foi apurada."
    else:
        a = "Não consegui apurar o que entra e o que sai."

    # (b) onde encaixa
    encaixes = []
    if ev.get("P1"):
        encaixes.append("o texto da página menciona vários agentes interagindo")
    if ev.get("P2"):
        encaixes.append("menciona log, replay ou visualização do que acontece")
    if ev.get("P3"):
        encaixes.append("menciona cenário, regra ou parâmetro configurável")
    if ev.get("P4"):
        encaixes.append("menciona métrica, exportação ou resultado analisável")
    b = ("Encaixa no fluxo de quem monta simulação com agentes: "
         + "; ".join(encaixes) + ".") if encaixes else \
        "Onde encaixa no trabalho de quem usa: não consegui apurar pelo texto da página."

    # (c) limite — a alínea que salva a atividade
    limites = []
    if fonte == "huggingface:space":
        estagio = hf.get("estagio") or "?"
        limites.append(f"é um Space do Hugging Face (SDK {hf.get('sdk') or '?'}), "
                       f"estado do runtime no momento da coleta: {estagio}")
        if estagio == "SLEEPING":
            limites.append("Space dormindo acorda ao ser aberto, mas leva o tempo de subir o container")
        if hf.get("gated"):
            limites.append("acesso restrito (gated)")
    elif fonte == "itchio":
        limites.append("é obra publicada no itch.io para jogar, não ferramenta de trabalho")
        if sinais.get("autor"):
            limites.append(f"publicado por {sinais['autor']}")
        limites.append("preço não apurado")
    elif fonte.startswith("diretorios"):
        limites.append("veio de catálogo comercial de IA, onde a listagem pode ser paga "
                       "e o link pode estar desatualizado")
    elif fonte == "github":
        limites.append("o link é a página do projeto declarada no repositório; "
                       "exige conferir se há aplicação hospedada ou só documentação")
    if ev.get("suspeita_paywall"):
        limites.append("a página tem sinal de 'fale com vendas' / trial pago antes de ver funcionando")
    if ev.get("suspeita_agente_unico"):
        limites.append("a página tem sinal de assistente de agente único, "
                       "o que reprova pelo critério E2 e precisa de conferência")
    if not ev.get("link_vivo"):
        limites.append(f"link NÃO respondeu 200 na verificação (status {ev.get('status')})")
    if not limites:
        limites.append("preço, requisito e o que ela não faz: não consegui apurar")
    cc = "Limite: " + "; ".join(limites) + "."

    return f"{a} {b} {cc}"


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--quantos", type=int, default=500)
    args = p.parse_args()

    SAIDA.mkdir(parents=True, exist_ok=True)
    itens = [json.loads(l) for l in
             (DADOS / "para_descrever.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
    itens = itens[: args.quantos]
    redigidas = carregar_redigidas()

    linhas = []
    n_redigidas = 0
    for c in itens:
        url = c["url"]
        desc = redigidas.get(c.get("url_coletada") or url)
        origem = "redigida" if desc else "composta"
        n_redigidas += 1 if desc else 0
        if not desc:
            desc = compor(c)
        linhas.append({
            "nome": nome_bom(c),
            "url": url,
            "descricao": " ".join(desc.split()),
            "categoria": ROTULO_FACETA.get(faceta_de(c), "Não classificado"),
            "imagem": favicon(c.get("url_coletada") or url),
            # campos extras: úteis para o aluno peneirar, ignorados pelo catálogo
            "descricao_origem": origem,
            "fonte_da_varredura": c.get("fonte"),
            "nota": c.get("nota"),
            "link_verificado_status": (c.get("evidencia") or {}).get("status"),
        })

    # ---------------------------------------------------------------- JSONL
    alvo = SAIDA / "500-ferramentas.jsonl"
    with alvo.open("w", encoding="utf-8") as f:
        for l in linhas:
            f.write(json.dumps(l, ensure_ascii=False) + "\n")

    # ------------------------------------------------------------------ CSV
    with (SAIDA / "500-ferramentas.csv").open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(linhas[0].keys()) if linhas else
                           ["nome", "url", "descricao", "categoria", "imagem"])
        w.writeheader()
        w.writerows(linhas)

    # ------------------------------------------------------------- Markdown
    md = [f"# As 500 — Entrega 1 (Ferramentas de Inspiração)", "",
          f"Gerado em {datetime.now().astimezone().isoformat(timespec='seconds')} · "
          f"{len(linhas)} itens · {n_redigidas} com descrição redigida, "
          f"{len(linhas) - n_redigidas} com descrição composta automaticamente.", ""]
    por_cat: dict[str, list[dict]] = {}
    for l in linhas:
        por_cat.setdefault(l["categoria"], []).append(l)
    for cat in sorted(por_cat):
        md += [f"## {cat} ({len(por_cat[cat])})", ""]
        for l in por_cat[cat]:
            md.append(f"- **[{l['nome']}]({l['url']})** — {l['descricao']}")
        md.append("")
    (SAIDA / "500-ferramentas.md").write_text("\n".join(md) + "\n", encoding="utf-8")

    print(f"{len(linhas)} itens escritos em entrega/500-ferramentas.{{jsonl,csv,md}}")
    print(f"  descrição redigida à mão: {n_redigidas}")
    print(f"  descrição composta automaticamente: {len(linhas) - n_redigidas}")
    if len(linhas) - n_redigidas > 0:
        print("  -> os 'compostos' ainda não passaram por leitura humana.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
