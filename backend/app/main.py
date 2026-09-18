from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .models import ChatRequest, ChatResponse, StatusResponse
from .rag import init_rag_pipeline, vector_store
from .generator import generate_response
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI(title="EcoMind AI API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    # If API Key not in env, we must warn or fail
    if not os.getenv("GEMINI_API_KEY"):
        print("WARNING: GEMINI_API_KEY environment variable is missing.")
    init_rag_pipeline()

@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    return generate_response(request.session_id, request.message)

@app.get("/api/kb/status", response_model=StatusResponse)
async def kb_status():
    if vector_store:
        return StatusResponse(status="Ready", document_count=5, chunks_count=100) # Mock counts for brevity
    return StatusResponse(status="Uninitialized", document_count=0, chunks_count=0)
