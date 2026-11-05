"use client";

import { useSearchParams } from "next/navigation";
import { Suspense } from "react";
import { Carregando } from "@/components/ui/Carregando";
import { Painel } from "@/components/painel/Painel";

function Conteudo() {
  const codigo = (useSearchParams().get("c") ?? "").toUpperCase();
  if (!codigo) return <main className="painel">Falta o código da sala no link.</main>;
  return <Painel codigo={codigo} />;
}

export default function Pagina() {
  return (
    <Suspense fallback={<Carregando />}>
      <Conteudo />
    </Suspense>
  );
}
