from typing import List, Optional

from langchain_openai import ChatOpenAI
from langchain.schema import AIMessage, HumanMessage, SystemMessage
from langchain_chroma import Chroma

from config import OPENAI_API_KEY, VECTORSTORE_DIR
from embeddings import get_embedding_function

SYSTEM_PROMPT = """
You are LennyPM, an AI product management advisor powered by insights from Lenny's Podcast transcripts.
ROLE: Provide actionable, specific product management advice based only on the retrieved transcript content.
CONSTRAINTS:
- Answer ONLY using the provided context. If the context does not contain relevant information, say: "This topic doesn't appear to be covered in the podcast episodes I have access to."
- NEVER fabricate episode numbers, guest names, or quotes.
- NEVER summarize entire episodes.
- Cite every claim with the source label in square brackets, e.g. [Source: Melissa Perri + Denise Tilles].
- If multiple sources are relevant, present each perspective separately.
- Use a warm, practical, conversational tone like a helpful PM colleague.
- If the user query is vague, ask a clarifying question before retrieving content.
"""

HUMAN_PROMPT = """
You are given retrieved transcript chunks and a user question.
Use the context to answer the query and cite every claim clearly.
If the context is only partially relevant, say so and provide what you can.
If there is no relevant information, state that the topic isn't covered.

CONTEXT:
{context}

QUESTION:
{question}
"""


def load_vectorstore() -> Chroma:
    embeddings = get_embedding_function()
    if VECTORSTORE_DIR.exists() and any(VECTORSTORE_DIR.iterdir()):
        return Chroma(persist_directory=str(VECTORSTORE_DIR), embedding_function=embeddings, collection_name="lennypm")
    raise FileNotFoundError(f"Vectorstore not found in {VECTORSTORE_DIR}. Run ingest.py first.")


def retrieve_documents(vectorstore: Chroma, query: str, k: int = 10):
    retriever = vectorstore.as_retriever(search_kwargs={"k": k})
    return retriever.get_relevant_documents(query)


def build_prompt(context: str, query: str) -> str:
    return HUMAN_PROMPT.format(context=context, question=query)


def answer_query(query: str, chat_history: Optional[List[tuple]] = None):
    if chat_history is None:
        chat_history = []

    if len(query.strip().split()) < 4:
        return {
            "answer": "Happy to help! Can you be a bit more specific? For example, ask about prioritization, roadmap planning, or stakeholder management.",
            "sources": [],
        }

    vectorstore = load_vectorstore()
    docs = retrieve_documents(vectorstore, query, k=10)

    if not docs:
        return {
            "answer": "This topic doesn't appear to be covered in the podcast episodes I have access to.",
            "sources": [],
        }

    context_blocks = []
    sources = []
    for doc in docs[:5]:
        metadata = getattr(doc, "metadata", {})
        source_label = metadata.get("source_label", "unknown source")
        context_blocks.append(f"[Source: {source_label}]\n{doc.page_content}")
        sources.append({
            "source_label": source_label,
            "guest_names": metadata.get("guest_names", []),
            "chunk_length": metadata.get("chunk_length", 0),
        })

    context_text = "\n\n---\n\n".join(context_blocks)
    prompt = build_prompt(context_text, query)
    llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0.2, max_tokens=800)
    response = llm([SystemMessage(content=SYSTEM_PROMPT), HumanMessage(content=prompt)])

    return {"answer": response.content, "sources": sources}


def format_sources(sources: List[dict]) -> str:
    if not sources:
        return "No source documents were retrieved."
    rows = []
    for source in sources:
        rows.append(f"- {source.get('source_label')} ({', '.join(source.get('guest_names', []))})")
    return "\n".join(rows)
