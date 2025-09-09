# chroma_memory.py
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OpenAIEmbeddings
import os
from langchain.schema.document import Document

CHROMA_DIR = "chroma_db"

# Load Chroma vector DB (must match the directory used in rag_loader)
def load_chroma():
    try:
        embeddings = OpenAIEmbeddings(model="text-embedding-3-small", openai_api_key=os.getenv("OPENAI_API_KEY"))
        vectordb = Chroma(persist_directory=CHROMA_DIR, embedding_function=embeddings)
        return vectordb
    except Exception as e:
        print(f"Failed to load Chroma DB: {e}")
        return None

# Search for relevant chunks given a query
def query_memory(query: str, top_k=4) -> list[Document]:
    try:
        vectordb = load_chroma()
        if vectordb is None:
            return []
        results = vectordb.similarity_search(query, k=top_k)
        return results
    except Exception as e:
        print(f"Failed to query memory: {e}")
        return []
