# Paul Graham GPT

AI-powered search and chat for [Paul Graham's](https://twitter.com/paulg) [essays](http://www.paulgraham.com/articles.html).

All code & data used is 100% open-source.

## Dataset

The dataset is a CSV file containing all text & embeddings used.

Download it [here](https://drive.google.com/file/d/1BxcPw2mn0VYFucc62wlt9H0nQiOu38ki/view?usp=sharing).

I recommend getting familiar with fetching, cleaning, and storing data as outlined in the scraping and embedding scripts below, but feel free to skip those steps and just use the dataset.

## How It Works

Paul Graham GPT provides 2 things:

1. A search interface.
2. A chat interface.

### Search

Search was created with [OpenAI Embeddings](https://platform.openai.com/docs/guides/embeddings) (`text-embedding-ada-002`).

First, we loop over the essays and generate embeddings for each chunk of text.

Then in the app we take the user's search query, generate an embedding, and use the result to find the most similar passages from the book.

The comparison is done using cosine similarity across our database of vectors.

Our database is a Postgres database with the [pgvector](https://github.com/pgvector/pgvector) extension hosted on [Supabase](https://supabase.com/).

Results are ranked by similarity score and returned to the user.

### Chat

Chat builds on top of search. It uses search results to create a prompt that is fed into GPT-3.5-turbo.

This allows for a chat-like experience where the user can ask questions about the book and get answers.

## Running Locally

Here's a quick overview of how to run it locally.

### Requirements

1. Set up OpenAI

You'll need an OpenAI API key to generate embeddings.

2. Set up Supabase and create a database

Note: You don't have to use Supabase. Use whatever method you prefer to store your data. But I like Supabase and think it's easy to use.

There is a schema.sql file in the root of the repo that you can use to set up the database.

Run that in the SQL editor in Supabase as directed.

I recommend turning on Row Level Security and setting up a service role to use with the app.

### Repo Setup

3. Clone repo

```bash
git clone https://github.com/mckaywrigley/paul-graham-gpt.git
```

4. Install dependencies

```bash
npm i
```

5. Set up environment variables

Create a .env.local file in the root of the repo with the following variables:

```bash
OPENAI_API_KEY=

NEXT_PUBLIC_SUPABASE_URL=
SUPABASE_SERVICE_ROLE_KEY=
```

### Dataset

6. Run scraping script

```bash
npm run scrape
```

This scrapes all of the essays from Paul Graham's website and saves them to a json file.

7. Run embedding script

```bash
npm run embed
```

This reads the json file, generates embeddings for each chunk of text, and saves the results to your database.

There is a 200ms delay between each request to avoid rate limiting.

This process will take 20-30 minutes.

### App

8. Run app

```bash
npm run dev
```

## Credits

Thanks to [Paul Graham](https://twitter.com/paulg) for his writing.

I highly recommend you read his essays.

3 years ago they convinced me to learn to code, and it changed my life.

## Contact

If you have any questions, feel free to reach out to me on [Twitter](https://twitter.com/mckaywrigley)!

## Notes

I sacrificed composability for simplicity in the app.

Yes, you can make things more modular and reusable.

But I kept pretty much everything in the homepage component for the sake of simplicity.
