import json
from typing import Dict, Any, Tuple, List
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
import os

sessions = {}

REQUIRED_VARS = ["soil_carbon", "rainfall", "land_use", "pollinator_presence"]
OPTIONAL_VARS = ["temperature", "biodiversity", "soil_ph", "soil_texture", "vegetation_type", "elevation", "soil_health_score", "carbon_stock"]

def get_session_state(session_id: str) -> Dict[str, Any]:
    if session_id not in sessions:
        sessions[session_id] = {}
    return sessions[session_id]

def update_state_with_query(session_id: str, query: str) -> Tuple[Dict[str, Any], List[str]]:
    state = get_session_state(session_id)
    
    # We use a quick LLM call to extract variables from the user's query
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro", temperature=0)
    
    extract_prompt = PromptTemplate.from_template(
        """Extract environmental variables from the user's query and output them as a JSON dictionary. 
        Possible variables to look for: {vars}
        Current known variables: {state}
        User Query: {query}
        
        Only output valid JSON, nothing else. If none found, output {{}}.
        """
    )
    all_vars = REQUIRED_VARS + OPTIONAL_VARS
    chain = extract_prompt | llm
    result = chain.invoke({"vars": ", ".join(all_vars), "state": json.dumps(state), "query": query})
    
    try:
        content = result.content
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0]
        elif "```" in content:
            content = content.split("```")[1].split("```")[0]
        new_vars = json.loads(content.strip())
        for k, v in new_vars.items():
            if k in all_vars:
                state[k] = str(v).lower()
    except Exception as e:
        print("Failed to parse extracted vars", e)
        
    sessions[session_id] = state
    
    missing_vars = [var for var in REQUIRED_VARS if var not in state]
    return state, missing_vars
