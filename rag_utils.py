import os
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

# load PDFs and create the vector database
def build_vector_store():
    print("Loading PDFs from knowledge_base...")
    # Load all PDF files inside the knowledge_base folder
    loader = PyPDFDirectoryLoader("knowledge_base")
    documents = loader.load()
    
    # Split large text documents into smaller chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150
    )
    docs = text_splitter.split_documents(documents)
    print(f"Total Chunks Created: {len(docs)}")
    
    # Convert text chunks into numerical vectors (Embeddings)
    print("Creating Embeddings and Vector Store...")
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    # save the vectors into a FAISS vector database
    vector_store = FAISS.from_documents(docs, embeddings)
    
    # Save the FAISS database locally on the machine
    vector_store.save_local("faiss_index")
    print("Vector Store saved successfully to 'faiss_index'!")
    return vector_store

# 4.to retrieve relevant documents for a given query
def get_relevant_docs(query):
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    if os.path.exists("faiss_index"):
        vector_store = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
        retriever = vector_store.as_retriever(search_kwargs={"k": 3})
        return retriever.invoke(query)
    else:
        print("Index not found. Please build vector store first.")
        return []

if __name__ == "__main__":
    # Test Run - Create the vector store for the first time
    build_vector_store()