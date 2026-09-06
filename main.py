from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.search import RAGSearch

# 1. FastAPI App initialize karein
app = FastAPI(title="RAG Search API", version="1.0")

#RAG Search Engine load karein
rag_engine = RAGSearch()

#Request Body ka schema define karein
class QueryRequest(BaseModel):
    query: str
    top_k: int = 3

#API Endpoints
@app.get("/")
def home():
    return {"message": "Welcome to RAG Search API!"}

@app.post("/search")
def search_documents(request: QueryRequest):
    if not request.query.strip():
        raise HTTPException(status_code=400, detail="Query string cannot be empty")
    
    try:
        summary = rag_engine.search_and_summarize(request.query, top_ki=request.top_k)
        return {
            "query": request.query,
            "summary": summary
        }
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))