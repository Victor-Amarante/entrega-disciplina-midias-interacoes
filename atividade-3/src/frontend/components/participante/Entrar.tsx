"use client";

import { useState } from "react";
import { api } from "@/lib/api";

export function Entrar({ codigo, aoEntrar }: { codigo: string; aoEntrar: (token: string) => void }) {
  const [apelido, setApelido] = useState("");
  const [erro, setErro] = useState<string | null>(null);
  const [enviando, setEnviando] = useState(false);

  async function entrar(e: React.FormEvent) {
    e.preventDefault();
    setEnviando(true);
    setErro(null);
    try {
      const r = await api<{ token: string }>(`/salas/${codigo}/entrar`, { corpo: { apelido: apelido.trim() } });
      aoEntrar(r.token);
    } catch (e) {
      setErro((e as Error).message);
      setEnviando(false);
    }
  }

  return (
    <main className="celular coluna" style={{ justifyContent: "center" }}>
      <div>
        <div className="titulo-fase">Sala {codigo}</div>
        <h1>Caça ao respondente sintético</h1>
        <p className="suave">
          Nesta pesquisa há gente da turma e agentes de IA fingindo ser desenvolvedores de software. Ninguém sabe quem é quem.
        </p>
      </div>
      <form className="cartao coluna" onSubmit={entrar}>
        <label htmlFor="apelido">Como quer ser chamado no placar?</label>
        <input
          id="apelido"
          value={apelido}
          onChange={(e) => setApelido(e.target.value)}
          placeholder="Um apelido"
          maxLength={24}
          autoFocus
        />
        <p className="suave pequeno" style={{ margin: 0 }}>
          Suas respostas aparecem anônimas para a turma. O apelido só aparece no ranking de detetives.
        </p>
        <button className="botao cheio" disabled={!apelido.trim() || enviando}>
          Entrar
        </button>
        {erro && <p className="erro">{erro}</p>}
      </form>
    </main>
  );
}
