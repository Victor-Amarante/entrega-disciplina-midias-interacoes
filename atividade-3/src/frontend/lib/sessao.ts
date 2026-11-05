// Tokens guardados no navegador, por sala, para recarregar a página sem perder o lugar.

function ler(chave: string): string | null {
  try {
    return localStorage.getItem(chave);
  } catch {
    return null;
  }
}

function gravar(chave: string, valor: string | null) {
  try {
    if (valor === null) localStorage.removeItem(chave);
    else localStorage.setItem(chave, valor);
  } catch {}
}

export const tokenParticipante = (codigo: string) => ler(`caca:p:${codigo}`);
export const guardarTokenParticipante = (codigo: string, token: string | null) => gravar(`caca:p:${codigo}`, token);
export const tokenHost = (codigo: string) => ler(`caca:h:${codigo}`);
export const guardarTokenHost = (codigo: string, token: string) => gravar(`caca:h:${codigo}`, token);
