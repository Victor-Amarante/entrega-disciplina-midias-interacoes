"use client";

import { useEffect, useState } from "react";
import type { PropsFase } from "./props";

export function Questionario({ visao, enviar }: PropsFase) {
  const perguntas = visao.perguntas ?? [];
  const salvas = visao.minhas_respostas ?? {};
  const jaEnviou = Object.keys(salvas).length > 0;
  const [respostas, setRespostas] = useState<Record<string, string>>(salvas);
  const [editando, setEditando] = useState(!jaEnviou);
  const [erro, setErro] = useState<string | null>(null);
  const [enviando, setEnviando] = useState(false);

  // Recarregou a página depois de enviar: mostra o que já foi salvo.
  useEffect(() => {
    if (jaEnviou && !editando) setRespostas(salvas);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [jaEnviou]);

  const faltam = perguntas.filter((p) => !(respostas[p.id] ?? "").trim()).length;

  async function mandar(e: React.FormEvent) {
    e.preventDefault();
    setEnviando(true);
    setErro(null);
    try {
      await enviar("/respostas", { respostas });
      setEditando(false);
    } catch (e) {
      setErro((e as Error).message);
    }
    setEnviando(false);
  }

  if (!editando)
    return (
      <div className="cartao centro" style={{ padding: "36px 20px" }}>
        <h2>Respostas enviadas ✓</h2>
        <p className="suave">Os agentes estão respondendo às mesmas perguntas agora. Daqui a pouco começa a caçada.</p>
        <button className="botao secundario" onClick={() => setEditando(true)}>
          Editar minhas respostas
        </button>
      </div>
    );

  return (
    <form className="coluna" onSubmit={mandar}>
      <div>
        <h2>Responda como você mesmo</h2>
        <p className="suave">Do jeito que você responderia a uma pesquisa no celular. Ninguém vai saber que foi você.</p>
      </div>
      {perguntas.map((p, i) => (
        <div key={p.id} className="cartao">
          <label htmlFor={p.id}>
            <span className="suave">{i + 1}.</span> {p.texto}
          </label>
          <textarea
            id={p.id}
            value={respostas[p.id] ?? ""}
            onChange={(e) => setRespostas({ ...respostas, [p.id]: e.target.value })}
            maxLength={500}
          />
        </div>
      ))}
      {erro && <p className="erro">{erro}</p>}
      <div className="barra-inferior">
        <div>
          <button className="botao cheio" disabled={faltam > 0 || enviando}>
            {faltam > 0 ? `Faltam ${faltam}` : "Enviar respostas"}
          </button>
        </div>
      </div>
    </form>
  );
}
