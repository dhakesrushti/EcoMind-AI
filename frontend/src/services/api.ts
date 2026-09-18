import axios from 'axios';

const API_URL = 'http://localhost:8000/api';

export interface ChatRequest {
    session_id: string;
    message: string;
}

export interface ChatResponse {
    analysis: string;
    key_factors: string[];
    recommendations: string[];
    expected_impact: string[];
    scientific_evidence: string[];
    sources: string[];
    reasoning_trace: string;
    state: Record<string, any>;
    needs_more_info: boolean;
    follow_up_questions: string[];
}

export interface StatusResponse {
    status: string;
    document_count: number;
    chunks_count: number;
}

export const chat = async (request: ChatRequest): Promise<ChatResponse> => {
    const response = await axios.post(`${API_URL}/chat`, request);
    return response.data;
};

export const getKbStatus = async (): Promise<StatusResponse> => {
    const response = await axios.get(`${API_URL}/kb/status`);
    return response.data;
};
