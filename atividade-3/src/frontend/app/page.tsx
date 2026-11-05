"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { useState } from "react";

export default function Inicio() {
  const router = useRouter();
  const [codigo, setCodigo] = useState("");

  function entrar(e: React.FormEvent) {
    e.preventDefault();
    const c = codigo.trim().toUpperCase();
    if (c) router.push(`/sala/?c=${c}`);
  }

  return (
    <main className="celular coluna" style={{ justifyContent: "center" }}>
      <div>
        <div className="titulo-fase">CIN0055 · Tendências em Mídia e Interação</div>
        <h1 style={{ fontSize: "2rem" }}>Caça ao respondente sintético</h1>
        <p className="suave">
          Uma pesquisa online com gente e máquinas misturadas. Você escreve perguntas para pegar os bots,
          responde, e depois tenta descobrir quem é quem.
        </p>
      </div>

      <form className="cartao coluna" onSubmit={entrar}>
        <label htmlFor="codigo">Código da sala</label>
        <input
          id="codigo"
          value={codigo}
          onChange={(e) => setCodigo(e.target.value.toUpperCase())}
          placeholder="ABCD"
          maxLength={4}
          autoCapitalize="characters"
          autoComplete="off"
          style={{ fontSize: "1.6rem", letterSpacing: ".3em", textAlign: "center" }}
        />
        <button className="botao cheio" disabled={codigo.trim().length < 4}>
          Entrar
        </button>
      </form>

      <p className="suave pequeno centro">
        Vai apresentar? <Link href="/host/">Criar uma sala</Link>
      </p>
    </main>
  );
}
