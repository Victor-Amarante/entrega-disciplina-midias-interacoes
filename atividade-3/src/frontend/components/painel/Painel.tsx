"use client";

import { useCallback, useEffect, useState } from "react";
import { api, comoHost } from "@/lib/api";
import { tokenHost } from "@/lib/sessao";
import { NOME_FASE } from "@/lib/textos";
import type { Fase, VisaoPainel } from "@/lib/tipos";
import { usePolling } from "@/lib/usePolling";
import { Carregando } from "@/components/ui/Carregando";
import { Entrada } from "./Entrada";
import { ArmadilhasPainel } from "./ArmadilhasPainel";
import { RespostasPainel } from "./RespostasPainel";
import { CacadaPainel } from "./CacadaPainel";
import { PlacarPainel } from "./PlacarPainel";
import { EnquetePainel } from "./EnquetePainel";
import { AtaquePainel } from "./AtaquePainel";

const AVISO_AO_ENTRAR: Partial<Record<Fase, string>> = {
  respostas: "Fechar as armadilhas? O questionário fica congelado e os agentes começam a responder.",
  cacada: "Fechar o questionário? Quem não enviou fica de fora da caçada.",
};

export function Painel({ codigo }: { codigo: string }) {
  const [token, setToken] = useState<string | null | undefined>(undefined);
  const [erroAcao, setErroAcao] = useState<string | null>(null);
  useEffect(() => setToken(tokenHost(codigo)), [codigo]);

  const buscar = useCallback(
    () => api<VisaoPainel>(`/salas/${codigo}/painel`, { cabecalhos: comoHost(token!) }),
    [codigo, token],
  );
  const { dados: painel, erro, setDados } = usePolling(token ? buscar : null, 1500);

  const acao = useCallback(
    async (caminho: string, corpo?: unknown, metodo?: string) => {
      setErroAcao(null);
      try {
        const novo = await api<VisaoPainel>(`/salas/${codigo}${caminho}`, { corpo, metodo, cabecalhos: comoHost(token!) });
        setDados(novo);
      } catch (e) {
        setErroAcao((e as Error).message);
      }
    },
    [codigo, token, setDados],
  );

  if (token === undefined) return <Carregando />;
  if (token === null)
    return (
      <main className="painel">
        <h2>Este navegador não abriu a sala {codigo}</h2>
        <p className="suave">O painel só funciona no navegador onde a sala foi criada.</p>
      </main>
    );
  if (!painel) return <Carregando texto={erro?.message ?? "Abrindo o painel…"} />;

  const i = painel.fases.indexOf(painel.fase);
  const proxima = painel.fases[i + 1];
  const anterior = painel.fases[i - 1];

  function irPara(fase: Fase) {
    const aviso = AVISO_AO_ENTRAR[fase];
    if (aviso && painel!.fases.indexOf(fase) > i && !window.confirm(aviso)) return;
    acao("/fase", { fase });
  }

  async function baixarDados() {
    try {
      const dados = await api<unknown>(`/salas/${codigo}/dados`, { cabecalhos: comoHost(token!) });
      const url = URL.createObjectURL(new Blob([JSON.stringify(dados, null, 2)], { type: "application/json" }));
      const link = Object.assign(document.createElement("a"), { href: url, download: `sala-${codigo}.json` });
      link.click();
      URL.revokeObjectURL(url);
    } catch (e) {
      setErroAcao((e as Error).message);
    }
  }

  const props = { painel, acao };
  return (
    <main className="painel">
      <header className="painel-topo">
        <div>
          <div className="titulo-fase" style={{ marginBottom: 0 }}>Caça ao respondente sintético</div>
          <div style={{ fontSize: "1.6rem", fontWeight: 800, letterSpacing: ".15em" }}>{painel.codigo}</div>
        </div>
        <nav className="passos" aria-label="Fases">
          {painel.fases.map((f, j) => (
            <button
              key={f}
              className={`passo ${f === painel.fase ? "atual" : j < i ? "feito" : ""}`}
              onClick={() => f !== painel.fase && irPara(f)}
            >
              {j + 1}. {NOME_FASE[f]}
            </button>
          ))}
        </nav>
        <span className="espaco" />
        <button className="botao secundario pequeno" onClick={baixarDados} title="Baixar tudo o que aconteceu na sala, em JSON">
          ⬇ Dados
        </button>
        {anterior && (
          <button className="botao secundario pequeno" onClick={() => irPara(anterior)}>
            ◀
          </button>
        )}
        {proxima && (
          <button className="botao" onClick={() => irPara(proxima)}>
            {NOME_FASE[proxima]} ▶
          </button>
        )}
      </header>

      {painel.simulado && (
        <p className="aviso">
          Modo simulado: o servidor está sem ANTHROPIC_API_KEY, e os agentes usam frases prontas. Serve para testar,
          não para o experimento.
        </p>
      )}
      {(erroAcao || erro) && <p className="erro">{erroAcao ?? erro?.message}</p>}

      {painel.fase === "lobby" && <Entrada {...props} />}
      {painel.fase === "armadilhas" && <ArmadilhasPainel {...props} />}
      {painel.fase === "respostas" && <RespostasPainel {...props} />}
      {painel.fase === "cacada" && <CacadaPainel {...props} />}
      {painel.fase === "placar" && <PlacarPainel {...props} />}
      {painel.fase === "enquete" && <EnquetePainel {...props} />}
      {painel.fase === "ataque" && <AtaquePainel {...props} />}
    </main>
  );
}
