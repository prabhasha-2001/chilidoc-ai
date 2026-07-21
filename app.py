import streamlit as st
import re
from agents import diagnostic_specialist_agent, rag_researcher_agent, agronomy_critic_agent

# Page Configuration
st.set_page_config(
    page_title="ChiliDoc AI - Smart Agronomic Assistant",
    page_icon="🌶️",
    layout="wide"
)

# Custom Styling
st.markdown("""
    <style>
    .main-title { font-size: 38px; color: #D32F2F; font-weight: bold; }
    .sub-title { font-size: 18px; color: #555; }
    .agent-box { padding: 15px; border-radius: 10px; background-color: #f8f9fa; margin-bottom: 15px; border-left: 5px solid #2E7D32; }
    </style>
""", unsafe_allow_html=True)

# Header Section
st.markdown('<div class="main-title">🌶️ ChiliDoc AI</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Multi-Agent Agronomic Advisor & Diagnostic System</div>', unsafe_allow_html=True)
st.divider()

# Sidebar for Config & Information
with st.sidebar:
    st.header("⚙️ Configuration")
    st.info("System status: **Active & Online**")
    st.markdown("---")
    st.markdown("### 🤖 Active Agents:")
    st.markdown("1. **Diagnostic Specialist** (ReAct)")
    st.markdown("2. **RAG Researcher** (Vector DB)")
    st.markdown("3. **Agronomy Critic** (Reflection)")

# Main Query Form
user_query = st.text_area(
    "Describe the symptoms visible on your chili plant or ask a question:",
    placeholder="e.g., The leaves are curling upwards and showing dark spots, and fruit is drooping...",
    height=100
)

col1, col2 = st.columns([1, 4])
with col1:
    submit_btn = st.button("🚀 Analyze & Diagnose", type="primary", use_container_width=True)

if submit_btn:
    if not user_query.strip():
        st.warning("Please describe your plant's symptoms before running the diagnosis.")
    else:
        # Step 1: Diagnostic Specialist
        with st.spinner("🤖 Agent 1: Diagnostic Specialist is analyzing symptoms..."):
            diag_output = diagnostic_specialist_agent(user_query)
            
        with st.expander("🔍 Step 1: Diagnostic Hypothesis (Specialist Agent)", expanded=True):
            st.markdown(diag_output)

        # Step 2: RAG Researcher
        with st.spinner("📚 Agent 2: RAG Researcher is scanning agricultural literature..."):
            rag_output, retrieved_docs = rag_researcher_agent(user_query, diag_output)
            
        with st.expander("📖 Step 2: Literature & Research Context (RAG Agent)", expanded=False):
            st.markdown(rag_output)
            if retrieved_docs:
                st.subheader("Cited Knowledge Sources:")
                for i, doc in enumerate(retrieved_docs, 1):
                    source = doc.metadata.get('source', 'Unknown Document')
                    st.caption(f"**Source {i}:** `{source}`")

        # Step 3: Agronomy Critic
        with st.spinner("🛡️ Agent 3: Agronomy Critic is reviewing for safety and sustainability..."):
            final_advisory = agronomy_critic_agent(diag_output, rag_output)
            
            # Clean up placeholders and names
            final_advisory = re.sub(r'\[(?:Your\s+)?Name\]', 'ChiliDoc AI Team', final_advisory, flags=re.IGNORECASE)

        # Final Approved Advisory Result
        st.success("✅ Final Approved Treatment Advisory")
        st.markdown(f'<div class="agent-box">{final_advisory}</div>', unsafe_allow_html=True)