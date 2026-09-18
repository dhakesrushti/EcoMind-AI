import os
import re
import google.generativeai as genai
from typing import Dict, Any, Tuple, List
from dotenv import load_dotenv
from retriever import retrieve_context, format_context_for_prompt

load_dotenv()

def get_gemini_model():
    """Initialize and return the Gemini model."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in environment variables.")
    
    genai.configure(api_key=api_key)
    # Use gemini-flash-lite-latest as it has a much higher free-tier limit (e.g. 1500/day) compared to standard flash models
    return genai.GenerativeModel('gemini-flash-lite-latest')

REQUIRED_VARS = [
    "soil_carbon",
    "rainfall",
    "biodiversity",
    "land_use",
    "pollinator_presence"
]

def update_conversation_state(user_input: str, current_state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Update state based on user input using fast heuristic extraction instead of a slow LLM call.
    This halves the response time and saves API quota.
    """
    lower_input = user_input.lower()
    
    # Simple heuristic extraction
    for var in REQUIRED_VARS:
        var_display = var.replace("_", " ")
        if var_display in lower_input or var in lower_input:
            # Check for generic values nearby
            if "low" in lower_input or "decreas" in lower_input or "poor" in lower_input:
                current_state[var] = "low"
            elif "high" in lower_input or "increas" in lower_input or "good" in lower_input:
                current_state[var] = "high"
            else:
                current_state[var] = "unknown / needs detail"
                
    return current_state

def check_missing_info(current_state: Dict[str, Any]) -> List[str]:
    """Return a list of missing required variables."""
    missing = []
    for var in REQUIRED_VARS:
        if var not in current_state or not current_state[var]:
            missing.append(var)
    return missing

def perform_reasoning(current_state: Dict[str, Any]) -> str:
    """Generate a reasoning trace based on the current state."""
    trace = "Reasoning Trace:\n"
    trace += "Analyzing current environmental factors...\n"
    
    # Example hardcoded reasoning logic based on user requirements
    sc = str(current_state.get("soil_carbon") or "").lower()
    rf = str(current_state.get("rainfall") or "").lower()
    bd = str(current_state.get("biodiversity") or "").lower()
    pp = str(current_state.get("pollinator_presence") or "").lower()
    
    if sc and "low" in sc:
        if rf and "low" in rf:
            trace += "Low Soil Carbon + Low Rainfall -> Recommending Agroforestry or drought-resistant ground cover.\n"
            
    if (bd and "low" in bd) or "decreas" in bd:
        trace += "Low/Decreasing Biodiversity -> Habitat Restoration required. Evaluating pollinator presence.\n"
        
    if pp and "low" in pp:
        trace += "Low Pollinator Presence -> Suggesting planting native flowering species.\n"
        
    trace += f"Contextual variables currently tracked: {', '.join([f'{k}: {v}' for k,v in current_state.items() if v])}\n"
    return trace

def generate_response(query: str, current_state: Dict[str, Any]) -> Tuple[str, str, List[Dict[str, Any]]]:
    """
    Main function to generate the response.
    Returns (final_response, reasoning_trace, retrieved_chunks)
    """
    # 1. Update state (simulate entity extraction)
    updated_state = update_conversation_state(query, current_state)
    
    # 2. Check for missing information
    missing_vars = check_missing_info(updated_state)
    
    # If there are missing variables, we MIGHT ask a follow up.
    # However, to be helpful, we only ask if the query is a broad recommendation request
    # For a general question, we might still proceed. 
    # Let's instruct the LLM to ask follow-up if it deems necessary based on missing_vars
    
    # 3. Retrieve context via RAG
    retrieved_chunks = retrieve_context(query)
    context_str = format_context_for_prompt(retrieved_chunks)
    
    # 4. Perform deterministic/heuristic reasoning (Trace)
    reasoning_trace = perform_reasoning(updated_state)
    
    # 5. Build prompt for Gemini
    prompt = f"""
    You are EcoMind AI, an expert Environmental Consultant.
    
    User Question: {query}
    
    Current Environmental State: {updated_state}
    Missing Environmental Variables: {missing_vars}
    
    Retrieved Context from Knowledge Base:
    {context_str}
    
    INSTRUCTIONS:
    If the user is asking for specific recommendations and crucial environmental variables are missing (from the Missing Environmental Variables list), you MUST start your response by asking for them.
    Example: "To provide accurate recommendations I need: - Soil organic carbon level - Rainfall pattern"
    
    Otherwise, answer the question using the provided context and environmental state.
    
    You MUST format your response EXACTLY with these sections (use Markdown headings):
    
    ### 1. Analysis
    (Your analysis of the situation based on context and state)
    
    ### 2. Recommendations
    (Actionable steps)
    
    ### 3. Expected Impact
    (What these steps will achieve)
    
    ### 4. Evidence
    (Why this works, based on science/context)
    
    ### 5. Sources
    (List the document sources used from the retrieved context)
    
    (Note: The Reasoning Trace will be displayed separately in the UI, do not include it here).
    """
    
    try:
        model = get_gemini_model()
        response = model.generate_content(prompt)
        final_answer = response.text
    except Exception as e:
        final_answer = f"Error generating response: {e}. Please ensure your GEMINI_API_KEY is correct."
        
    return final_answer, reasoning_trace, retrieved_chunks, updated_state
