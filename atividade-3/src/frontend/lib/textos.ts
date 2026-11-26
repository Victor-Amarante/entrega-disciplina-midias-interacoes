import type { Fase, TipoPergunta } from "./tipos";

export const NOME_FASE: Record<Fase, string> = {
  lobby: "Entrada",
  armadilhas: "Armadilhas",
  respostas: "Questionário",
  cacada: "Caçada",
  placar: "Placar",
};

export const TIPOS: { tipo: TipoPergunta; nome: string; dica: string; exemplo: string }[] = [
  {
    tipo: "pegadinha",
    nome: "Pegadinha",
    dica: "Uma pergunta boba, que qualquer um sabe responder. A diferença está na atitude: gente costuma zoar ou responder torto de propósito.",
    exemplo: "Quantas letras “a” tem em “abacate”?",
  },
  {
    tipo: "sem_filtro",
    nome: "Sem filtro",
    dica: "Algo que uma pessoa responde sem cerimônia e um modelo educado evita ou amacia: opinião forte, reclamação, fofoca.",
    exemplo: "Qual linguagem você acha um lixo? Sem ficar em cima do muro.",
  },
  {
    tipo: "vivencia",
    nome: "Experiência vivida",
    dica: "Uma lembrança concreta do trabalho, com detalhe de lugar e sensação.",
    exemplo: "Conta o pior deploy que você já viu dar errado.",
  },
];

export const NOME_TIPO: Record<TipoPergunta, string> = {
  generica: "Genérica",
  atencao: "Atenção",
  local: "Contexto local",
  impossivel: "Evento impossível",
  vivencia: "Experiência vivida",
  invertida: "Só máquina sabe",
  sem_filtro: "Sem filtro",
  pegadinha: "Pegadinha",
  sala: "Aqui na sala",
};

export const pct = (x: number | null | undefined) => (x === null || x === undefined ? "—" : `${Math.round(x * 100)}%`);
export const usd = (x: number | null | undefined) =>
  x === null || x === undefined ? "—" : x < 0.01 ? `US$ ${x.toFixed(4)}` : `US$ ${x.toFixed(2)}`;
