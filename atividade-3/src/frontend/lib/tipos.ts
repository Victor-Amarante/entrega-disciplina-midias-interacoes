// Formas que o backend devolve (app/servicos/visoes.py).

export type Fase = "lobby" | "armadilhas" | "respostas" | "cacada" | "placar" | "enquete" | "ataque";
export type TipoPergunta = "generica" | "atencao" | "local" | "impossivel" | "vivencia";
export type Veredito = "humano" | "maquina";
export type Opcao = "a" | "b";

export interface Cartao {
  id: string;
  rotulo: string;
  respostas: { pergunta_id: string; pergunta: string; resposta: string }[];
  meu_veredito: Veredito | null;
  minha_pista: string | null;
  verdade?: Veredito;
  persona?: string;
  com_busca?: boolean;
}

export interface VisaoParticipante {
  codigo: string;
  fase: Fase;
  apelido: string;
  participantes: number;
  minhas_armadilhas?: { id: string; texto: string; tipo: TipoPergunta }[];
  limite_armadilhas?: number;
  armadilhas_encerradas?: boolean;
  perguntas?: { id: string; texto: string }[];
  minhas_respostas?: Record<string, string>;
  cartoes?: Cartao[];
  meu_resultado?: { acertos: number; total: number };
  enquete?: { pergunta: string; opcao_a: string; opcao_b: string; meu_voto: Opcao | null };
}

export interface PerguntaPainel {
  id: string;
  texto: string;
  tipo: TipoPergunta;
  autor: string | null;
  selecionada: boolean;
  fixa: boolean;
  no_questionario: boolean;
}

export interface AgentePainel {
  id: string;
  nome: string;
  com_busca: boolean;
  status: "pendente" | "pronto" | "erro";
  erro: string | null;
  segundos: number;
  custo_usd: number;
}

export interface CartaoRevelado {
  rotulo: string;
  votos_maquina: number;
  votos: number;
  persona: { nome: string; resumo: string } | null;
  com_busca: boolean;
  respostas: { pergunta: string; resposta: string }[];
}

export interface Placar {
  julgamentos: number;
  taxa_acerto: number | null;
  taxa_deteccao: number | null;
  taxa_falsa_acusacao: number | null;
  deteccao_com_busca: number | null;
  deteccao_sem_busca: number | null;
  n_julgamentos_agentes: number;
  n_julgamentos_humanos: number;
  armadilhas: {
    id: string;
    texto: string;
    tipo: TipoPergunta;
    tipo_rotulo: string;
    autor: string;
    pegou_agentes: number;
    acusou_humanos: number;
    saldo: number;
  }[];
  detetives: { apelido: string; acertos: number; total: number }[];
  agente_mais_convincente: CartaoRevelado | null;
  humano_mais_suspeito: CartaoRevelado | null;
  custo_medio_agente_usd: number | null;
}

export interface Ataque {
  votos_a: number;
  votos_b: number;
  alvo: Opcao;
  necessarios: number;
  taxa_deteccao: number | null;
  necessarios_com_defesa: number | null;
  humanos_barrados: number;
  custo_medio_agente_usd: number | null;
  custo_ataque_usd: number | null;
  status_sinteticos: "parado" | "gerando" | "pronto" | "erro";
  sinteticos: { opcao: Opcao; justificativa: string }[];
}

export interface VisaoPainel {
  codigo: string;
  fase: Fase;
  fases: Fase[];
  config: { n_agentes: number; frac_busca: number; max_perguntas: number; cards_por_juiz: number };
  simulado: boolean;
  modelo: string;
  participantes: { id: string; apelido: string }[];
  perguntas: PerguntaPainel[];
  questionario_fechado: boolean;
  respostas_humanas: number;
  agentes: AgentePainel[];
  cacada: { julgamentos: number; juizes: number; juizes_concluidos: number; cartoes_no_jogo: number };
  enquete: { pergunta: string; opcao_a: string; opcao_b: string; votos: number };
  placar?: Placar;
  ataque?: Ataque;
}
