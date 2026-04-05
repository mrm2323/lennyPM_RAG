# LennyPM RAG Prototype

A retrieval-augmented generation system for Lenny's Podcast transcripts.

## Features

- Ingests transcript `.txt` files from `Lenny's Podcast Transcripts Archive [public]`
- Cleans and chunks episode transcripts
- Builds local Chroma vector store for semantic retrieval
- Uses free local SentenceTransformer embeddings for vectorization
- Uses OpenAI `GPT-4o-mini` for answer generation
- Streamlit UI for chat-style queries with citations

## Setup

1. Create a Python virtual environment and activate it:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Set environment variables in `.env`:

```bash
OPENAI_API_KEY=your-openai-key
TRANSCRIPTS_DIR="/Users/mehulmitkari/Documents/AI PROJECTS/Lenny's Podcast Transcripts Archive [public]"
VECTORSTORE_DIR="/Users/mehulmitkari/Documents/AI PROJECTS/lennypm_rag/vectorstore"
EMBEDDING_PROVIDER=sentence_transformer
EMBEDDING_MODEL=all-MiniLM-L6-v2
```

Optional:

```bash
PINECONE_API_KEY=your-pinecone-key
PINECONE_ENV=us-east-1
PINECONE_INDEX=lennypm
COHERE_API_KEY=your-cohere-api-key
```
By default, the prototype now uses a free local SentenceTransformer embedding model and a local Chroma vector store. This means full transcript ingestion can be done without embedding API cost.

## Ingest transcripts

```bash
python lennypm_rag/ingest.py
```

Note: This now processes the full transcript dataset. For faster development runs, set `TRANSCRIPT_LIMIT=10` in `.env`.

## Run Streamlit app

```bash
streamlit run lennypm_rag/app.py
```

## Test CLI query

```bash
python lennypm_rag/query.py
```

## Current Status

- ✅ Basic RAG pipeline implemented
- ✅ Free local SentenceTransformer embeddings configured
- ✅ Local Chroma vectorstore built from the full transcript corpus (313 transcripts)
- ✅ OpenAI GPT-4o-mini generation working
- ✅ Streamlit UI ready for chat queries
- ✅ Citations and source metadata included
- ⚠️ OpenAI API key is still required for answer generation
- ⚠️ LangChain deprecation warnings may appear with current dependency versions

## Run Streamlit app

```bash
streamlit run lennypm_rag/app.py
```

## Query from the command line

```bash
python lennypm_rag/query.py
```

## Notes

- The dataset contains transcript files without explicit episode numbers, so citations use the transcript source label.
- The app supports local Chroma storage by default and optionally Pinecone if configured.
