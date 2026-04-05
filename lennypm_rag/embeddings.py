from langchain_openai import OpenAIEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings

from config import EMBEDDING_PROVIDER, EMBEDDING_MODEL, OPENAI_EMBEDDING_MODEL, OPENAI_API_KEY


def get_embedding_function():
    if EMBEDDING_PROVIDER == "openai":
        if not OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is required for OpenAI embedding provider.")
        return OpenAIEmbeddings(model=OPENAI_EMBEDDING_MODEL)

    return HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
