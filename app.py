from src.data_loader import load_all_documents
from src.vectorstore import FaissVectorStore
from src.search import RAGSearch

if __name__ == "__main__":
    print("[INFO] Rebuilding FAISS Index ...")
    docs = load_all_documents("data")
    
    store = FaissVectorStore("faiss_store")
    store.build_from_document(docs)  # Is line se actual text embed ho kar save hoga!

    # Query Search
    rag_search = RAGSearch(llm_model="gemini-3.6-flash")
    query = "What is Artificial Intelligence?"

    summary = rag_search.search_and_summarize(query, top_ki=3)
    print("\n----Summary Output----")
    print("\nSummary:\n", summary)