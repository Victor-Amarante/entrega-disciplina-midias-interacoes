import type { VisaoParticipante } from "@/lib/tipos";

export interface PropsFase {
  visao: VisaoParticipante;
  enviar: (caminho: string, corpo?: unknown, metodo?: string) => Promise<void>;
}
