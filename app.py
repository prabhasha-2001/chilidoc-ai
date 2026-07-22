import streamlit as st
import re
from agents import diagnostic_specialist_agent, rag_researcher_agent, agronomy_critic_agent

# Page Configuration
st.set_page_config(
    page_title="ChiliDoc AI - Smart Agronomic Assistant",
    page_icon="🌶️",
    layout="wide"
)

# Custom Styling & CSS Animations
st.markdown("""
    <style>
    /* Main Title and Subtitle Styling */
    .main-title { 
        font-size: 42px; 
        color: #D32F2F; 
        font-weight: 800; 
        font-family: 'Inter', sans-serif;
    }
    .sub-title { 
        font-size: 18px; 
        color: #555; 
        margin-bottom: 10px;
    }
    .agent-box { 
        padding: 20px; 
        border-radius: 12px; 
        background-color: #f8f9fa; 
        margin-bottom: 20px; 
        border-left: 6px solid #2E7D32;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    
    /* Smooth Bouncing Animation for Header Chili Icon */
    .chili-animation-container {
        display: flex;
        justify-content: center;
        align-items: center;
        margin-bottom: 5px;
    }
    
    .animated-chili-icon {
        font-size: 70px;
        display: inline-block;
        animation: floatAndBounce 3s ease-in-out infinite;
    }

    @keyframes floatAndBounce {
        0% { transform: translateY(0px) rotate(0deg) scale(1); }
        50% { transform: translateY(-15px) rotate(8deg) scale(1.1); }
        100% { transform: translateY(0px) rotate(0deg) scale(1); }
    }

    /* Talking Chili Avatar & Thought Speech Bubble Styling */
    .chili-speech-container {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-top: 15px;
        margin-bottom: 10px;
    }
    
    .chili-avatar {
        font-size: 45px;
        animation: pulse 2s infinite ease-in-out;
    }

    .thought-bubble {
        position: relative;
        background: #ffffff;
        border: 2px solid #D32F2F;
        border-radius: 18px;
        padding: 12px 18px;
        font-size: 15px;
        font-weight: 600;
        color: #2c3e50;
        box-shadow: 2px 4px 10px rgba(0,0,0,0.08);
    }

    /* Triangle pointer for the speech bubble */
    .thought-bubble:before {
        content: '';
        position: absolute;
        bottom: 12px;
        left: -12px;
        border-width: 8px 12px 8px 0;
        border-style: solid;
        border-color: transparent #D32F2F transparent transparent;
        display: block;
        width: 0;
    }

    .thought-bubble:after {
        content: '';
        position: absolute;
        bottom: 14px;
        left: -9px;
        border-width: 6px 9px 6px 0;
        border-style: solid;
        border-color: transparent #ffffff transparent transparent;
        display: block;
        width: 0;
    }

    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.1) rotate(-5deg); }
        100% { transform: scale(1); }
    }
    </style>
""", unsafe_allow_html=True)

# Top Bouncing Animated Chili Header
st.markdown("""
    <div class="chili-animation-container">
        <div class="animated-chili-icon">🌶️</div>
    </div>
""", unsafe_allow_html=True)

# Header Section
st.markdown('<div class="main-title" style="text-align: center;">ChiliDoc AI</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title" style="text-align: center;">Multi-Agent Agronomic Advisor & Diagnostic System</div>', unsafe_allow_html=True)
st.divider()

# Sidebar for Configuration & System Info
with st.sidebar:
    st.header("⚙️ Configuration")
    st.info("System status: **Active & Online**")
    st.markdown("---")
    st.markdown("### 🤖 Active Agents:")
    st.markdown("1. **Diagnostic Specialist** (ReAct)")
    st.markdown("2. **RAG Researcher** (Vector DB)")
    st.markdown("3. **Agronomy Critic** (Reflection)")

# Animated Talking Chili Avatar with Thought Speech Bubble
st.markdown("""
    <div class="chili-speech-container">
        <div class="chili-avatar">🌶️</div>
        <div class="thought-bubble">
            Describe the symptoms visible on your chili plant or ask me a question!
        </div>
    </div>
""", unsafe_allow_html=True)

# User Symptom Input Field
user_query = st.text_area(
    label="",
    placeholder="e.g., The leaves are curling upwards and showing dark spots, and fruit is drooping...",
    height=100
)

col1, col2 = st.columns([1, 4])
with col1:
    submit_btn = st.button("🚀 Analyze & Diagnose", type="primary", use_container_width=True)

# Main Agentic Execution Workflow
if submit_btn:
    if not user_query.strip():
        st.warning("Please describe your plant's symptoms before running the diagnosis.")
    else:
        # Step 1: Execute Diagnostic Specialist Agent
        with st.spinner("🤖 Agent 1: Diagnostic Specialist is analyzing symptoms..."):
            diag_output = diagnostic_specialist_agent(user_query)
            
        with st.expander("🔍 Step 1: Diagnostic Hypothesis (Specialist Agent)", expanded=True):
            st.markdown(diag_output)

        # Step 2: Execute RAG Researcher Agent
        with st.spinner("📚 Agent 2: RAG Researcher is scanning agricultural literature..."):
            rag_output, retrieved_docs = rag_researcher_agent(user_query, diag_output)
            
        with st.expander("📖 Step 2: Literature & Research Context (RAG Agent)", expanded=False):
            st.markdown(rag_output)
            if retrieved_docs:
                st.subheader("Cited Knowledge Sources:")
                for i, doc in enumerate(retrieved_docs, 1):
                    source = doc.metadata.get('source', 'Unknown Document')
                    st.caption(f"**Source {i}:** `{source}`")

        # Step 3: Execute Agronomy Critic Agent for Safety & Self-Reflection
        with st.spinner("🛡️ Agent 3: Agronomy Critic is reviewing for safety and sustainability..."):
            final_advisory = agronomy_critic_agent(diag_output, rag_output)
            
            # Clean up default placeholder names in the advisory response
            final_advisory = re.sub(r'\[(?:Your\s+)?Name\]', 'ChiliDoc AI Team', final_advisory, flags=re.IGNORECASE)

        # Display Approved Final Treatment Plan
        st.success("✅ Final Approved Treatment Advisory")
        st.markdown(f'<div class="agent-box">{final_advisory}</div>', unsafe_allow_html=True)