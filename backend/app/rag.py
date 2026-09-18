import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
CHROMA_DB_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "chroma_db")

# Global variables
vector_store = None
embeddings = None

def init_rag_pipeline():
    global vector_store, embeddings
    print("Initializing embeddings model...")
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    if os.path.exists(CHROMA_DB_DIR) and os.listdir(CHROMA_DB_DIR):
        print("Loading existing Chroma database...")
        vector_store = Chroma(persist_directory=CHROMA_DB_DIR, embedding_function=embeddings)
    else:
        print("No existing Chroma database found. Ingesting documents...")
        ingest_documents()

def ingest_documents():
    global vector_store, embeddings
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
        
    source_dir = r"C:\Users\dhake\Downloads\Dataset for assessment"
    expected_pdfs = [
        "sustainability-11-02879.pdf",
        "FAO Recarbonizing Soils Manual.pdf",
        "OpenLandMap.pdf",
        "soil_health.pdf",
        "s41597-026-07749-4.pdf"
    ]
    
    import shutil
    if os.path.exists(source_dir):
        for pdf in expected_pdfs:
            src_path = os.path.join(source_dir, pdf)
            dst_path = os.path.join(DATA_DIR, pdf)
            if os.path.exists(src_path) and not os.path.exists(dst_path):
                shutil.copy2(src_path, dst_path)
                print(f"Copied {pdf} to data directory.")

    documents = []
    for filename in os.listdir(DATA_DIR):
        if filename.endswith(".pdf"):
            file_path = os.path.join(DATA_DIR, filename)
            try:
                loader = PyPDFLoader(file_path)
                documents.extend(loader.load())
            except Exception as e:
                print(f"Error loading {filename}: {e}")
            
    if not documents:
        print("No PDF documents found in data directory.")
        return
        
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=300)
    splits = text_splitter.split_documents(documents)
    
    print("Creating Chroma vector store...")
    vector_store = Chroma.from_documents(
        documents=splits,
        embedding=embeddings,
        persist_directory=CHROMA_DB_DIR
    )
    vector_store.persist()
    print(f"Ingested {len(documents)} pages, created {len(splits)} chunks.")

def retrieve_context(query: str, k: int = 3):
    if vector_store is None:
        return []
    results = vector_store.similarity_search(query, k=k)
    return results
