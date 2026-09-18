import chromadb
from typing import List, Dict, Any
from ingestion import collection_name, embedding_function, CHROMA_DATA_PATH

def get_chroma_collection():
    """Helper to get the ChromaDB collection."""
    client = chromadb.PersistentClient(path=CHROMA_DATA_PATH)
    return client.get_or_create_collection(
        name=collection_name,
        embedding_function=embedding_function
    )

def retrieve_context(query: str, n_results: int = 5) -> List[Dict[str, Any]]:
    """
    Retrieve relevant chunks for a given query from ChromaDB.
    """
    collection = get_chroma_collection()
    
    if collection.count() == 0:
        return []
        
    results = collection.query(
        query_texts=[query],
        n_results=min(n_results, collection.count())
    )
    
    retrieved_chunks = []
    
    # Check if we have documents and metadatas
    if results and "documents" in results and "metadatas" in results:
        documents = results["documents"][0]
        metadatas = results["metadatas"][0]
        
        for doc, meta in zip(documents, metadatas):
            retrieved_chunks.append({
                "text": doc,
                "source": meta.get("source", "Unknown Source")
            })
            
    return retrieved_chunks

def format_context_for_prompt(retrieved_chunks: List[Dict[str, Any]]) -> str:
    """
    Format the retrieved chunks into a single string to inject into the LLM prompt.
    """
    if not retrieved_chunks:
        return "No external context provided."
        
    context = ""
    for i, chunk in enumerate(retrieved_chunks):
        context += f"--- Document Source: {chunk['source']} ---\n"
        context += f"{chunk['text']}\n\n"
        
    return context
