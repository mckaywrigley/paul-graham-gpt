import { encode } from "gpt-3-encoder";
import fs from "fs";
import axios from "axios";
import { YouTubeTranscript } from "node-youtube-transcript";

const CHUNK_SIZE = 200;
const PLAYLIST_ID = "PLjH18-dhIa4oDDVFDoRwiYVQ0mWGgxasP";
const API_KEY = "TU_API_KEY";

const getVideoIds = async () => {
  const response = await axios.get(
    `https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&maxResults=50&playlistId=${PLAYLIST_ID}&key=${API_KEY}`
  );

  const videoIds = response.data.items.map((item) => item.snippet.resourceId.videoId);
  return videoIds;
};

const getTranscript = async (videoId) => {
  try {
    const transcript = await YouTubeTranscript.fetchTranscript(videoId, "en");

    const content = transcript
      .map((entry) => entry.text)
      .join(" ")
      .replace(/\s+/g, " ")
      .replace(/\.([a-zA-Z])/g, ". $1");

    return content;
  } catch (error) {
    console.error(`Error al obtener la transcripción del video ${videoId}:`, error);
    return "";
  }
};

const chunkTranscript = (transcript) => {
  const transcriptChunks = [];

  if (encode(transcript).length > CHUNK_SIZE) {
    const split = transcript.split(". ");
    let chunkText = "";

    for (let i = 0; i < split.length; i++) {
      const sentence = split[i];
      const sentenceTokenLength = encode(sentence);
      const chunkTextTokenLength = encode(chunkText).length;

      if (chunkTextTokenLength + sentenceTokenLength.length > CHUNK_SIZE) {
        transcriptChunks.push(chunkText);
        chunkText = "";
      }

      if (sentence[sentence.length - 1].match(/[a-z0-9]/i)) {
        chunkText += sentence + ". ";
      } else {
        chunkText += sentence + " ";
      }
    }

    transcriptChunks.push(chunkText.trim());
  } else {
    transcriptChunks.push(transcript.trim());
  }

  return transcriptChunks;
};

(async () => {
  const videoIds = await getVideoIds();
  const transcripts = [];

  for (const videoId of videoIds) {
    const transcript = await getTranscript(videoId);
    const chunkedTranscript = chunkTranscript(transcript);
    transcripts.push({
      videoId,
      transcript,
      chunks: chunkedTranscript,
    });
  }

  fs.writeFileSync("transcripts.json", JSON.stringify(transcripts));
})();
