export enum OpenAIModel {
  DAVINCI_TURBO = "gpt-3.5-turbo"
}

export type PGChunk = {
  source: string;
  content: string;
  embedding: number[];
};