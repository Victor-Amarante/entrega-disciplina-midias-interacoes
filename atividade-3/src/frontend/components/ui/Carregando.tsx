export function Carregando({ texto = "Carregando…" }: { texto?: string }) {
  return <div className="carregando pulsando">{texto}</div>;
}
