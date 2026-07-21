import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from rag_utils import get_relevant_docs

# Load environment variables
load_dotenv()

# Initialize API Keys
groq_api_key = os.getenv("GROQ_API_KEY")
openrouter_api_key = os.getenv("OPENROUTER_API_KEY") or os.getenv("OPENAI_API_KEY")

# Model 1: Fast, Low-Cost & Low-Latency (Groq Llama 3.1) - Fast ReAct Diagnostics & RAG Context Extraction
fast_llm = ChatGroq(
    groq_api_key=groq_api_key,
    model_name="llama-3.1-8b-instant",
    temperature=0.2
)

# Model 2: High Reasoning & Safety Reflection (OpenRouter / OpenAI) -  Complex Safety Auditing, Chemical Verification & Final Synthesis
reasoning_llm = ChatOpenAI(
    api_key=openrouter_api_key,
    base_url="https://openrouter.ai/api/v1" if os.getenv("OPENROUTER_API_KEY") else None,
    model_name="openai/gpt-4o-mini" if os.getenv("OPENROUTER_API_KEY") else "gpt-4o-mini",
    temperature=0.3
)


# AGENT 1: Diagnostic Specialist (ReAct Pattern) 
def diagnostic_specialist_agent(user_query, image_analysis_summary=""):
    """
    Analyzes visual disease symptoms and farmer input using ReAct reasoning.
    Uses: fast_llm (Groq) for rapid symptom parsing.
    """
    prompt = f"""
    You are an expert Crop Disease Diagnostic Specialist specializing in Chili plants.
    
    User Query / Symptoms: {user_query}
    Visual Analysis Summary from Image: {image_analysis_summary}
    
    Task:
    1. Reason through the observed symptoms step-by-step.
    2. Formulate a preliminary hypothesis of the disease (e.g., Anthracnose, Leaf Curl, Bacterial Wilt).
    3. Specify what additional domain-specific information or verification is needed from the knowledge base.
    
    Provide a clear, structured diagnostic reasoning output.
    """
    # fast_llm 
    response = fast_llm.invoke(prompt)
    return response.content


# AGENT 2: RAG Researcher (Tool-Use / Retrieval Pattern)
def rag_researcher_agent(query, diagnostic_hypothesis):
    """
    Uses RAG Tool to retrieve research-backed management strategies from PDF documents.
    Uses: fast_llm (Groq) for fast context processing.
    """
    search_query = f"{query} {diagnostic_hypothesis}"
    retrieved_docs = get_relevant_docs(search_query)
    
    context = "\n\n".join([doc.page_content for doc in retrieved_docs]) if retrieved_docs else "No specific documents found."
    
    prompt = f"""
    You are an Agricultural Research Agent with access to specialized literature on Chili crops.
    
    Diagnostic Context: {diagnostic_hypothesis}
    Retrieved Scientific Literature Context:
    {context}
    
    Task:
    1. Extract verified chemical, biological, and cultural control treatments.
    2. Cite relevant research practices found in the context.
    3. Formulate a detailed management and treatment plan.
    """
    # fast_llm
    response = fast_llm.invoke(prompt)
    return response.content, retrieved_docs


# AGENT 3: Agronomy Critic (Reflection / Self-Critique Pattern)
def agronomy_critic_agent(diagnostic_plan, research_treatment_plan):
    """
    Reflects on proposed treatments for safety, practicality, and environmental sustainability.
    Uses: reasoning_llm (OpenRouter/GPT-4o-mini) for safety evaluation.
    """
    prompt = f"""
    You are a Senior Agronomist and Safety Critic evaluating crop disease treatment plans.
    
    Diagnostic Hypothesis: {diagnostic_plan}
    Proposed Treatment Plan: {research_treatment_plan}
    
    Task (Reflection & Refinement):
    1. Evaluate safety for smallholder farmers (dosage, chemical handling, safety equipment).
    2. Ensure biological controls are prioritized where suitable.
    3. Check for any conflicting recommendations.
    4. Provide the FINAL APPROVED advisory response for the farmer. Do NOT use placeholders like [Your Name].
    """
    # reasoning_llm (Deep reasoning requirements)
    response = reasoning_llm.invoke(prompt)
    return response.content


if __name__ == "__main__":
    test_query = "My chili plant leaves have dark sunken spots on the fruit."
    
    print("\n--- 1. Running Diagnostic Specialist (Groq) ---")
    diag_res = diagnostic_specialist_agent(test_query)
    print(diag_res)
    
    print("\n--- 2. Running RAG Researcher (Groq) ---")
    rag_res, docs = rag_researcher_agent(test_query, diag_res)
    print(rag_res)
    
    print("\n--- 3. Running Agronomy Critic (OpenRouter/Deep Reasoning) ---")
    final_res = agronomy_critic_agent(diag_res, rag_res)
    print(final_res)