"use client";

import { useEffect, useState } from "react";
import type { Veredito } from "@/lib/tipos";
import { Aguarde } from "@/components/ui/Aguarde";
import { Progresso } from "@/components/ui/Progresso";
import type { PropsFase } from "./props";

export function Cacada({ visao, enviar }: PropsFase) {
  const cartoes = visao.cartoes ?? [];
  const julgados = cartoes.filter((c) => c.meu_veredito).length;
  const primeiroPendente = cartoes.findIndex((c) => !c.meu_veredito);
  const [indice, setIndice] = useState<number | null>(null);
  const [pista, setPista] = useState<string | null>(null);
  // Disse "máquina" sem marcar pista: pede a resposta que entregou antes de enviar.
  const [pedindoPista, setPedindoPista] = useState(false);
  const [erro, setErro] = useState<string | null>(null);
  const [enviando, setEnviando] = useState(false);

  const atual = indice ?? (primeiroPendente >= 0 ? primeiroPendente : null);
  const cartao = atual !== null ? cartoes[atual] : null;

  useEffect(() => {
    setPista(cartao?.minha_pista ?? null);
    setPedindoPista(false);
  }, [cartao?.id, cartao?.minha_pista]);

  if (cartoes.length === 0)
    return <Aguarde titulo="Preparando os cartões…" texto="Esperando as respostas ficarem prontas." />;

  async function julgar(veredito: Veredito, pistaEscolhida: string | null = pista) {
    if (!cartao) return;
    if (veredito === "maquina" && !pistaEscolhida && !pedindoPista) {
      setPedindoPista(true);
      window.scrollTo({ top: 0, behavior: "smooth" });
      return;
    }
    setEnviando(true);
    setErro(null);
    try {
      await enviar("/julgamentos", {
        respondente_id: cartao.id,
        veredito,
        pista_id: veredito === "maquina" ? pistaEscolhida : null,
      });
      setPedindoPista(false);
      setIndice(null); // volta para o próximo cartão sem veredito
    } catch (e) {
      setErro((e as Error).message);
    }
    setEnviando(false);
  }

  if (!cartao)
    return (
      <div className="coluna">
        <div className="cartao centro" style={{ padding: "32px 20px" }}>
          <h2>Caçada concluída ✓</h2>
          <p className="suave">Você julgou os {cartoes.length} cartões. Olhe para o telão: o placar vem aí.</p>
        </div>
        <ListaDeCartoes visao={visao} aoEscolher={setIndice} />
      </div>
    );

  return (
    <div className="coluna">
      <div className="coluna" style={{ gap: 6 }}>
        <div className="linha pequeno suave">
          <span>Cartão {atual! + 1} de {cartoes.length}</span>
          <span className="espaco" />
          <span>{julgados} julgados</span>
        </div>
        <Progresso feito={julgados} total={cartoes.length} />
      </div>

      <div className="cartao">
        <h2 style={{ marginBottom: 4 }}>Respondente #{cartao.rotulo}</h2>
        {pedindoPista ? (
          <p className="aviso">🤖 Qual resposta te entregou? Toque nela.</p>
        ) : (
          <p className="suave pequeno">
            Gente ou máquina? Se desconfiar, toque na resposta que te entregou a pista.
          </p>
        )}
        {cartao.respostas.map((r) => (
          <button
            key={r.pergunta_id}
            type="button"
            className={`resposta ${pista === r.pergunta_id ? "pista" : ""}`}
            onClick={() => {
              if (pedindoPista) julgar("maquina", r.pergunta_id);
              else setPista(pista === r.pergunta_id ? null : r.pergunta_id);
            }}
            disabled={enviando}
          >
            <div className="pergunta">{r.pergunta}</div>
            <div>{r.resposta || <span className="suave">(em branco)</span>}</div>
            {pista === r.pergunta_id && <div className="pequeno" style={{ color: "var(--maquina)", marginTop: 4 }}>🚩 pista</div>}
          </button>
        ))}
      </div>

      {erro && <p className="erro">{erro}</p>}
      <div className="barra-inferior">
        {pedindoPista ? (
          <div className="linha" style={{ flexWrap: "nowrap" }}>
            <button className="botao secundario cheio" disabled={enviando} onClick={() => setPedindoPista(false)}>
              Voltar
            </button>
            <button className="botao maquina cheio" disabled={enviando} onClick={() => julgar("maquina", null)}>
              Máquina, sem pista
            </button>
          </div>
        ) : (
          <div className="linha" style={{ flexWrap: "nowrap" }}>
            <button className="botao humano cheio" disabled={enviando} onClick={() => julgar("humano")}>
              🧑 Humano
            </button>
            <button className="botao maquina cheio" disabled={enviando} onClick={() => julgar("maquina")}>
              🤖 Máquina
            </button>
          </div>
        )}
      </div>
      {indice !== null && (
        <button className="botao secundario" onClick={() => setIndice(null)}>
          Voltar
        </button>
      )}
    </div>
  );
}

function ListaDeCartoes({ visao, aoEscolher }: { visao: PropsFase["visao"]; aoEscolher: (i: number) => void }) {
  return (
    <div className="cartao">
      <p className="suave pequeno">Mudou de ideia? Toque num cartão para rever.</p>
      <div className="linha">
        {(visao.cartoes ?? []).map((c, i) => (
          <button key={c.id} className={`chip ${c.meu_veredito ?? ""}`} onClick={() => aoEscolher(i)}>
            #{c.rotulo} {c.meu_veredito === "maquina" ? "🤖" : "🧑"}
          </button>
        ))}
      </div>
    </div>
  );
}
