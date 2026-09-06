import os 
import time
from dotenv import load_dotenv
from src.vectorstore import FaissVectorStore
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

class RAGSearch:
    def __init__(self, persist_dir: str = "faiss_store", embedding_model: str = "all-MiniLM-L6-v2", llm_model: str = "gemini-3.6-flash"):
        self.vectorstore = FaissVectorStore(persist_dir, embedding_model)

        #Load or build vectorstore
        faiss_path = os.path.join(persist_dir, "faiss.index")
        meta_path = os.path.join(persist_dir, "metadata.pkl")

        if not (os.path.exists(faiss_path) and os.path.exists(meta_path)):
            from data_loader import load_all_documents
            docs = load_all_documents("data")
            self.vectorstore.build_from_document(docs)

        else:
            self.vectorstore.load()

        google_api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
        self.llm = ChatGoogleGenerativeAI(google_api_key=google_api_key, model=llm_model)
        print(f"[INFO] Google LLM Initialize: {llm_model}")

    def search_and_summarize(self, query: str, top_ki: int =5) -> str:
        t0 = time.time()

        results = self.vectorstore.query(query, top_ki=top_ki)
        texts = []

        # Extract text properly from results
        for r in results:
            if isinstance(r, dict):
                meta = r.get("metadata", {})
                if isinstance(meta, dict) and "text" in meta:
                    texts.append(meta["text"])

        context = "\n\n".join(texts)
        if not context:
            return "No relevant document found."
        
        prompt = f"""Summarize the followring context for the query: '{query}'\n\nContext:\n{context}\n\nSummary"""

        t2 = time.time()
        response = self.llm.invoke(prompt)
        t3 = time.time()

        if isinstance(response.content, list):
            return response.content[0].get("text", "") if isinstance(response.content[0], dict) else str(response.content[0])

        
        return response.content

