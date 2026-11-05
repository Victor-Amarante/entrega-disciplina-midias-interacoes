export function Progresso({ feito, total }: { feito: number; total: number }) {
  const largura = total ? Math.min(100, (feito / total) * 100) : 0;
  return (
    <div className="progresso" aria-label={`${feito} de ${total}`}>
      <div style={{ width: `${largura}%` }} />
    </div>
  );
}
