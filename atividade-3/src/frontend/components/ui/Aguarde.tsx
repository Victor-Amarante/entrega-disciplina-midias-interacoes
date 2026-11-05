export function Aguarde({ titulo, texto }: { titulo: string; texto: string }) {
  return (
    <div className="cartao centro" style={{ padding: "40px 20px" }}>
      <h2>{titulo}</h2>
      <p className="suave pulsando" style={{ margin: 0 }}>{texto}</p>
    </div>
  );
}
