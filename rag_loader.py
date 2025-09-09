# rag_loader.py
import os
import glob
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OpenAIEmbeddings

CHROMA_DIR = "chroma_db"

# Step 1: Load PDF or .txt files from a directory
def load_documents(folder_path: str):
    all_files = glob.glob(f"{folder_path}/*")
    docs = []
    for file_path in all_files:
        if file_path.endswith(".pdf"):
            loader = PyPDFLoader(file_path)
        elif file_path.endswith(".txt"):
            loader = TextLoader(file_path)
        else:
            continue
        docs.extend(loader.load())
    return docs

# Step 2: Split into chunks
def split_documents(docs):
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    return splitter.split_documents(docs)

# Step 3: Embed and save to Chroma
def embed_and_store(docs, persist_directory=CHROMA_DIR):
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    vectordb = Chroma.from_documents(docs, embedding=embeddings, persist_directory=persist_directory)
    vectordb.persist()
    print(f"✅ Stored {len(docs)} chunks into Chroma.")

# Run this file as a script to ingest
if __name__ == "__main__":
    folder = "docs"  # put your PDFs or .txt files here
    print("📄 Loading documents...")
    raw_docs = load_documents(folder)
    print(f"Loaded {len(raw_docs)} raw documents.")
    chunks = split_documents(raw_docs)
    print(f"🧠 Split into {len(chunks)} chunks.")
    embed_and_store(chunks)
