"use client";

import { useSearchParams } from "next/navigation";
import { Suspense } from "react";
import { Carregando } from "@/components/ui/Carregando";
import { Jogo } from "@/components/participante/Jogo";

function Sala() {
  const codigo = (useSearchParams().get("c") ?? "").toUpperCase();
  if (!codigo) return <main className="celular">Falta o código da sala no link.</main>;
  return <Jogo codigo={codigo} />;
}

export default function Pagina() {
  return (
    <Suspense fallback={<Carregando />}>
      <Sala />
    </Suspense>
  );
}
