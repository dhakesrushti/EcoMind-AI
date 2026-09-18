from pydantic import BaseModel
from typing import Dict, List, Optional, Any

class ChatRequest(BaseModel):
    session_id: str
    message: str

class ChatResponse(BaseModel):
    analysis: str
    key_factors: List[str]
    recommendations: List[str]
    expected_impact: List[str]
    scientific_evidence: List[str]
    sources: List[str]
    reasoning_trace: str
    state: Dict[str, Any] # current known environmental variables
    needs_more_info: bool
    follow_up_questions: List[str]

class StatusResponse(BaseModel):
    status: str
    document_count: int
    chunks_count: int
