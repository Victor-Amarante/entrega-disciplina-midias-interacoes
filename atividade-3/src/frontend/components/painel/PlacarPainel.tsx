"use client";

import { pct, usd } from "@/lib/textos";
import type { CartaoRevelado, Placar, VereditoAuditado } from "@/lib/tipos";
import type { PropsPainel } from "./props";

export function PlacarPainel({ painel }: PropsPainel) {
  const p = painel.placar;
  if (!p) return null;
  if (p.julgamentos === 0) return <p className="suave">Ninguém deu veredito ainda.</p>;

  return (
    <div className="coluna" style={{ gap: 20 }}>
      {p.leituras.length > 0 && (
        <div className="cartao">
          <h3>O que o placar diz</h3>
          <ul className="leituras">
            {p.leituras.map((l, i) => (
              <li key={i}>{l}</li>
            ))}
          </ul>
        </div>
      )}

      <div className="grade" style={{ alignItems: "start" }}>
        <Matriz p={p} />
        <div className="coluna">
          <Numero
            valor={pct(p.taxa_acerto)}
            rotulo="de acerto da turma"
            detalhe={`${p.acertos} de ${p.julgamentos} vereditos certos. Sem olhar as respostas, daria ${pct(p.acerto_sem_olhar)}.`}
          />
          <div className="grade">
            <Numero
              valor={pct(p.taxa_deteccao)}
              rotulo="dos agentes foram pegos"
              detalhe={`${p.matriz.agentes_pegos} de ${p.n_julgamentos_agentes} vereditos. Quanto maior, melhor.`}
              cor="var(--maquina)"
              pequeno
            />
            <Numero
              valor={pct(p.taxa_falsa_acusacao)}
              rotulo="dos humanos foram acusados"
              detalhe={`${p.matriz.humanos_acusados} de ${p.n_julgamentos_humanos} vereditos. Quanto menor, melhor.`}
              cor="var(--perigo)"
              pequeno
            />
          </div>
        </div>
      </div>

      <div className="grade">
        <Numero
          valor={usd(p.custo_medio_agente_usd)}
          rotulo="custo médio de um respondente sintético"
          detalhe="o questionário inteiro, ao preço de API de hoje"
          pequeno
        />
      </div>

      <Armadilhas p={p} />

      <div className="grade" style={{ alignItems: "start" }}>
        {p.agente_mais_convincente && (
          <Revelado titulo="O agente mais convincente" cartao={p.agente_mais_convincente} cor="var(--maquina)" />
        )}
        {p.humano_mais_suspeito && (
          <Revelado titulo="O humano mais acusado de ser máquina" cartao={p.humano_mais_suspeito} cor="var(--humano)" />
        )}
      </div>

      <Auditoria p={p} />

      <Acaso p={p} />
    </div>
  );
}

function Acaso({ p }: { p: Placar }) {
  if (p.taxa_acerto === null || p.acerto_sem_olhar === null) return null;
  const maioria = p.n_julgamentos_agentes >= p.n_julgamentos_humanos ? "máquina" : "humano";
  const pontos = Math.round((p.taxa_acerto - p.acerto_sem_olhar) * 100);
  const comparacao =
    Math.abs(pontos) < 10
      ? "praticamente o mesmo que não olhar: os agentes se disfarçaram bem."
      : pontos > 0
        ? `${pontos} pontos acima: a turma conseguiu reconhecer as máquinas.`
        : `${-pontos} pontos abaixo: ler as respostas atrapalhou mais do que ajudou.`;
  return (
    <div className="cartao">
      <h3>Como ler o acerto</h3>
      <p>
        Sem ler nenhuma resposta, só dizendo “{maioria}” para todos os cartões, daria{" "}
        <strong>{pct(p.acerto_sem_olhar)}</strong> de acerto. Essa é a régua do acaso: a turma só mostra que sabe
        separar gente de máquina se passar dela.
      </p>
      <ul className="leituras">
        <li>Perto da régua: a turma não conseguiu separar. Os agentes venceram.</li>
        <li>Bem acima da régua: a turma reconhece as máquinas.</li>
      </ul>
      <p style={{ marginBottom: 0 }}>
        Nesta sala: <strong>{pct(p.taxa_acerto)}</strong> de acerto, {comparacao}
      </p>
    </div>
  );
}

function Matriz({ p }: { p: Placar }) {
  const m = p.matriz;
  return (
    <div className="cartao">
      <h3>Onde caiu cada veredito</h3>
      <p className="suave pequeno">
        Cada cartão julgado entra numa destas caixas. Nas marcadas com ✓ a turma acertou; nas com ✗, errou.
      </p>
      <div className="matriz">
        <span />
        <span className="matriz-cabeca">disseram 🤖 máquina</span>
        <span className="matriz-cabeca">disseram 🧑 humano</span>
        <span className="matriz-cabeca">era agente</span>
        <Caixa n={m.agentes_pegos} rotulo="agentes pegos" certo />
        <Caixa n={m.agentes_passaram} rotulo="agentes que passaram por gente" />
        <span className="matriz-cabeca">era humano</span>
        <Caixa n={m.humanos_acusados} rotulo="humanos acusados de máquina" />
        <Caixa n={m.humanos_reconhecidos} rotulo="humanos reconhecidos" certo />
      </div>
    </div>
  );
}

function Caixa({ n, rotulo, certo }: { n: number; rotulo: string; certo?: boolean }) {
  return (
    <div className={`caixa ${certo ? "certo" : "errado"}`}>
      <strong>{n}</strong>
      <span className="pequeno">
        {certo ? "✓" : "✗"} {rotulo}
      </span>
    </div>
  );
}

function leituraArmadilha(pegou: number, acusou: number): string {
  if (!pegou && !acusou) return "ninguém apontou";
  if (pegou > acusou) return "boa armadilha";
  if (acusou > pegou) return "confundiu";
  return "empate";
}

function Armadilhas({ p }: { p: Placar }) {
  return (
    <div className="cartao">
      <h3>Qual pergunta entregou a máquina?</h3>
      <p className="suave pequeno">
        Quem disse “máquina” marcou a resposta que deu a pista. <em>Pegou agente</em> conta as vezes em que a pista
        estava certa; <em>acusou humano</em>, as vezes em que ela levou a acusar uma pessoa. Uma boa armadilha pega
        agentes sem acusar humanos.
      </p>
      <div className="rolagem">
        <table className="tabela">
          <thead>
            <tr>
              <th></th>
              <th>Pergunta</th>
              <th>Tipo</th>
              <th>Pegou agente</th>
              <th>Acusou humano</th>
              <th>Leitura</th>
            </tr>
          </thead>
          <tbody>
            {p.armadilhas.map((a) => (
              <tr key={a.id}>
                <td className="suave">P{a.numero}</td>
                <td>
                  {a.texto}
                  <div className="suave pequeno">{a.autor}</div>
                </td>
                <td><span className="chip">{a.tipo_rotulo}</span></td>
                <td style={{ color: "var(--maquina)", fontWeight: 700 }}>{a.pegou_agentes}</td>
                <td style={{ color: "var(--perigo)", fontWeight: 700 }}>{a.acusou_humanos}</td>
                <td className="pequeno">{leituraArmadilha(a.pegou_agentes, a.acusou_humanos)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

function Auditoria({ p }: { p: Placar }) {
  const { cartoes, jogadores } = p.auditoria;
  const nAgentes = cartoes.filter((c) => c.verdade === "maquina").length;
  return (
    <div className="cartao">
      <h3>Todos os vereditos</h3>
      <p className="suave pequeno">
        Cada linha é um jogador; cada coluna, um cartão. 🤖 = disse máquina, 🧑 = disse humano. Verde acertou, vermelho
        errou. P3 é a pergunta marcada como pista. Vazio: o cartão não caiu para essa pessoa; “·”: caiu, mas ficou sem
        veredito.
      </p>
      <div className="rolagem">
        <table className="tabela auditoria">
          <thead>
            <tr>
              <th colSpan={2}></th>
              {nAgentes > 0 && (
                <th colSpan={nAgentes} style={{ color: "var(--maquina)" }}>
                  🤖 eram agentes
                </th>
              )}
              {cartoes.length > nAgentes && (
                <th colSpan={cartoes.length - nAgentes} style={{ color: "var(--humano)" }}>
                  🧑 eram humanos
                </th>
              )}
            </tr>
            <tr>
              <th>Jogador</th>
              <th>Acertos</th>
              {cartoes.map((c) => (
                <th key={c.id} title={c.persona ? c.persona.nome : "humano"}>
                  #{c.rotulo}
                  <div>
                    <span className={`chip ${c.verdade}`}>
                      {c.verdade === "maquina" ? "🤖" : "🧑"}
                    </span>
                  </div>
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {jogadores.map((j, i) => (
              <tr key={j.apelido + i}>
                <td>{j.apelido}</td>
                <td>
                  <strong>{j.acertos}/{j.total}</strong>
                </td>
                {cartoes.map((c) => (
                  <Celula key={c.id} recebeu={j.cartoes.includes(c.id)} v={j.vereditos[c.id]} />
                ))}
              </tr>
            ))}
          </tbody>
          <tfoot>
            <tr>
              <td colSpan={2}>disseram máquina</td>
              {cartoes.map((c) => (
                <td key={c.id}>
                  {c.votos_maquina}/{c.votos}
                </td>
              ))}
            </tr>
          </tfoot>
        </table>
      </div>
      <details style={{ marginTop: 16 }}>
        <summary>Ver as respostas de cada cartão</summary>
        <div className="grade" style={{ alignItems: "start", marginTop: 12 }}>
          {cartoes.map((c) => (
            <Revelado
              key={c.id}
              titulo={c.verdade === "maquina" ? "🤖 Agente" : "🧑 Humano"}
              cartao={c}
              cor={c.verdade === "maquina" ? "var(--maquina)" : "var(--humano)"}
            />
          ))}
        </div>
      </details>
    </div>
  );
}

function Celula({ recebeu, v }: { recebeu: boolean; v?: VereditoAuditado }) {
  if (!recebeu) return <td />;
  if (!v) return <td className="suave">·</td>;
  return (
    <td className={`celula ${v.acertou ? "certo" : "errado"}`}>
      {v.veredito === "maquina" ? "🤖" : "🧑"}
      {v.pista && <span className="pequeno"> P{v.pista}</span>}
    </td>
  );
}

function Numero({
  valor,
  rotulo,
  detalhe,
  cor,
  pequeno,
}: {
  valor: string;
  rotulo: string;
  detalhe?: string;
  cor?: string;
  pequeno?: boolean;
}) {
  return (
    <div className="cartao">
      <div className="numero-grande" style={{ color: cor, fontSize: pequeno ? "2.2rem" : undefined }}>{valor}</div>
      <div className="rotulo-numero">{rotulo}</div>
      {detalhe && <div className="suave pequeno" style={{ marginTop: 4 }}>{detalhe}</div>}
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
        </p>
      )}
      {cartao.respostas.map((r, i) => (
        <div key={i} className="resposta" style={{ cursor: "default" }}>
          <div className="pergunta">P{i + 1} · {r.pergunta}</div>
          <div>{r.resposta}</div>
        </div>
      ))}
    </div>
  );
}
