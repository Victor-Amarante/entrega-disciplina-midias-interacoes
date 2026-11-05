import type { VisaoPainel } from "@/lib/tipos";

export interface PropsPainel {
  painel: VisaoPainel;
  acao: (caminho: string, corpo?: unknown, metodo?: string) => Promise<void>;
}
