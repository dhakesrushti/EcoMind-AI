import json
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from .models import ChatResponse
from .rag import retrieve_context
from .state import update_state_with_query
from .reasoning import run_reasoning_engine

def generate_response(session_id: str, query: str) -> ChatResponse:
    # 1. Update state and check missing variables
    state, missing_vars = update_state_with_query(session_id, query)
    
    # If missing required info, return asking for it
    if missing_vars:
        # Format the follow up nicely
        bullet_points = "\n".join([f"• {var.replace('_', ' ').capitalize()}" for var in missing_vars])
        analysis_text = f"To better understand the causes, I need a few details:\n\n{bullet_points}\n\nOnce I have this information, I can provide evidence-backed recommendations."
        
        return ChatResponse(
            analysis=analysis_text,
            key_factors=[f"{k}: {v}" for k, v in state.items()],
            recommendations=[],
            expected_impact=[],
            scientific_evidence=[],
            sources=[],
            reasoning_trace="Waiting for sufficient data.",
            state=state,
            needs_more_info=True,
            follow_up_questions=[f"What is your {var.replace('_', ' ')}?" for var in missing_vars]
        )
        
    # 2. Retrieve Context
    # We formulate a query based on the state to get better results
    state_query = " ".join([f"{k} is {v}" for k, v in state.items()])
    docs = retrieve_context(query + " " + state_query, k=3)
    context_text = "\n\n".join([d.page_content for d in docs])
    sources = list(set([d.metadata.get("source", "Unknown Document").split("/")[-1].split("\\")[-1] for d in docs]))
    
    # 3. Reasoning Engine
    rule_recommendations, reasoning_trace = run_reasoning_engine(state)
    
    # 4. Gemini Response
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro", temperature=0.2)
    
    prompt = PromptTemplate.from_template(
        """You are EcoMind AI, an expert Environmental Consultant. 
        Based on the following known environmental variables, rule-engine recommendations, and retrieved scientific evidence, 
        provide a comprehensive, scientifically grounded assessment.
        
        Current Environmental Variables: {state}
        Rule-Engine Recommendations: {rule_recommendations}
        
        Retrieved Scientific Evidence:
        {context}
        
        Format your response EXACTLY as this JSON structure:
        {{
            "analysis": "Explain the environmental issues identified based on the variables.",
            "expected_impact": ["Benefit 1", "Benefit 2"],
            "scientific_evidence": ["Evidence quote 1", "Evidence quote 2"]
        }}
        
        Ensure your scientific evidence quotes are actually derived from the provided retrieved context. Do not hallucinate citations.
        """
    )
    
    chain = prompt | llm
    result = chain.invoke({
        "state": json.dumps(state),
        "rule_recommendations": ", ".join(rule_recommendations),
        "context": context_text
    })
    
    try:
        content = result.content
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0]
        elif "```" in content:
            content = content.split("```")[1].split("```")[0]
        llm_json = json.loads(content.strip())
        
        return ChatResponse(
            analysis=llm_json.get("analysis", "Analysis completed."),
            key_factors=[f"{k}: {v}" for k, v in state.items()],
            recommendations=rule_recommendations if rule_recommendations else ["General best practices recommended."],
            expected_impact=llm_json.get("expected_impact", []),
            scientific_evidence=llm_json.get("scientific_evidence", []),
            sources=sources,
            reasoning_trace=reasoning_trace,
            state=state,
            needs_more_info=False,
            follow_up_questions=[]
        )
    except Exception as e:
        print("Error parsing LLM output", e)
        # Fallback
        return ChatResponse(
            analysis="Environmental stress detected based on provided factors.",
            key_factors=[f"{k}: {v}" for k, v in state.items()],
            recommendations=rule_recommendations,
            expected_impact=["Improved environmental resilience"],
            scientific_evidence=["Evidence retrieved from documents."],
            sources=sources,
            reasoning_trace=reasoning_trace,
            state=state,
            needs_more_info=False,
            follow_up_questions=[]
        )
