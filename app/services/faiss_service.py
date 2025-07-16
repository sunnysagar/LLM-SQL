"""
    This file handles:

Converting documents into vector embeddings

Indexing them using FAISS

Searching for similar documents based on user query
"""

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# Load embedding model (MiniLM = small + fast)
model = SentenceTransformer('all-MiniLM-L6-v2')

# FAISS index for vector similarity search (384 = embedding size)
index = faiss.IndexFlatL2(384)

# Store original documents in list for reference
documents = []

def load_documents(docs: list[str]):
    """
    Converts documents into vectors and adds them to the FAISS index
    """
    global documents
    documents = docs
    embeddings = model.encode(docs)
    index.add(np.array(embeddings))  # Add vectors to FAISS

def search(query: str, k: int = 3) -> list[str]:
    """
    Searches FAISS index using query vector and returns top-k matching documents
    """
    query_vec = model.encode([query])
    distances, indices = index.search(np.array(query_vec), k)
    return [documents[i] for i in indices[0]]
