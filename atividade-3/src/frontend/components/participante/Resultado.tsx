"use client";

import type { PropsFase } from "./props";

export function Resultado({ visao }: PropsFase) {
  const cartoes = visao.cartoes ?? [];
  const r = visao.meu_resultado;
  return (
    <div className="coluna">
      <div className="cartao centro" style={{ padding: "28px 20px" }}>
        <div className="numero-grande">
          {r?.acertos ?? 0}/{r?.total ?? 0}
        </div>
        <div className="rotulo-numero">acertos seus. O acaso daria metade.</div>
      </div>

      <div className="cartao">
        <h3>Quem era quem nos seus cartões</h3>
        {cartoes.map((c) => {
          const acertou = c.meu_veredito === c.verdade;
          return (
            <div key={c.id} className="linha" style={{ padding: "10px 0", borderTop: "1px solid var(--borda)" }}>
              <strong>#{c.rotulo}</strong>
              <span className={`chip ${c.verdade}`}>
                {c.verdade === "maquina" ? `🤖 ${c.persona ?? "agente"}${c.com_busca ? " · com busca" : ""}` : "🧑 humano"}
              </span>
              <span className="espaco" />
              <span className="pequeno">
                {c.meu_veredito ? (acertou ? "✓ acertou" : "✗ errou") : <span className="suave">não julgou</span>}
              </span>
            </div>
          );
        })}
      </div>
      <p className="suave centro pequeno">O telão mostra o placar da turma.</p>
    </div>
  );
}
