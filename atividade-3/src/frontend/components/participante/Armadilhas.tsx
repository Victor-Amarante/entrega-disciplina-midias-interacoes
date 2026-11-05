"use client";

import { useState } from "react";
import { NOME_TIPO, TIPOS } from "@/lib/textos";
import type { TipoPergunta } from "@/lib/tipos";
import { Aguarde } from "@/components/ui/Aguarde";
import type { PropsFase } from "./props";

export function Armadilhas({ visao, enviar }: PropsFase) {
  const minhas = visao.minhas_armadilhas ?? [];
  const limite = visao.limite_armadilhas ?? 2;
  const [tipo, setTipo] = useState<TipoPergunta>("local");
  const [texto, setTexto] = useState("");
  const [erro, setErro] = useState<string | null>(null);
  const [enviando, setEnviando] = useState(false);
  const atual = TIPOS.find((t) => t.tipo === tipo)!;

  if (visao.armadilhas_encerradas)
    return <Aguarde titulo="Armadilhas encerradas" texto="O questionário já foi montado. Aguarde a próxima fase." />;

  async function mandar(e: React.FormEvent) {
    e.preventDefault();
    setEnviando(true);
    setErro(null);
    try {
      await enviar("/armadilhas", { texto: texto.trim(), tipo });
      setTexto("");
    } catch (e) {
      setErro((e as Error).message);
    }
    setEnviando(false);
  }

  return (
    <div className="coluna">
      <div>
        <h2>Escreva uma pergunta que pegue um bot</h2>
        <p className="suave">
          Você é o instituto de pesquisa. Agentes de IA com persona de desenvolvedor de software vão responder ao mesmo
          questionário que a turma. Que pergunta um humano responde fácil e uma máquina erra?
        </p>
      </div>

      {minhas.length < limite && (
        <form className="cartao coluna" onSubmit={mandar}>
          <div className="linha">
            {TIPOS.map((t) => (
              <button
                type="button"
                key={t.tipo}
                className={`chip ${t.tipo === tipo ? "ativo" : ""}`}
                onClick={() => setTipo(t.tipo)}
              >
                {t.nome}
              </button>
            ))}
          </div>
          <p className="suave pequeno" style={{ margin: 0 }}>{atual.dica}</p>
          <textarea
            value={texto}
            onChange={(e) => setTexto(e.target.value)}
            placeholder={`Ex.: ${atual.exemplo}`}
            maxLength={300}
          />
          <button className="botao cheio" disabled={texto.trim().length < 5 || enviando}>
            Mandar armadilha
          </button>
          {erro && <p className="erro">{erro}</p>}
        </form>
      )}

      {minhas.length > 0 && (
        <div className="cartao">
          <p className="suave pequeno">
            Suas armadilhas ({minhas.length}/{limite}). O apresentador escolhe quais entram no questionário.
          </p>
          {minhas.map((p) => (
            <div key={p.id} className="linha" style={{ padding: "8px 0", borderTop: "1px solid var(--borda)" }}>
              <div className="espaco">
                <span className="chip">{NOME_TIPO[p.tipo]}</span>
                <div style={{ marginTop: 6 }}>{p.texto}</div>
              </div>
              <button className="botao secundario pequeno" onClick={() => enviar(`/armadilhas/${p.id}`, undefined, "DELETE")}>
                Apagar
              </button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
