// Chamadas ao backend. Em produção o site e a API estão no mesmo endereço;
// em desenvolvimento a API roda na porta 8000 da mesma máquina.

function base(): string {
  if (process.env.NEXT_PUBLIC_API_URL) return process.env.NEXT_PUBLIC_API_URL;
  if (process.env.NODE_ENV === "development" && typeof window !== "undefined") {
    return `${window.location.protocol}//${window.location.hostname}:8000`;
  }
  return "";
}

export class ErroApi extends Error {
  constructor(public status: number, mensagem: string) {
    super(mensagem);
  }
}

export async function api<T>(
  caminho: string,
  opcoes: { metodo?: string; corpo?: unknown; cabecalhos?: Record<string, string> } = {},
): Promise<T> {
  const resposta = await fetch(`${base()}/api${caminho}`, {
    method: opcoes.metodo ?? (opcoes.corpo === undefined ? "GET" : "POST"),
    headers: { "Content-Type": "application/json", ...opcoes.cabecalhos },
    body: opcoes.corpo === undefined ? undefined : JSON.stringify(opcoes.corpo),
  });
  if (!resposta.ok) {
    let mensagem = "Algo deu errado. Tente de novo.";
    try {
      const dados = await resposta.json();
      if (typeof dados.detail === "string") mensagem = dados.detail;
    } catch {}
    throw new ErroApi(resposta.status, mensagem);
  }
  return resposta.json();
}

export const comoParticipante = (token: string) => ({ "X-Participante-Token": token });
export const comoHost = (token: string) => ({ "X-Host-Token": token });
