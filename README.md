## Clinical Research RAG Chatbot (MVP)

This is a minimal but functional Retrieval Augmented Generation (RAG) chatbot for clinical research studies.

The chatbot:
- Loads local clinical research documents (PDF / TXT)
- Chunks and embeds them using OpenAI
- Stores embeddings in a local FAISS index
- Answers questions **only** using retrieved context
- Returns concise answers and the supporting source chunks

---

### Project Structure

```text
backend/
  main.py           # FastAPI app entrypoint
  config.py         # Environment-based configuration
  api/
    chat.py         # /api/chat endpoint
  rag/
    ingest.py       # Ingestion: load → chunk → embed → FAISS
    retriever.py    # FAISS-based retriever
    pipeline.py     # RAG pipeline (retrieve + generate)
  prompts/
    research_prompt.py  # Prompt template & system instructions
  services/
    openai_client.py    # OpenAI embedding + chat clients
  utils/
    chunking.py         # Chunking utilities
    loader.py           # Document loaders (PDF/TXT)
frontend/
  package.json      # Vite + React app
  index.html
  vite.config.ts
  tsconfig.json
  src/
    main.tsx        # Frontend entrypoint
    App.tsx         # Layout shell
    config.ts       # Backend API base URL
    styles.css      # Modern chat UI styling
    components/
      Chat.tsx      # Chat interface + sources panel
data/
  documents/        # Put your input documents here
  faiss_index/      # Saved FAISS index (created by ingestion)
scripts/
  ingest_documents.py   # CLI to build FAISS index
tests/
  __init__.py
requirements.txt
.env.example
README.md
```

---

### Prerequisites

- Python 3.10+ (recommended)
- An OpenAI API key
- (Optional but recommended) Virtual environment (e.g., `venv`)

---

### Setup

#### 1. Clone and navigate

```bash
git clone <your-repo-url>.git
cd medical-research-chatbot
```

#### 2. Create and activate virtual environment

```bash
python -m venv .venv
# Windows (PowerShell)
. .venv/Scripts/Activate.ps1
# macOS/Linux
source .venv/bin/activate
```

#### 3. Install backend dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

#### 4. Configure environment

Copy the example env file and fill in values:

```bash
cp .env.example .env
```

Edit `.env` and set:

- `OPENAI_API_KEY`
- (Optional) `MODEL_NAME`, `EMBEDDING_MODEL`, paths, etc.

---

### Preparing Documents

Place your clinical research documents in:

```text
data/documents/
```

Supported formats (MVP):

- `.pdf`
- `.txt`

You can use subfolders (they will be scanned recursively).

---

### Ingest Documents (Build FAISS Index)

Run the ingestion script once (or whenever documents change):

```bash
python scripts/ingest_documents.py
```

This will:

1. Load all PDF/TXT from `data/documents`
2. Chunk them
3. Create embeddings via OpenAI
4. Build and save a FAISS index to `data/faiss_index`

You can override paths:

```bash
python scripts/ingest_documents.py ^
  --documents-path path\\to\\docs ^
  --index-path path\\to\\index
```

*(On macOS/Linux, replace `^` with `\` or a newline.)*

---

### Run the FastAPI Server

Start the API (development):

```bash
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:

- Base: `http://localhost:8000`
- Health check: `http://localhost:8000/health`
- Chat endpoint: `POST http://localhost:8000/api/chat`

---

### API Usage

#### Endpoint

`POST /api/chat`

#### Request body

```json
{
  "question": "What are the side effects of treatment X?"
}
```

#### Example (curl, Windows PowerShell)

```bash
curl -X POST "http://localhost:8000/api/chat" ^
  -H "Content-Type: application/json" ^
  -d "{\"question\": \"What are the side effects of treatment X?\"}"
```

#### Response

```json
{
  "answer": "The most frequently reported side effects of treatment X are ... (Source 1).",
  "sources": [
    {
      "label": "Source 1",
      "text": "Chunked text from the relevant document...",
      "metadata": {
        "source": "data/documents/study_001.pdf",
        "page": 3
      }
    },
    {
      "label": "Source 2",
      "text": "Another supporting chunk...",
      "metadata": {
        "source": "data/documents/study_002.pdf",
        "page": 1
      }
    }
  ]
}
```

---

### Behavior & Safety

- The model is **instructed to answer only from the provided context**.
- If the answer is not present in the retrieved chunks, it should respond:
  > `"I could not find information in the documents."`
- A post-check in the pipeline further guards against hallucinations by returning the above message when the model refuses or returns an empty / irrelevant answer.

---

### Frontend (React + Vite)

A minimal, modern-styled chat UI is included under `frontend/`.

#### 1. Install frontend dependencies

```bash
cd frontend
npm install
```

#### 2. Configure backend URL (optional)

By default, the frontend calls `http://localhost:8000`:

- See `frontend/src/config.ts`.
- To override for different environments (e.g., Vercel deployment), set:

```bash
VITE_API_BASE_URL=https://your-backend-domain
```

in a `frontend/.env` file or in your Vercel project environment settings.

#### 3. Run frontend locally

In one terminal, run the backend as above. In another:

```bash
cd frontend
npm run dev
```

Open the URL printed in the console (typically `http://localhost:5173`).

You will see:

- A chat panel where you can ask questions about your ingested clinical documents.
- A sources panel that shows the chunks used for the most recent answer.

---

### Extensibility

The codebase is intentionally simple and modular:

- Add new loaders in `backend/utils/loader.py` (e.g., DOCX, HTML).
- Tune chunk sizes in `backend/utils/chunking.py`.
- Adjust retrieval `TOP_K` via `.env`.
- Customize prompt behavior in `backend/prompts/research_prompt.py`.
- Add more endpoints under `backend/api/`.

This should be sufficient as an MVP for a clinical research study chatbot, and can be iterated on without major refactors.

