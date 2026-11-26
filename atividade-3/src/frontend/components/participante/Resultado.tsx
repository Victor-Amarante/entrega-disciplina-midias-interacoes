"use client";

import { pct } from "@/lib/textos";
import type { Cartao } from "@/lib/tipos";
import type { PropsFase } from "./props";

export function Resultado({ visao }: PropsFase) {
  const cartoes = visao.cartoes ?? [];
  const r = visao.meu_resultado;
  const total = r?.total ?? 0;
  const julgados = cartoes.filter((c) => c.meu_veredito);
  const maquinas = julgados.filter((c) => c.verdade === "maquina").length;
  const semOlhar = Math.max(maquinas, julgados.length - maquinas);
  return (
    <div className="coluna">
      <div className="cartao centro" style={{ padding: "28px 20px" }}>
        <div className="numero-grande">
          {r?.acertos ?? 0}/{total}
        </div>
        <div className="rotulo-numero">
          cartões certos. Sem olhar as respostas, você acertaria {semOlhar}.
        </div>
        {visao.acerto_turma != null && (
          <p className="pequeno" style={{ marginTop: 12, marginBottom: 0 }}>
            A turma toda acertou {pct(visao.acerto_turma)} dos vereditos.
          </p>
        )}
      </div>

      <div className="cartao">
        <h3>Cartão por cartão</h3>
        <p className="suave pequeno">O que você disse, o que era de verdade e a resposta que você marcou como pista.</p>
        {cartoes.map((c) => (
          <Linha key={c.id} c={c} />
        ))}
      </div>
      <p className="suave centro pequeno">O telão mostra o placar da turma.</p>
    </div>
  );
}

function Linha({ c }: { c: Cartao }) {
  const acertou = c.meu_veredito === c.verdade;
  const pista = c.respostas.findIndex((r) => r.pergunta_id === c.minha_pista);
  return (
    <div style={{ padding: "10px 0", borderTop: "1px solid var(--borda)" }}>
      <div className="linha">
        <strong>#{c.rotulo}</strong>
        <span className={`chip ${c.verdade}`}>
          era {c.verdade === "maquina" ? `🤖 ${c.persona ?? "agente"}` : "🧑 humano"}
        </span>
        <span className="espaco" />
        <span className="pequeno" style={{ color: c.meu_veredito ? (acertou ? "var(--certo)" : "var(--perigo)") : undefined }}>
          {c.meu_veredito ? (acertou ? "✓ acertou" : "✗ errou") : <span className="suave">não julgou</span>}
        </span>
      </div>
      {c.meu_veredito && (
        <div className="suave pequeno" style={{ marginTop: 4 }}>
          Você disse {c.meu_veredito === "maquina" ? "🤖 máquina" : "🧑 humano"}
          {pista >= 0 && <> · pista: P{pista + 1}, “{c.respostas[pista].pergunta}”</>}
        </div>
      )}
    </div>
  );
}
