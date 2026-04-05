from pathlib import Path
from typing import List
import shutil

from langchain_core.documents import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma

from config import TRANSCRIPTS_DIR, VECTORSTORE_DIR, TRANSCRIPT_LIMIT
from embeddings import get_embedding_function
from utils import clean_transcript_text, parse_source_metadata


def load_transcripts(transcripts_dir: Path) -> List[Document]:
    documents: List[Document] = []
    transcript_paths = sorted(transcripts_dir.glob("*.txt"))
    if TRANSCRIPT_LIMIT > 0:
        transcript_paths = transcript_paths[:TRANSCRIPT_LIMIT]

    for transcript_path in transcript_paths:
        raw_text = transcript_path.read_text(errors="ignore")
        cleaned = clean_transcript_text(raw_text)
        metadata = parse_source_metadata(transcript_path)
        if not cleaned:
            continue
        if len(cleaned) < 100:
            continue
        documents.append(Document(page_content=cleaned, metadata=metadata))
    return documents


def chunk_documents(documents: List[Document]) -> List[Document]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100,
        separators=["\n\n", "\n", ". ", " "]
    )
    chunks: List[Document] = []
    for doc in documents:
        split_texts = splitter.split_text(doc.page_content)
        for i, chunk_text in enumerate(split_texts):
            if len(chunk_text.strip()) < 50:
                continue
            chunk_metadata = dict(doc.metadata)
            chunk_metadata["chunk_index"] = i
            chunk_metadata["chunk_length"] = len(chunk_text)
            chunks.append(Document(page_content=chunk_text.strip(), metadata=chunk_metadata))
    return chunks


def build_vectorstore(documents: List[Document]):
    embeddings = get_embedding_function()

    if VECTORSTORE_DIR.exists():
        shutil.rmtree(VECTORSTORE_DIR)
    VECTORSTORE_DIR.mkdir(parents=True, exist_ok=True)

    vectorstore = Chroma.from_documents(
        documents,
        embeddings,
        persist_directory=str(VECTORSTORE_DIR),
        collection_name="lennypm",
    )
    return vectorstore


def main() -> None:
    print(f"Loading transcripts from {TRANSCRIPTS_DIR}")
    if not TRANSCRIPTS_DIR.exists():
        raise FileNotFoundError(f"Transcripts directory not found: {TRANSCRIPTS_DIR}")

    docs = load_transcripts(TRANSCRIPTS_DIR)
    print(f"Loaded {len(docs)} transcript documents.")
    chunks = chunk_documents(docs)
    print(f"Built {len(chunks)} chunks.")
    build_vectorstore(chunks)
    print(f"Vectorstore persisted to {VECTORSTORE_DIR}")


if __name__ == "__main__":
    main()
