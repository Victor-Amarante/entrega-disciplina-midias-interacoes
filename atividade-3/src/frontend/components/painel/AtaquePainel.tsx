"use client";

import { useEffect, useState } from "react";
import { pct, usd } from "@/lib/textos";
import type { PropsPainel } from "./props";

export function AtaquePainel({ painel }: PropsPainel) {
  const at = painel.ataque;
  const e = painel.enquete;
  const [injetados, setInjetados] = useState(0);
  const [rodando, setRodando] = useState(false);
  const maximo = at?.sinteticos.length ?? 0;

  useEffect(() => {
    if (!rodando || !at) return;
    if (injetados >= Math.min(at.necessarios, maximo)) {
      setRodando(false);
      return;
    }
    const id = setTimeout(() => setInjetados((n) => n + 1), 900);
    return () => clearTimeout(id);
  }, [rodando, injetados, at, maximo]);

  if (!at) return null;

  const extraA = at.alvo === "a" ? injetados : 0;
  const extraB = at.alvo === "b" ? injetados : 0;
  const totalA = at.votos_a + extraA;
  const totalB = at.votos_b + extraB;
  const total = Math.max(1, totalA + totalB);
  const virou = injetados >= at.necessarios;
  const opcaoAlvo = at.alvo === "a" ? e.opcao_a : e.opcao_b;
  const ultimos = at.sinteticos.slice(0, injetados).reverse();

  return (
    <div className="coluna" style={{ gap: 20 }}>
      <div className="cartao">
        <h2>{e.pergunta}</h2>
        <Barra rotulo={e.opcao_a} humanos={at.votos_a} extras={extraA} total={total} />
        <div style={{ height: 10 }} />
        <Barra rotulo={e.opcao_b} humanos={at.votos_b} extras={extraB} total={total} />
        <p className="suave pequeno" style={{ marginTop: 10 }}>
          Votos da turma: {at.votos_a} × {at.votos_b}. Em laranja, respostas sintéticas.
        </p>
      </div>

      <div className="grade" style={{ alignItems: "start" }}>
        <div className="cartao">
          <div className="numero-grande" style={{ color: "var(--maquina)" }}>{at.necessarios}</div>
          <div className="rotulo-numero">respostas sintéticas bastam para virar para “{opcaoAlvo}”</div>
          <div style={{ marginTop: 16 }}>
            {at.status_sinteticos === "gerando" && <p className="suave pulsando">Escrevendo as respostas falsas…</p>}
            {at.status_sinteticos === "erro" && <p className="erro">Falhou ao gerar as respostas. Volte uma fase e avance de novo.</p>}
            {at.status_sinteticos === "pronto" && !virou && (
              <button className="botao maquina" disabled={rodando} onClick={() => setRodando(true)}>
                {rodando ? "Injetando…" : "Injetar respostas sintéticas"}
              </button>
            )}
            {virou && <p style={{ fontSize: "1.2rem", fontWeight: 700 }}>Virou. 🎯</p>}
          </div>
        </div>

        {virou && (
          <div className="cartao">
            <h3>E se as armadilhas da turma estivessem no questionário?</h3>
            {at.necessarios_com_defesa !== null ? (
              <p>
                Na caçada, vocês marcaram {pct(at.taxa_deteccao)} dos agentes como máquina. Com essa defesa, o
                atacante precisaria de <strong>{at.necessarios_com_defesa}</strong> respostas sintéticas em vez de{" "}
                {at.necessarios}
                {at.humanos_barrados > 0 && (
                  <>
                    , e a mesma defesa barraria por engano uns <strong>{at.humanos_barrados}</strong> humanos da turma
                  </>
                )}
                .
              </p>
            ) : (
              <p className="suave">A caçada não teve vereditos suficientes para estimar a defesa.</p>
            )}
            {at.custo_ataque_usd !== null && (
              <p className="suave">
                Custo do ataque, ao preço de API de hoje: cerca de {usd(at.custo_ataque_usd)} ({usd(at.custo_medio_agente_usd)} por resposta).
              </p>
            )}
          </div>
        )}
      </div>

      {ultimos.length > 0 && (
        <div className="cartao">
          <h3>Justificativas injetadas</h3>
          {ultimos.map((v, i) => (
            <div key={ultimos.length - i} className="resposta" style={{ cursor: "default" }}>
              <div className="pergunta">sintético #{ultimos.length - i} · {opcaoAlvo}</div>
              <div>{v.justificativa}</div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

function Barra({ rotulo, humanos, extras, total }: { rotulo: string; humanos: number; extras: number; total: number }) {
  return (
    <div>
      <div className="linha" style={{ marginBottom: 4 }}>
        <strong>{rotulo}</strong>
        <span className="espaco" />
        <span>{humanos + extras}</span>
      </div>
      <div className="barra-voto">
        <div style={{ width: `${(humanos / total) * 100}%`, background: "var(--humano)", color: "#062a22" }}>
          {humanos > 0 ? humanos : ""}
        </div>
        <div style={{ width: `${(extras / total) * 100}%`, background: "var(--maquina)", color: "#2b0d05" }}>
          {extras > 0 ? `+${extras}` : ""}
        </div>
      </div>
    </div>
  );
}
