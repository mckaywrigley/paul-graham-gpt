import { PGChunk, PGEssay, PGJSON } from "@/types";
import fs from "fs";
import path from "path";
import { encode } from "gpt-3-encoder";

const CHUNK_SIZE = 200;
const TRANSCRIPTIONS_DIR = "./scripts/data"; // Reemplaza esto con la ruta de tu carpeta de transcripciones

const getFilenames = async () => {
  return fs.readdirSync(TRANSCRIPTIONS_DIR).filter((file) => file.endsWith(".txt"));
};

const getTranscription = async (filename: string) => {
  const content = fs.readFileSync(path.join(TRANSCRIPTIONS_DIR, filename), "utf-8");

  let transcription: PGEssay = {
    title: filename.replace(".txt", ""),
    url: "",
    date: "",
    thanks: "",
    content,
    length: content.length,
    tokens: encode(content).length,
    chunks: [],
  };

  return transcription;
};

const chunkTranscription = async (transcription: PGEssay) => {
  const { title, url, date, thanks, content, ...chunklessSection } = transcription;

  let transcriptionTextChunks = [];

  if (encode(content).length > CHUNK_SIZE) {
    const split = content.split(". ");
    let chunkText = "";

    for (let i = 0; i < split.length; i++) {
      const sentence = split[i];
      const sentenceTokenLength = encode(sentence);
      const chunkTextTokenLength = encode(chunkText).length;

      if (chunkTextTokenLength + sentenceTokenLength.length > CHUNK_SIZE) {
        transcriptionTextChunks.push(chunkText);
        chunkText = "";
      }

      if (sentence[sentence.length - 1].match(/[a-z0-9]/i)) {
        chunkText += sentence + ". ";
      } else {
        chunkText += sentence + " ";
      }
    }

    transcriptionTextChunks.push(chunkText.trim());
  } else {
    transcriptionTextChunks.push(content.trim());
  }

  const transcriptionChunks = transcriptionTextChunks.map((text) => {
    const trimmedText = text.trim();

    const chunk: PGChunk = {
      essay_title: title,
      essay_url: url,
      essay_date: date,
      essay_thanks: thanks,
      content: trimmedText,
      content_length: trimmedText.length,
      content_tokens: encode(trimmedText).length,
      embedding: [],
    };

    return chunk;
  });

  if (transcriptionChunks.length > 1) {
    for (let i = 0; i < transcriptionChunks.length; i++) {
      const chunk = transcriptionChunks[i];
      const prevChunk = transcriptionChunks[i - 1];

      if (chunk.content_tokens < 100 && prevChunk) {
        prevChunk.content += " " + chunk.content;
        prevChunk.content_length += chunk.content_length;
        prevChunk.content_tokens += chunk.content_tokens;
        transcriptionChunks.splice(i, 1);
        i--;
      }
    }
  }

  const chunkedSection: PGEssay = {
    ...transcription,
    chunks: transcriptionChunks,
  };

  return chunkedSection;
};

(async () => {
  const filenames = await getFilenames();

  let transcriptions = [];

  for (let i = 0; i < filenames.length; i++) {
    const transcription = await getTranscription(filenames[i]);
    const chunkedTranscription = await chunkTranscription(transcription);
    transcriptions.push(chunkedTranscription);
  }

  const json: PGJSON = {
    current_date: "2023-03-01", // Actualiza esta fecha si es necesario
    author: "Nombre del autor", // Reemplaza esto con el nombre del autor
    url: "URL del canal", // Reemplaza esto con la URL del canal
    length: transcriptions.reduce((acc, transcription) => acc + transcription.length, 0),
    tokens: transcriptions.reduce((acc, transcription) => acc + transcription.tokens, 0),
    essays: transcriptions,
  };

  fs.writeFileSync("scripts/transcriptions.json", JSON.stringify(json));
})();