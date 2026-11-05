"use client";

import { pct, usd } from "@/lib/textos";
import type { CartaoRevelado } from "@/lib/tipos";
import type { PropsPainel } from "./props";

export function PlacarPainel({ painel }: PropsPainel) {
  const p = painel.placar;
  if (!p) return null;
  if (p.julgamentos === 0) return <p className="suave">Ninguém deu veredito ainda.</p>;

  return (
    <div className="coluna" style={{ gap: 20 }}>
      <div className="grade">
        <Numero valor={pct(p.taxa_acerto)} rotulo="de acerto da turma (o acaso dá 50%)" />
        <Numero valor={pct(p.taxa_deteccao)} rotulo={`dos vereditos sobre agentes disseram "máquina"`} cor="var(--maquina)" />
        <Numero valor={pct(p.taxa_falsa_acusacao)} rotulo="dos vereditos sobre humanos os acusaram de máquina" cor="var(--perigo)" />
      </div>

      <div className="grade">
        <Numero valor={pct(p.deteccao_sem_busca)} rotulo="detecção dos agentes sem busca" pequeno />
        <Numero valor={pct(p.deteccao_com_busca)} rotulo="detecção dos agentes com busca na web 🔎" pequeno />
        <Numero valor={usd(p.custo_medio_agente_usd)} rotulo="custo médio de um respondente sintético" pequeno />
      </div>

      <div className="cartao">
        <h3>Qual armadilha pegou máquina?</h3>
        <p className="suave pequeno">
          Conta quantas vezes a resposta àquela pergunta foi marcada como pista num veredito de “máquina”, separando
          quando o respondente era mesmo um agente e quando era um humano acusado.
        </p>
        <table className="tabela">
          <thead>
            <tr>
              <th>Pergunta</th>
              <th>Tipo</th>
              <th>Pegou agente</th>
              <th>Acusou humano</th>
            </tr>
          </thead>
          <tbody>
            {p.armadilhas.map((a) => (
              <tr key={a.id}>
                <td>
                  {a.texto}
                  <div className="suave pequeno">{a.autor}</div>
                </td>
                <td><span className="chip">{a.tipo_rotulo}</span></td>
                <td style={{ color: "var(--maquina)", fontWeight: 700 }}>{a.pegou_agentes}</td>
                <td style={{ color: "var(--perigo)", fontWeight: 700 }}>{a.acusou_humanos}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <div className="grade" style={{ alignItems: "start" }}>
        {p.agente_mais_convincente && (
          <Revelado titulo="O agente mais convincente" cartao={p.agente_mais_convincente} cor="var(--maquina)" />
        )}
        {p.humano_mais_suspeito && (
          <Revelado titulo="O humano mais acusado de ser máquina" cartao={p.humano_mais_suspeito} cor="var(--humano)" />
        )}
        {p.detetives.length > 0 && (
          <div className="cartao">
            <h3>Melhores detetives</h3>
            {p.detetives.map((d, i) => (
              <div key={d.apelido + i} className="linha" style={{ padding: "6px 0" }}>
                <span>{i + 1}. {d.apelido}</span>
                <span className="espaco" />
                <strong>{d.acertos}/{d.total}</strong>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

function Numero({ valor, rotulo, cor, pequeno }: { valor: string; rotulo: string; cor?: string; pequeno?: boolean }) {
  return (
    <div className="cartao">
      <div className="numero-grande" style={{ color: cor, fontSize: pequeno ? "2.2rem" : undefined }}>{valor}</div>
      <div className="rotulo-numero">{rotulo}</div>
    </div>
  );
}

function Revelado({ titulo, cartao, cor }: { titulo: string; cartao: CartaoRevelado; cor: string }) {
  return (
    <div className="cartao" style={{ borderColor: cor }}>
      <h3>{titulo}</h3>
      <p className="suave pequeno">
        Respondente #{cartao.rotulo} · {cartao.votos_maquina} de {cartao.votos} disseram “máquina”
      </p>
      {cartao.persona && (
        <p className="pequeno">
          <strong>{cartao.persona.nome}</strong>, {cartao.persona.resumo}
          {cartao.com_busca ? " · com busca 🔎" : ""}
        </p>
      )}
      {cartao.respostas.map((r, i) => (
        <div key={i} className="resposta" style={{ cursor: "default" }}>
          <div className="pergunta">{r.pergunta}</div>
          <div>{r.resposta}</div>
        </div>
      ))}
    </div>
  );
}
