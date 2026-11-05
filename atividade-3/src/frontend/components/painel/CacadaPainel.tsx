"use client";

import type { PropsPainel } from "./props";
import { Progresso } from "@/components/ui/Progresso";

export function CacadaPainel({ painel }: PropsPainel) {
  const c = painel.cacada;
  const pendentes = painel.agentes.filter((a) => a.status === "pendente").length;
  return (
    <div className="coluna">
      <div className="cartao centro" style={{ padding: "32px 20px" }}>
        <h2>Gente ou máquina?</h2>
        <p className="suave" style={{ fontSize: "1.15rem", margin: 0 }}>
          Cada um recebeu cartões anônimos com as respostas de alguém. Alguns são da turma, outros são agentes.
          Toque na resposta que te entregou a pista e dê o veredito.
        </p>
      </div>
      <div className="grade">
        <div className="cartao">
          <div className="numero-grande">{c.julgamentos}</div>
          <div className="rotulo-numero">vereditos dados</div>
        </div>
        <div className="cartao">
          <div className="numero-grande">
            {c.juizes_concluidos}/{painel.participantes.length}
          </div>
          <div className="rotulo-numero">pessoas terminaram</div>
          <div style={{ marginTop: 12 }}><Progresso feito={c.juizes_concluidos} total={painel.participantes.length} /></div>
        </div>
        <div className="cartao">
          <div className="numero-grande">{c.cartoes_no_jogo}</div>
          <div className="rotulo-numero">respondentes no jogo</div>
        </div>
      </div>
      {pendentes > 0 && <p className="aviso">{pendentes} agente(s) ainda respondendo; entram nos cartões de quem abrir a caçada depois.</p>}
    </div>
  );
}
