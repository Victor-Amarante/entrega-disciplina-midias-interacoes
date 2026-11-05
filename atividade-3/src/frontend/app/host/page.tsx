"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { useState } from "react";
import { api } from "@/lib/api";
import { guardarTokenHost } from "@/lib/sessao";

export default function CriarSala() {
  const router = useRouter();
  const [nAgentes, setNAgentes] = useState(8);
  const [fracBusca, setFracBusca] = useState(50);
  const [maxPerguntas, setMaxPerguntas] = useState(6);
  const [erro, setErro] = useState<string | null>(null);
  const [criando, setCriando] = useState(false);

  async function criar(e: React.FormEvent) {
    e.preventDefault();
    setCriando(true);
    try {
      const r = await api<{ codigo: string; host_token: string }>("/salas", {
        corpo: { config: { n_agentes: nAgentes, frac_busca: fracBusca / 100, max_perguntas: maxPerguntas } },
      });
      guardarTokenHost(r.codigo, r.host_token);
      router.push(`/painel/?c=${r.codigo}`);
    } catch (e) {
      setErro((e as Error).message);
      setCriando(false);
    }
  }

  return (
    <main className="celular coluna">
      <div>
        <div className="titulo-fase">Apresentador</div>
        <h1>Criar uma sala</h1>
        <p className="suave">
          Abra o painel no projetor. A turma entra pelo QR code com o celular. Os valores padrão servem para uma
          turma de 20 a 40 pessoas.
        </p>
      </div>
      <form className="cartao coluna" onSubmit={criar}>
        <div>
          <label htmlFor="n">Agentes infiltrados: {nAgentes}</label>
          <input id="n" type="range" min={2} max={12} value={nAgentes} onChange={(e) => setNAgentes(+e.target.value)} />
        </div>
        <div>
          <label htmlFor="b">Com busca na web: {fracBusca}%</label>
          <input id="b" type="range" min={0} max={100} step={25} value={fracBusca} onChange={(e) => setFracBusca(+e.target.value)} />
          <p className="suave pequeno" style={{ margin: "4px 0 0" }}>
            Parte dos agentes pode pesquisar antes de responder, para testar as perguntas de contexto local.
          </p>
        </div>
        <div>
          <label htmlFor="q">Perguntas no questionário: {maxPerguntas}</label>
          <input id="q" type="range" min={3} max={10} value={maxPerguntas} onChange={(e) => setMaxPerguntas(+e.target.value)} />
          <p className="suave pequeno" style={{ margin: "4px 0 0" }}>
            Duas são fixas (uma genérica e uma checagem de atenção); o resto sai das armadilhas da turma.
          </p>
        </div>
        <button className="botao cheio" disabled={criando}>
          Criar sala e abrir o painel
        </button>
        {erro && <p className="erro">{erro}</p>}
      </form>
      <p className="suave pequeno centro">
        <Link href="/">Voltar</Link>
      </p>
    </main>
  );
}
