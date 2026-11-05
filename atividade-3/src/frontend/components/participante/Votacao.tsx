"use client";

import { useState } from "react";
import type { Opcao } from "@/lib/tipos";
import type { PropsFase } from "./props";

export function Votacao({ visao, enviar }: PropsFase) {
  const e = visao.enquete!;
  const aberta = visao.fase === "enquete";
  const [erro, setErro] = useState<string | null>(null);

  async function votar(opcao: Opcao) {
    setErro(null);
    try {
      await enviar("/voto", { opcao });
    } catch (err) {
      setErro((err as Error).message);
    }
  }

  return (
    <div className="coluna">
      <div>
        <h2>{e.pergunta}</h2>
        <p className="suave">
          {aberta
            ? "Vote no que você pensa de verdade. Dá para mudar o voto enquanto a enquete estiver aberta."
            : "Enquete fechada. Agora o telão mostra quantos bots bastariam para virar o resultado."}
        </p>
      </div>
      {(["a", "b"] as Opcao[]).map((op) => {
        const texto = op === "a" ? e.opcao_a : e.opcao_b;
        const meu = e.meu_voto === op;
        return (
          <button
            key={op}
            className={`botao cheio ${meu ? "" : "secundario"}`}
            style={{ padding: "22px 18px", fontSize: "1.1rem" }}
            disabled={!aberta}
            onClick={() => votar(op)}
          >
            {meu ? "✓ " : ""}
            {texto}
          </button>
        );
      })}
      {erro && <p className="erro">{erro}</p>}
    </div>
  );
}
