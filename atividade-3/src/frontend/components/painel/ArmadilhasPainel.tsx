"use client";

import { useState } from "react";
import { NOME_TIPO, TIPOS } from "@/lib/textos";
import type { PerguntaPainel } from "@/lib/tipos";
import type { PropsPainel } from "./props";

export function ArmadilhasPainel({ painel, acao }: PropsPainel) {
  const [nova, setNova] = useState("");
  const fechado = painel.questionario_fechado;
  const daTurma = painel.perguntas.filter((p) => p.autor);
  const doInstituto = painel.perguntas.filter((p) => !p.autor);
  const selecionadas = painel.perguntas.filter((p) => p.selecionada).length;
  const max = painel.config.max_perguntas;
  const lista = fechado
    ? painel.perguntas.filter((p) => p.no_questionario)
    : [...doInstituto, ...daTurma];

  return (
    <div className="grade" style={{ gridTemplateColumns: "1fr 2fr", alignItems: "start" }}>
      <div className="coluna">
        <div className="cartao">
          <h3>Tipos de armadilha</h3>
          {TIPOS.map((t) => (
            <div key={t.tipo} style={{ marginBottom: 10 }}>
              <strong>{t.nome}</strong>
              <div className="suave pequeno">{t.dica}</div>
            </div>
          ))}
        </div>
        <div className="cartao">
          <div className="numero-grande">{daTurma.length}</div>
          <div className="rotulo-numero">armadilhas recebidas de {painel.participantes.length} pessoas</div>
        </div>
      </div>

      <div className="coluna">
        <div className="linha">
          <h2 style={{ margin: 0 }}>
            Questionário: {fechado ? lista.length : selecionadas}/{max}
          </h2>
          <span className="espaco" />
          {!fechado && (
            <button className="botao secundario pequeno" onClick={() => acao("/perguntas/sortear", {})}>
              Sortear armadilhas
            </button>
          )}
        </div>

        {fechado ? (
          <p className="aviso">
            O questionário já foi fechado e os agentes já responderam a estas perguntas. Para mudar, crie uma sala nova.
          </p>
        ) : (
          <p className="suave pequeno" style={{ margin: 0 }}>
            Do banco do instituto, entrou uma pergunta de cada tipo, sorteada. Clique em qualquer pergunta, do instituto
            ou da turma, para incluir ou tirar, até completar as vagas. Se nenhuma da turma estiver marcada ao avançar, o
            sorteio escolhe variando os tipos e completa com o banco.
          </p>
        )}

        <div className="cartao">
          {lista.map((p) => (
            <Linha key={p.id} pergunta={p} fechado={fechado} alternar={() => acao(`/perguntas/${p.id}/alternar`, {})} />
          ))}
          {!fechado && daTurma.length === 0 && (
            <p className="suave pulsando" style={{ marginTop: 12 }}>Esperando as armadilhas da turma…</p>
          )}
        </div>

        {!fechado && (
          <form
            className="linha"
            style={{ flexWrap: "nowrap" }}
            onSubmit={(e) => {
              e.preventDefault();
              acao("/perguntas", { texto: nova, tipo: "generica" }).then(() => setNova(""));
            }}
          >
            <input value={nova} onChange={(e) => setNova(e.target.value)} placeholder="Acrescentar uma pergunta do instituto" />
            <button className="botao secundario" disabled={nova.trim().length < 5}>
              Acrescentar
            </button>
          </form>
        )}
      </div>
    </div>
  );
}

function Linha({ pergunta: p, fechado, alternar }: { pergunta: PerguntaPainel; fechado: boolean; alternar: () => void }) {
  return (
    <label
      className="linha"
      style={{
        padding: "10px 0",
        borderBottom: "1px solid var(--borda)",
        fontWeight: 400,
        cursor: fechado ? "default" : "pointer",
        flexWrap: "nowrap",
      }}
    >
      {fechado ? (
        <span style={{ width: 20, textAlign: "center", flex: "none" }} title="Questionário fechado">
          🔒
        </span>
      ) : (
        <input type="checkbox" checked={p.selecionada} onChange={alternar} style={{ width: 20, height: 20, flex: "none" }} />
      )}
      <div className="espaco">
        <div>{p.texto}</div>
        <div className="linha" style={{ marginTop: 4 }}>
          <span className="chip">{NOME_TIPO[p.tipo]}</span>
          <span className="suave pequeno">{p.autor ?? "instituto"}</span>
        </div>
      </div>
    </label>
  );
}
