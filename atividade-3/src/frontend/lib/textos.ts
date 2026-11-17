import type { Fase, TipoPergunta } from "./tipos";

export const NOME_FASE: Record<Fase, string> = {
  lobby: "Entrada",
  armadilhas: "Armadilhas",
  respostas: "Questionário",
  cacada: "Caçada",
  placar: "Placar",
};

// Os tipos que a turma pode escolher. A checagem de atenção ficou de fora: é mais fácil para a máquina do que
// para gente, e continua só como pergunta fixa, para comparação.
export const TIPOS: { tipo: TipoPergunta; nome: string; dica: string; exemplo: string }[] = [
  {
    tipo: "invertida",
    nome: "Só máquina sabe",
    dica: "O contrário: algo que gente não responde de cabeça e uma máquina responde na hora, certinho.",
    exemplo: "Sem calculadora e sem pesquisar: quanto é 347 × 28?",
  },
  {
    tipo: "sem_filtro",
    nome: "Sem filtro",
    dica: "Algo que uma pessoa responde sem cerimônia e um modelo educado evita ou amacia: opinião forte, reclamação, fofoca.",
    exemplo: "Qual linguagem você acha um lixo? Sem ficar em cima do muro.",
  },
  {
    tipo: "sala",
    nome: "Aqui na sala",
    dica: "Algo que só quem está nesta aula agora sabe.",
    exemplo: "Qual foi a primeira coisa que o apresentador falou hoje?",
  },
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
];

export const NOME_TIPO: Record<TipoPergunta, string> = {
  generica: "Genérica",
  atencao: "Atenção",
  local: "Contexto local",
  impossivel: "Evento impossível",
  vivencia: "Experiência vivida",
  invertida: "Só máquina sabe",
  sem_filtro: "Sem filtro",
  sala: "Aqui na sala",
};

export const pct = (x: number | null | undefined) => (x === null || x === undefined ? "—" : `${Math.round(x * 100)}%`);
export const usd = (x: number | null | undefined) =>
  x === null || x === undefined ? "—" : x < 0.01 ? `US$ ${x.toFixed(4)}` : `US$ ${x.toFixed(2)}`;
