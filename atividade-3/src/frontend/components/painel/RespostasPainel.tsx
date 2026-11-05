"use client";

import type { PropsPainel } from "./props";
import { Progresso } from "@/components/ui/Progresso";

export function RespostasPainel({ painel, acao }: PropsPainel) {
  const prontos = painel.agentes.filter((a) => a.status === "pronto").length;
  const total = painel.participantes.length;

  return (
    <div className="coluna">
      <div className="grade">
        <div className="cartao">
          <div className="numero-grande">
            {painel.respostas_humanas}/{total}
          </div>
          <div className="rotulo-numero">humanos responderam</div>
          <div style={{ marginTop: 12 }}><Progresso feito={painel.respostas_humanas} total={total} /></div>
        </div>
        <div className="cartao">
          <div className="numero-grande">
            {prontos}/{painel.agentes.length}
          </div>
          <div className="rotulo-numero">agentes responderam</div>
          <div style={{ marginTop: 12 }}><Progresso feito={prontos} total={painel.agentes.length} /></div>
        </div>
      </div>

      <div className="cartao">
        <h3>Agentes</h3>
        <p className="suave pequeno">
          Cada um tem uma persona de desenvolvedor de software e recebe as mesmas perguntas. Os marcados com 🔎 podem pesquisar na web.
        </p>
        <div className="grade" style={{ gridTemplateColumns: "repeat(auto-fill, minmax(180px, 1fr))", gap: 10 }}>
          {painel.agentes.map((a, i) => (
            <div key={a.id} className="cartao" style={{ padding: 12, margin: 0 }}>
              <div className="linha">
                <strong>Agente {i + 1}</strong>
                {a.com_busca && <span title="com busca na web">🔎</span>}
                <span className="espaco" />
                {a.status === "pendente" && <span className="pulsando">⏳</span>}
                {a.status === "pronto" && <span>✓ {a.segundos}s</span>}
                {a.status === "erro" && <span className="erro">erro</span>}
              </div>
              {a.status === "erro" && (
                <>
                  <p className="suave pequeno" style={{ margin: "6px 0" }}>{a.erro}</p>
                  <button className="botao secundario pequeno" onClick={() => acao(`/agentes/${a.id}/tentar-de-novo`, {})}>
                    Tentar de novo
                  </button>
                </>
              )}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
