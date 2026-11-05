"use client";

import { useEffect, useState } from "react";
import type { PropsPainel } from "./props";

export function EnquetePainel({ painel, acao }: PropsPainel) {
  const e = painel.enquete;
  const [pergunta, setPergunta] = useState(e.pergunta);
  const [a, setA] = useState(e.opcao_a);
  const [b, setB] = useState(e.opcao_b);
  useEffect(() => {
    setPergunta(e.pergunta);
    setA(e.opcao_a);
    setB(e.opcao_b);
  }, [e.pergunta, e.opcao_a, e.opcao_b]);
  const mudou = pergunta !== e.pergunta || a !== e.opcao_a || b !== e.opcao_b;

  return (
    <div className="coluna" style={{ gap: 20 }}>
      <div className="cartao centro" style={{ padding: "32px 20px" }}>
        <div className="titulo-fase">Ato 2 · Agora vocês são o atacante</div>
        <h1 style={{ fontSize: "clamp(1.8rem, 4vw, 3rem)" }}>{e.pergunta}</h1>
        <div className="linha" style={{ justifyContent: "center", gap: 16, fontSize: "1.3rem" }}>
          <span className="chip" style={{ fontSize: "1.1rem" }}>{e.opcao_a}</span>
          <span className="chip" style={{ fontSize: "1.1rem" }}>{e.opcao_b}</span>
        </div>
        <div className="numero-grande" style={{ marginTop: 24 }}>{e.votos}</div>
        <div className="rotulo-numero">votos (o resultado fica escondido até o ataque)</div>
      </div>

      {e.votos === 0 && (
        <form
          className="cartao coluna"
          onSubmit={(ev) => {
            ev.preventDefault();
            acao("/enquete", { pergunta, opcao_a: a, opcao_b: b }, "PUT");
          }}
        >
          <h3 style={{ margin: 0 }}>Trocar o tema (antes do primeiro voto)</h3>
          <input value={pergunta} onChange={(ev) => setPergunta(ev.target.value)} />
          <div className="linha" style={{ flexWrap: "nowrap" }}>
            <input value={a} onChange={(ev) => setA(ev.target.value)} />
            <input value={b} onChange={(ev) => setB(ev.target.value)} />
          </div>
          <button className="botao secundario" disabled={!mudou}>Salvar enquete</button>
        </form>
      )}
    </div>
  );
}
