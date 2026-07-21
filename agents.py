import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from rag_utils import get_relevant_docs

# Load environment variables
load_dotenv()

# Initialize LLM Models
groq_api_key = os.getenv("GROQ_API_KEY")

# Primary LLM for Diagnostic Specialist & Agronomy Critic
llm = ChatGroq(
    groq_api_key=groq_api_key,
    model_name="llama-3.1-8b-instant",
    temperature=0.2
)

# AGENT 1: Diagnostic Specialist (ReAct Pattern) 
def diagnostic_specialist_agent(user_query, image_analysis_summary=""):
    """
    Analyzes visual disease symptoms and farmer input using ReAct reasoning.
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
    response = llm.invoke(prompt)
    return response.content

# AGENT 2: RAG Researcher (Tool-Use Pattern)
def rag_researcher_agent(query, diagnostic_hypothesis):
    """
    Uses RAG Tool to retrieve research-backed management strategies from PDF documents.
    """
    # Search Vector Database using rag_utils tool
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
    response = llm.invoke(prompt)
    return response.content, retrieved_docs

# AGENT 3: Agronomy Critic (Reflection Pattern)
def agronomy_critic_agent(diagnostic_plan, research_treatment_plan):
    """
    Reflects on proposed treatments for safety, practicality, and environmental sustainability.
    """
    prompt = f"""
    You are a Senior Agronomist and Safety Critic evaluating crop disease treatment plans.
    
    Diagnostic Hypothesis: {diagnostic_plan}
    Proposed Treatment Plan: {research_treatment_plan}
    
    Task (Reflection & Refinement):
    1. Evaluate safety for smallholder farmers (dosage, chemical handling, safety equipment).
    2. Ensure biological controls are prioritized where suitable.
    3. Check for any conflicting recommendations.
    4. Provide the FINAL APPROVED advisory response for the farmer.
    """
    response = llm.invoke(prompt)
    return response.content

if __name__ == "__main__":
    test_query = "My chili plant leaves have dark sunken spots on the fruit."
    
    print("\n--- 1. Running Diagnostic Specialist ---")
    diag_res = diagnostic_specialist_agent(test_query)
    print(diag_res)
    
    print("\n--- 2. Running RAG Researcher ---")
    rag_res, docs = rag_researcher_agent(test_query, diag_res)
    print(rag_res)
    
    print("\n--- 3. Running Agronomy Critic ---")
    final_res = agronomy_critic_agent(diag_res, rag_res)
    print(final_res)