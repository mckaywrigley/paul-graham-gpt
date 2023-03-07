import { PGChunk } from "@/types";
import { loadEnvConfig } from "@next/env";
import { createClient } from "@supabase/supabase-js";
import fs from "fs";
import { Configuration, OpenAIApi } from "openai";

loadEnvConfig("");

const generateEmbeddings = async (chunks: PGChunk[]) => {
  const configuration = new Configuration({ apiKey: process.env.OPENAI_API_KEY });
  const openai = new OpenAIApi(configuration);

  const supabase = createClient(process.env.NEXT_PUBLIC_SUPABASE_URL!, process.env.SUPABASE_SERVICE_ROLE_KEY!);

  for (let j = 0; j < chunks.length; j++) {
    const chunk = chunks[j];

    const { source, content } = chunk;

    const embeddingResponse = await openai.createEmbedding({
      model: "text-embedding-ada-002",
      input: content
    });

    const [{ embedding }] = embeddingResponse.data.data;

    const { data, error } = await supabase
      .from("pg")
      .insert({
        source,
        content,
        embedding
      })
      .select("*");

    if (error) {
      console.log("error", error);
    } else {
      console.log("saved", j);
    }

    await new Promise((resolve) => setTimeout(resolve, 200));
  }
};

(async () => {
  const book: PGChunk[] = JSON.parse(fs.readFileSync("new_scraper/pg.json", "utf8"));

  await generateEmbeddings(book);
})();
