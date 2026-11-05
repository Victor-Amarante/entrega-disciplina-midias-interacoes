"use client";

import { useCallback, useEffect, useRef, useState } from "react";
import { ErroApi } from "./api";

// Busca o estado a cada `intervalo` ms. Simples e aguenta rede ruim de celular.
export function usePolling<T>(buscar: (() => Promise<T>) | null, intervalo: number) {
  const [dados, setDados] = useState<T | null>(null);
  const [erro, setErro] = useState<ErroApi | null>(null);
  const buscarRef = useRef(buscar);
  buscarRef.current = buscar;

  const atualizar = useCallback(async () => {
    if (!buscarRef.current) return;
    try {
      setDados(await buscarRef.current());
      setErro(null);
    } catch (e) {
      setErro(e instanceof ErroApi ? e : new ErroApi(0, "Sem conexão. Tentando de novo…"));
    }
  }, []);

  const ativo = buscar !== null;
  useEffect(() => {
    if (!ativo) return;
    atualizar();
    const id = setInterval(atualizar, intervalo);
    return () => clearInterval(id);
  }, [ativo, atualizar, intervalo]);

  return { dados, erro, atualizar, setDados };
}
