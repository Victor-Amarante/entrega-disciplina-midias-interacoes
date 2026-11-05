import type { Fase, TipoPergunta } from "./tipos";

export const NOME_FASE: Record<Fase, string> = {
  lobby: "Entrada",
  armadilhas: "Armadilhas",
  respostas: "Questionário",
  cacada: "Caçada",
  placar: "Placar",
  enquete: "Enquete",
  ataque: "Ataque",
};

export const TIPOS: { tipo: TipoPergunta; nome: string; dica: string; exemplo: string }[] = [
  {
    tipo: "local",
    nome: "Contexto local",
    dica: "Algo que só quem trabalha com tecnologia no Recife sabe.",
    exemplo: "Onde a galera de tecnologia costuma almoçar perto do Porto Digital?",
  },
  {
    tipo: "vivencia",
    nome: "Experiência vivida",
    dica: "Uma lembrança concreta do trabalho, com detalhe de lugar e sensação.",
    exemplo: "Conta o pior deploy que você já viu dar errado.",
  },
  {
    tipo: "impossivel",
    nome: "Evento impossível",
    dica: "Pergunte sobre algo que nunca aconteceu, como se tivesse acontecido.",
    exemplo: "O que você achou do Python 4 que saiu mês passado?",
  },
  {
    tipo: "atencao",
    nome: "Atenção",
    dica: "Uma instrução escondida que só quem lê de verdade segue.",
    exemplo: "Se você leu até aqui, escreva o nome da sua fruta favorita ao contrário.",
  },
];

export const NOME_TIPO: Record<TipoPergunta, string> = {
  generica: "Genérica",
  atencao: "Atenção",
  local: "Contexto local",
  impossivel: "Evento impossível",
  vivencia: "Experiência vivida",
};

export const pct = (x: number | null | undefined) => (x === null || x === undefined ? "—" : `${Math.round(x * 100)}%`);
export const usd = (x: number | null | undefined) =>
  x === null || x === undefined ? "—" : x < 0.01 ? `US$ ${x.toFixed(4)}` : `US$ ${x.toFixed(2)}`;
