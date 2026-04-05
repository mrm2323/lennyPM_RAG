import os
import sys
from pathlib import Path

# Disable chromadb telemetry BEFORE any imports of anything that uses it
os.environ["CHROMADB_TELEMETRY_DISABLED"] = "true"
os.environ["OTEL_SDK_DISABLED"] = "true"

# Block problematic telemetry modules
import importlib.abc
import importlib.machinery

class BlockedImporter(importlib.abc.MetaPathFinder):
    def find_module(self, fullname, path=None):
        if "opentelemetry" in fullname or "chromadb.telemetry" in fullname:
            return importlib.machinery.NullImporter(fullname)
        return None

sys.meta_path.insert(0, BlockedImporter())

from dotenv import load_dotenv

load_dotenv()

ROOT = Path(__file__).parent
TRANSCRIPTS_DIR = Path(os.getenv("TRANSCRIPTS_DIR", ROOT.parent / "Lenny's Podcast Transcripts Archive [public]"))
VECTORSTORE_DIR = Path(os.getenv("VECTORSTORE_DIR", ROOT / "vectorstore"))
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY", "")
PINECONE_ENV = os.getenv("PINECONE_ENV", "")
PINECONE_INDEX = os.getenv("PINECONE_INDEX", "lennypm")
COHERE_API_KEY = os.getenv("COHERE_API_KEY", "")
EMBEDDING_PROVIDER = os.getenv("EMBEDDING_PROVIDER", "sentence_transformer").lower()
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
OPENAI_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-large")
TRANSCRIPT_LIMIT = int(os.getenv("TRANSCRIPT_LIMIT", "0"))

USE_PINECONE = bool(PINECONE_API_KEY and PINECONE_ENV)
USE_COHERE = bool(COHERE_API_KEY)
