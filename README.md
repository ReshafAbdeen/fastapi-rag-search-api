# RAG Search API

A simple Retrieval-Augmented Generation (RAG) pipeline exposed as a REST API using **FastAPI**. It loads documents from a local folder, embeds them using **Sentence Transformers**, stores the embeddings in a **FAISS** vector index, and uses **Google Gemini** to generate a summarized answer for a given query based on the most relevant retrieved chunks.

## Features

- Loads and parses multiple document formats: PDF, TXT, CSV, Excel (`.xlsx`), Word (`.docx`), and JSON.
- Splits documents into overlapping chunks for better retrieval quality.
- Generates embeddings using the `all-MiniLM-L6-v2` Sentence Transformer model.
- Stores and searches embeddings using a FAISS vector index (`IndexFlatL2`).
- Persists the FAISS index and metadata to disk so it doesn't need to be rebuilt on every restart.
- Uses Google's Gemini model (via `langchain-google-genai`) to summarize retrieved context for a user's query.
- Exposes a simple REST API (`/search`) built with FastAPI, with interactive docs at `/docs`.

## Project Structure

```
.
├── main.py               # FastAPI app and API endpoints
├── src/
│   ├── search.py         # RAGSearch: orchestrates retrieval + summarization
│   ├── vectorstore.py     # FaissVectorStore: build/save/load/query the FAISS index
│   ├── embedding.py       # EmbeddingPipeline: chunking + embedding generation
│   └── data_loader.py     # load_all_documents: reads files from the data/ folder
├── data/                  # Put your source documents here (PDF, TXT, CSV, XLSX, DOCX, JSON)
├── faiss_store/           # Auto-generated: stores the FAISS index and metadata
├── .env                   # Environment variables (API keys) — not committed to git
└── requirements.txt       # Python dependencies
```

## How It Works

1. On startup, `RAGSearch` checks whether a FAISS index already exists in `faiss_store/`.
   - If not, it loads all documents from the `data/` folder, splits them into chunks, generates embeddings, and builds a new FAISS index.
   - If it exists, it simply loads the saved index and metadata.
2. When a search request comes in, the query is embedded and the FAISS index is searched for the most relevant chunks.
3. The retrieved chunks are passed as context to the Gemini model, which generates a summarized answer for the original query.

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/ReshafAbdeen/fastapi-rag-search-api.git
cd fastapi-rag-search-api
```

### 2. Create a virtual environment and install dependencies

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
```

### 3. Set up environment variables

Create a `.env` file in the project root with your Gemini API key:

```
GEMINI_API_KEY=your_api_key_here
```

### 4. Add your documents

Place any PDF, TXT, CSV, XLSX, DOCX, or JSON files you want to search inside the `data/` folder. On the first run, the app will automatically build the FAISS index from these files.

### 5. Run the server

```bash
uvicorn main:app --reload
```

The API will be available at `http://127.0.0.1:8000`.

Interactive API documentation (Swagger UI) is available at:

```
http://127.0.0.1:8000/docs
```

## API Usage

### `GET /`

Health check endpoint.

**Response:**
```json
{ "message": "Welcome to RAG Search API!" }
```

### `POST /search`

Searches the indexed documents and returns a summarized answer for the given query.

**Request body:**
```json
{
  "query": "What is Artificial Intelligence?",
  "top_k": 3
}
```

**Response:**
```json
{
  "query": "What is Artificial Intelligence?",
  "summary": "Based on the provided context, Artificial Intelligence (AI) refers to..."
}
```

## Notes

- The embedding model (`all-MiniLM-L6-v2`) is loaded once at startup, so it won't slow down individual requests.
- If you change or add documents in the `data/` folder, delete the `faiss_store/` folder to force a rebuild of the index on the next run.
- Make sure your Gemini model name (in `search.py`) is a currently supported model — Google periodically deprecates older model versions.

## License

This project is open for personal and educational use. Add your preferred license here (e.g., MIT).