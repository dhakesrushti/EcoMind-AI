import streamlit as st
import os
from ingestion import ingest_document, get_document_count, get_unique_sources, clear_knowledge_base
from reasoning import generate_response, REQUIRED_VARS

# Apply Professional Dark Theme configuration
st.set_page_config(
    page_title="EcoMind AI",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for dark theme and styling
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #0d1117 0%, #161b22 100%);
        color: #c9d1d9;
    }
    .css-1d391kg {
        background-color: #161b22;
        border-right: 1px solid #30363d;
    }
    .stTextInput>div>div>input {
        color: #c9d1d9;
        background-color: #0d1117;
        border: 1px solid #30363d;
        border-radius: 8px;
    }
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
        color: #58a6ff;
        font-weight: 600;
        letter-spacing: -0.5px;
    }
    .stButton>button {
        background: linear-gradient(180deg, #238636 0%, #2ea043 100%);
        color: white;
        border: 1px solid rgba(240, 246, 252, 0.1);
        border-radius: 6px;
        transition: all 0.2s ease-in-out;
        font-weight: 500;
    }
    .stButton>button:hover {
        background: #2ea043;
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(46, 160, 67, 0.2);
    }
    .chat-message {
        padding: 1.5rem;
        border-radius: 12px;
        margin-bottom: 1rem;
        display: flex;
        flex-direction: column;
        backdrop-filter: blur(10px);
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.05);
    }
    .chat-message.user {
        background-color: rgba(35, 134, 54, 0.1);
        border-left: 4px solid #238636;
    }
    .chat-message.bot {
        background-color: rgba(88, 166, 255, 0.1);
        border-left: 4px solid #58a6ff;
    }
    
    /* Sleeker expander */
    .streamlit-expanderHeader {
        background-color: rgba(255, 255, 255, 0.02) !important;
        border-radius: 6px;
        border: 1px solid rgba(255, 255, 255, 0.05);
    }
</style>
""", unsafe_allow_html=True)

# Initialize Session State
if "messages" not in st.session_state:
    st.session_state.messages = []
    
if "env_state" not in st.session_state:
    st.session_state.env_state = {var: None for var in REQUIRED_VARS}

# Sidebar
with st.sidebar:
    st.title("🌿 EcoMind AI")
    
    st.subheader("Knowledge Base")
    doc_count = get_document_count()
    st.metric(label="Total Chunks in DB", value=doc_count)
    
    unique_sources = get_unique_sources()
    if unique_sources:
        with st.expander("Documents in DB"):
            for src in unique_sources:
                st.write(f"- {src}")
                
        if st.button("🗑️ Clear Knowledge Base", help="Remove all uploaded documents from the database"):
            clear_knowledge_base()
            st.rerun()
    
    st.divider()
    
    st.subheader("Upload Documents")
    uploaded_files = st.file_uploader(
        "Upload PDF Papers or Datasets", 
        type=["pdf", "txt", "csv"], 
        accept_multiple_files=True
    )
    
    if st.button("Process Documents"):
        if uploaded_files:
            with st.spinner("Processing and chunking..."):
                total_chunks = 0
                for file in uploaded_files:
                    chunks_added = ingest_document(file.name, file)
                    total_chunks += chunks_added
                st.success(f"Successfully processed and stored {total_chunks} chunks!")
                st.rerun()
        else:
            st.warning("Please upload files first.")



# Main Content Area
st.title("AI Environmental Consultant")
st.markdown("Ask environmental questions based on uploaded research papers and datasets.")

# Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        
        # Display Reasoning Trace & Sources if available
        if message["role"] == "assistant" and "reasoning" in message:
            with st.expander("View Reasoning Trace"):
                st.markdown(message["reasoning"])
            if "sources" in message and message["sources"]:
                with st.expander("Retrieved Sources"):
                    for src in message["sources"]:
                        st.markdown(f"**{src['source']}**")
                        st.markdown(f"> {src['text']}")

# Chat Input
if prompt := st.chat_input("How can I improve biodiversity?"):
    # Check for API key
    if not os.getenv("GEMINI_API_KEY"):
        st.error("Please provide a Gemini API Key in the .env file.")
        st.stop()
        
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.markdown(prompt)
        
    # Generate Assistant Response
    with st.chat_message("assistant"):
        with st.spinner("Analyzing and reasoning..."):
            # generate_response updates the env_state internally and returns the updated state
            final_answer, reasoning_trace, sources, updated_state = generate_response(
                prompt, st.session_state.env_state
            )
            
            # Update session state with new env_state
            st.session_state.env_state = updated_state
            
            # Display response
            st.markdown(final_answer)
            
            with st.expander("View Reasoning Trace"):
                st.markdown(reasoning_trace)
                
            if sources:
                with st.expander("Retrieved Sources"):
                    for src in sources:
                        st.markdown(f"**{src['source']}**")
                        st.markdown(f"> {src['text']}")
            
            # Add to history
            st.session_state.messages.append({
                "role": "assistant",
                "content": final_answer,
                "reasoning": reasoning_trace,
                "sources": sources
            })
