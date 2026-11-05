"use client";

import { QRCodeSVG } from "qrcode.react";
import { useEffect, useState } from "react";
import type { PropsPainel } from "./props";

export function linkDaSala(codigo: string) {
  return typeof window === "undefined" ? "" : `${window.location.origin}/sala/?c=${codigo}`;
}

export function Entrada({ painel }: PropsPainel) {
  const [link, setLink] = useState("");
  useEffect(() => setLink(linkDaSala(painel.codigo)), [painel.codigo]);

  return (
    <div className="grade" style={{ gridTemplateColumns: "minmax(280px, 420px) 1fr", alignItems: "start" }}>
      <div className="cartao centro">
        {link && (
          <div style={{ background: "#fff", padding: 16, borderRadius: 12, display: "inline-block" }}>
            <QRCodeSVG value={link} size={320} style={{ width: "100%", height: "auto", maxWidth: 320 }} />
          </div>
        )}
        <p style={{ marginTop: 12, wordBreak: "break-all" }}>{link}</p>
        <p className="suave">
          ou entre no site e digite <strong style={{ color: "var(--texto)", letterSpacing: ".15em" }}>{painel.codigo}</strong>
        </p>
      </div>
      <div className="coluna">
        <div>
          <div className="numero-grande">{painel.participantes.length}</div>
          <div className="rotulo-numero">pessoas na sala</div>
        </div>
        <div className="linha">
          {painel.participantes.map((p) => (
            <span key={p.id} className="chip">{p.apelido}</span>
          ))}
        </div>
        <div className="cartao">
          <h3>Como funciona</h3>
          <ol className="suave" style={{ margin: 0, paddingLeft: 20 }}>
            <li>Vocês escrevem perguntas-armadilha para pegar bots.</li>
            <li>Todo mundo responde ao questionário, junto com {painel.config.n_agentes} agentes de IA.</li>
            <li>Cada um recebe cartões anônimos e diz: gente ou máquina?</li>
            <li>Placar: qual armadilha funcionou, e quem foi acusado injustamente.</li>
            <li>Enquete: quantos bots bastam para virar o resultado da turma.</li>
          </ol>
        </div>
      </div>
    </div>
  );
}
