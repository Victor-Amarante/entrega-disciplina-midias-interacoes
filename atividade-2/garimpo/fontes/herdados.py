"""Herança da Entrega 1: o que o critério E1 de lá rejeitou POR SER daqui.

Esta não é uma varredura nova — é o reaproveitamento declarado da varredura
anterior, e por isso está isolada num adaptador próprio, com rótulo de fonte
próprio (`herdado:<fonte original>`), para nunca se confundir com coleta feita
agora.

O raciocínio: na Entrega 1 o aluno escolheu como critério eliminatório "não se
abre e usa", e esse critério matou 5.238 candidatos com motivos como
"repositório sem homepage — nada para abrir e usar (é Entrega 2)". Ou seja, a
peneira de lá já separou, com o critério dele e por escrito, um monte de coisa
que é exatamente o objeto desta unidade. Jogar isso fora e varrer de novo os
mesmos endereços seria desperdício de tempo dele e de banda dos servidores.

O que É herdado: repositório de código e link de registro de pacote.
O que NÃO é herdado: paper e página de publicação. Eles foram rejeitados lá por
"é paper, não app", e reprovam aqui também pelo critério E1 desta entrega
("não dá para instalar ou importar") — herdar seria trazer lixo conhecido.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

from . import Contexto

NOME = "herdados"
METODO = (
    "Lê `atividade-1/dados/candidatos.jsonl` e reaplica a função `eliminar()` da peneira "
    "daquela entrega, mantendo apenas os itens que ela rejeitou com motivo de Entrega 2 — "
    "'repositório sem homepage', 'link aponta para hospedagem de código' e link de registro "
    "de pacote. Paper e página de publicação são descartados, porque reprovam também no "
    "critério E1 desta entrega. Nenhuma requisição de rede é feita: são endereços já "
    "coletados, já normalizados e já deduplicados pela mesma regra, e cada um entra com "
    "fonte `herdado:<fonte original>` para poder ser separado da coleta nova a qualquer momento."
)
VIES = (
    "Carrega inteiro o viés da varredura da Entrega 1, porque é a mesma coleta vista pelo "
    "avesso: mesmo vocabulário de nove facetas, mesmas fontes (Hacker News, GitHub, "
    "Hugging Face, itch.io, diretórios), mesmos cegos. Como o vocabulário de lá mirava "
    "AMBIENTE e não biblioteca, o que sobra aqui é enviesado para projeto que se apresenta "
    "como produto — e sub-representa biblioteca de infraestrutura, que ninguém descreve como "
    "'ambiente de simulação'. Não substitui varredura nova; complementa."
)

MOTIVOS_QUE_SAO_ENTREGA_2 = ("repositório sem homepage", "hospedagem de código")
REGISTROS_NA_URL = ("pypi.org/project/", "npmjs.com/package/", "crates.io/crates/",
                    "nuget.org/packages/", "rubygems.org/gems/", "packagist.org/packages/",
                    "pkg.go.dev/", "hex.pm/packages/", "pub.dev/packages/")


def varrer(ctx: Contexto) -> None:
    raiz1 = Path(__file__).resolve().parents[3] / "atividade-1"
    arq = raiz1 / "dados" / "candidatos.jsonl"
    if not arq.exists():
        ctx.log.evento("fonte_pulada", {"fonte": NOME,
                                        "motivo": f"não achei {arq}"})
        return
    if str(raiz1) not in sys.path:
        sys.path.insert(0, str(raiz1))
    from peneirar import eliminar  # a MESMA função que rodou na Entrega 1

    lidos = herdados = 0
    for linha in arq.read_text(encoding="utf-8").splitlines():
        if not linha.strip():
            continue
        try:
            c = json.loads(linha)
        except json.JSONDecodeError:
            continue
        lidos += 1
        motivo = eliminar(c)
        if not motivo:
            continue  # sobreviveu na Entrega 1: é aplicativo, não é desta unidade
        url = c.get("url", "")
        eh_entrega_2 = (any(m in motivo for m in MOTIVOS_QUE_SAO_ENTREGA_2)
                        or any(reg in url for reg in REGISTROS_NA_URL))
        if not eh_entrega_2:
            continue
        sinais = dict(c.get("sinais") or {})
        sinais["herdado_de"] = c.get("fonte")
        sinais["motivo_na_entrega_1"] = motivo
        ctx.log.item(NOME, c.get("fonte", "?"),
                     {"url": url, "nome": c.get("nome"), "motivo_entrega_1": motivo,
                      "fonte_original": c.get("fonte")})
        ctx.deposito.adicionar(
            nome=c.get("nome") or "", url=url,
            fonte=f"herdado:{c.get('fonte')}",
            consulta=c.get("consulta") or "", descricao_fonte=c.get("descricao_fonte") or "",
            sinais=sinais,
        )
        herdados += 1
    ctx.log.evento("herança", {"candidatos_lidos": lidos, "herdados": herdados})
