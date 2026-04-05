import os
import sys

# Disable chromadb telemetry BEFORE any imports
os.environ["CHROMADB_TELEMETRY_DISABLED"] = "true"
os.environ["OTEL_SDK_DISABLED"] = "true"

# Prevent telemetry module from loading
import importlib.abc
import importlib.machinery

class BlockedImporter(importlib.abc.MetaPathFinder):
    def find_module(self, fullname, path=None):
        if "opentelemetry" in fullname or "chromadb.telemetry" in fullname:
            return importlib.machinery.NullImporter(fullname)
        return None

sys.meta_path.insert(0, BlockedImporter())

import streamlit as st
from rag import answer_query, format_sources

st.set_page_config(
    page_title="LennyPM",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for beautiful styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #FF4B4B;
        font-size: 3rem;
        font-weight: bold;
        margin-bottom: 1rem;
    }
    .subtitle {
        text-align: center;
        color: #FAFAFA;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
    .chat-container {
        max-width: 800px;
        margin: 0 auto;
    }
    .user-message {
        background-color: #262730;
        border-radius: 15px;
        padding: 15px;
        margin: 10px 0;
        border-left: 5px solid #FF4B4B;
    }
    .assistant-message {
        background-color: #1E1E1E;
        border-radius: 15px;
        padding: 15px;
        margin: 10px 0;
        border-left: 5px solid #00D4AA;
    }
    .sources-section {
        background-color: #262730;
        border-radius: 10px;
        padding: 15px;
        margin-top: 20px;
    }
    .stTextInput > div > div > input {
        background-color: #262730;
        color: #FAFAFA;
        border-radius: 10px;
    }
    .stButton > button {
        background-color: #FF4B4B;
        color: white;
        border-radius: 10px;
        border: none;
        padding: 10px 20px;
        font-weight: bold;
    }
    .stButton > button:hover {
        background-color: #E63946;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.title("🎙️ LennyPM")
    st.markdown("---")
    st.markdown("**About:**")
    st.markdown("Get product management advice from Lenny's Podcast transcripts using AI-powered retrieval.")
    st.markdown("---")
    st.markdown("**Features:**")
    st.markdown("- 📚 Full transcript corpus (313 episodes)")
    st.markdown("- 🔍 Semantic search with citations")
    st.markdown("- 🤖 GPT-4 powered answers")
    st.markdown("- 💰 Free embeddings (no API costs)")
    st.markdown("---")
    st.markdown("**Built with:**")
    st.markdown("- Streamlit")
    st.markdown("- LangChain")
    st.markdown("- SentenceTransformers")
    st.markdown("- ChromaDB")

# Main content
st.markdown('<h1 class="main-header">LennyPM</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Your AI PM advisor powered by Lenny\'s Podcast insights</p>', unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

if "sources" not in st.session_state:
    st.session_state.sources = []

# Chat interface
st.markdown('<div class="chat-container">', unsafe_allow_html=True)

# Display chat messages
for message in st.session_state.messages:
    if message["role"] == "user":
        st.markdown(f'<div class="user-message"><strong>You:</strong> {message["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="assistant-message"><strong>LennyPM:</strong> {message["content"]}</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Chat input
if prompt := st.chat_input("Ask a product management question..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Get AI response
    with st.spinner("🔍 Searching transcripts..."):
        result = answer_query(prompt)
    
    # Add assistant message
    st.session_state.messages.append({"role": "assistant", "content": result["answer"]})
    st.session_state.sources = result.get("sources", [])
    
    # Rerun to update the chat
    st.rerun()

# Sources section
if st.session_state.sources:
    st.markdown('<div class="sources-section">', unsafe_allow_html=True)
    st.subheader("📚 Sources")
    st.markdown(format_sources(st.session_state.sources))
    st.markdown('</div>', unsafe_allow_html=True)
