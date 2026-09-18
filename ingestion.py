import os
import uuid
from typing import List, Dict, Any
from PyPDF2 import PdfReader
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer

# Initialize ChromaDB client (local storage)
CHROMA_DATA_PATH = "./chroma_db"
client = chromadb.PersistentClient(path=CHROMA_DATA_PATH)

from chromadb.utils import embedding_functions

# Use sentence-transformers embedding function
# Chroma has a built-in SentenceTransformerEmbeddingFunction that handles everything correctly
embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")

# Get or create collection
collection_name = "ecomind_documents"
collection = client.get_or_create_collection(
    name=collection_name,
    embedding_function=embedding_function
)

def extract_text_from_pdf(file_bytes) -> str:
    """Extract text from a PDF file."""
    reader = PdfReader(file_bytes)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    return text

def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 200) -> List[str]:
    """Split text into overlapping chunks."""
    chunks = []
    start = 0
    text_length = len(text)
    
    while start < text_length:
        end = min(start + chunk_size, text_length)
        chunk = text[start:end]
        chunks.append(chunk)
        start += chunk_size - overlap
        
    return chunks

def ingest_document(file_name: str, file_bytes) -> int:
    """
    Process a document and store it in ChromaDB.
    Returns the number of chunks processed.
    """
    # 1. Extract text
    if file_name.lower().endswith('.pdf'):
        text = extract_text_from_pdf(file_bytes)
    else:
        # For simplicity, fallback to decoding if it's a raw text file or dataset
        try:
            text = file_bytes.read().decode('utf-8')
        except Exception:
            text = str(file_bytes.read())
            
    if not text.strip():
        return 0

    # 2. Chunk text
    chunks = chunk_text(text)
    
    if not chunks:
        return 0
        
    # 3. Prepare data for ChromaDB
    ids = [str(uuid.uuid4()) for _ in range(len(chunks))]
    metadatas = [{"source": file_name, "chunk_index": i} for i in range(len(chunks))]
    
    # 4. Store in ChromaDB
    collection.add(
        documents=chunks,
        metadatas=metadatas,
        ids=ids
    )
    
    return len(chunks)

def get_document_count() -> int:
    """Return the total number of documents (chunks) in the collection."""
    return collection.count()

def get_unique_sources() -> List[str]:
    """Return a list of unique source documents in the collection."""
    if collection.count() == 0:
        return []
    
    results = collection.get(include=["metadatas"])
    sources = set()
    for meta in results.get("metadatas", []):
        if meta and "source" in meta:
            sources.add(meta["source"])
    return list(sources)

def clear_knowledge_base():
    """Clear all documents from the knowledge base."""
    global collection
    client.delete_collection(name=collection_name)
    collection = client.get_or_create_collection(
        name=collection_name,
        embedding_function=embedding_function
    )
