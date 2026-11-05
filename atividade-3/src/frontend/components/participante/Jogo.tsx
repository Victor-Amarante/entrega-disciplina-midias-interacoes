"use client";

import { useCallback, useEffect, useState } from "react";
import { api, comoParticipante } from "@/lib/api";
import { guardarTokenParticipante, tokenParticipante } from "@/lib/sessao";
import { NOME_FASE } from "@/lib/textos";
import type { VisaoParticipante } from "@/lib/tipos";
import { usePolling } from "@/lib/usePolling";
import { Aguarde } from "@/components/ui/Aguarde";
import { Carregando } from "@/components/ui/Carregando";
import { Entrar } from "./Entrar";
import { Armadilhas } from "./Armadilhas";
import { Questionario } from "./Questionario";
import { Cacada } from "./Cacada";
import { Resultado } from "./Resultado";
import { Votacao } from "./Votacao";

export function Jogo({ codigo }: { codigo: string }) {
  const [token, setToken] = useState<string | null | undefined>(undefined);

  useEffect(() => setToken(tokenParticipante(codigo)), [codigo]);

  const buscar = useCallback(
    () => api<VisaoParticipante>(`/salas/${codigo}/eu`, { cabecalhos: comoParticipante(token!) }),
    [codigo, token],
  );
  const { dados: visao, erro, atualizar } = usePolling(token ? buscar : null, 2000);

  // Token que o servidor não reconhece (sala recriada, por exemplo): pede o apelido de novo.
  useEffect(() => {
    if (erro?.status === 401) {
      guardarTokenParticipante(codigo, null);
      setToken(null);
    }
  }, [erro, codigo]);

  const enviar = useCallback(
    async (caminho: string, corpo?: unknown, metodo?: string) => {
      await api(`/salas/${codigo}${caminho}`, { corpo, metodo, cabecalhos: comoParticipante(token!) });
      await atualizar();
    },
    [codigo, token, atualizar],
  );

  if (token === undefined) return <Carregando />;
  if (token === null)
    return (
      <Entrar
        codigo={codigo}
        aoEntrar={(t) => {
          guardarTokenParticipante(codigo, t);
          setToken(t);
        }}
      />
    );
  if (!visao) {
    if (erro?.status === 404) return <main className="celular erro">Sala {codigo} não encontrada.</main>;
    return <Carregando texto={erro ? erro.message : "Entrando na sala…"} />;
  }

  const props = { visao, enviar };
  return (
    <main className="celular">
      <div className="linha suave pequeno" style={{ marginBottom: 16 }}>
        <span>Sala {visao.codigo}</span>
        <span className="espaco" />
        <span>{visao.apelido}</span>
      </div>
      <div className="titulo-fase">{NOME_FASE[visao.fase]}</div>
      {erro && <p className="aviso">{erro.message}</p>}
      {visao.fase === "lobby" && <Aguarde titulo="Você está dentro!" texto="Escute a apresentação. O jogo começa já já." />}
      {visao.fase === "armadilhas" && <Armadilhas {...props} />}
      {visao.fase === "respostas" && <Questionario {...props} />}
      {visao.fase === "cacada" && <Cacada {...props} />}
      {visao.fase === "placar" && <Resultado {...props} />}
      {(visao.fase === "enquete" || visao.fase === "ataque") && <Votacao {...props} />}
    </main>
  );
}
