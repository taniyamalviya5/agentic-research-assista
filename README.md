# Agentic Research Assistant — C16 Basic

A complete reference implementation for the **"Building an Intelligent Agentic Research Assistant"** use case in the supplied RTB (C16) requirements.

## What is implemented

- PDF ingestion and text extraction
- Recursive + metadata-aware chunking
- Local embeddings using `BAAI/bge-small-en-v1.5`
- Persistent ChromaDB vector store
- CrewAI router agent for source selection
- Deterministic routing fallback when LLM credentials are unavailable
- Local RAG retrieval with similarity scores
- Tavily web search integration
- Multi-source aggregation
- Groq LLM response generation
- Context-grounded prompting with citations
- Basic retrieval/faithfulness/hallucination-oriented evaluation
- FastAPI REST API
- Lightweight browser UI
- Unit tests
- Docker support
- Architecture and learning documentation covering Milestones 3 and 4

## Important 2026 model note

The original assignment names Groq Llama 3 8B. Groq has since deprecated the older `llama3-8b-8192` model, and later `llama-3.1-8b-instant` was also scheduled for decommissioning in 2026. The project therefore defaults to a currently supported Groq model through `GROQ_MODEL`, while keeping the model configurable. This preserves the assignment's Groq requirement without hard-coding a retired model.

## Architecture

```text
                         +----------------------+
                         |      Browser UI       |
                         +----------+-----------+
                                    |
                                    v
                         +----------------------+
                         |      FastAPI API     |
                         +----------+-----------+
                                    |
                                    v
                         +----------------------+
                         |   Research Service   |
                         +----+------------+----+
                              |            |
                    +---------+--+      +--+----------+
                    | CrewAI     |      | Query       |
                    | Router     |      | Classifier  |
                    +------+-----+      +------+-------+
                           |                   |
                 +---------+-------------------+---------+
                 |                                     |
                 v                                     v
       +--------------------+                 +-------------------+
       | ChromaDB + BGE     |                 | Tavily Web Search |
       | local document RAG |                 | current knowledge |
       +---------+----------+                 +---------+---------+
                 |                                      |
                 +------------------+-------------------+
                                    |
                                    v
                         +----------------------+
                         | Context Aggregator   |
                         +----------+-----------+
                                    |
                                    v
                         +----------------------+
                         | Groq Response Agent  |
                         +----------+-----------+
                                    |
                                    v
                         Answer + source list
```

## Assignment mapping

| Requirement | Implementation |
|---|---|
| PDF ingestion | `app/ingestion/pdf_processor.py` |
| BAAI/bge-small-en-v1.5 | `app/rag/embeddings.py` |
| ChromaDB | `app/rag/vector_store.py` |
| Chunking/indexing | `app/ingestion/chunking.py` |
| CrewAI router | `app/agents/router.py` |
| Source selection | `app/services/research_service.py` |
| Vector retrieval | `app/rag/retriever.py` |
| Tavily search | `app/search/tavily_client.py` |
| Ranking | local similarity + source scoring |
| Multi-source aggregation | `app/services/research_service.py` |
| Groq LLM | `app/llm/groq_client.py` |
| Context-aware generation | grounded system prompt |
| Response structure | Pydantic schemas |
| Evaluation | `app/evaluation/metrics.py` |
| API | `app/main.py` |
| UI | `static/` |
| Tests | `tests/` |

## Quick start

### 1. Prerequisites

- Python 3.11+
- Git
- Optional: Docker
- A Groq API key for generation
- A Tavily API key for web search

### 2. Create environment

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
```

### 3. Configure keys

```bash
copy .env.example .env
```

Set:

```env
GROQ_API_KEY=...
TAVILY_API_KEY=...
```

The app works in local-only mode without Tavily, and the router has a deterministic fallback without Groq.

### 4. Start

```bash
uvicorn app.main:app --reload
```

Open:

```text
http://127.0.0.1:8000
```

### 5. Upload a PDF

Use the UI or:

```bash
curl -X POST "http://127.0.0.1:8000/api/documents/upload" \
  -F "file=@your-paper.pdf"
```

### 6. Ask a question

```bash
curl -X POST "http://127.0.0.1:8000/api/research" \
  -H "Content-Type: application/json" \
  -d '{"query":"What problem does the paper solve and what is its key contribution?","use_web":true}'
```

## API

- `GET /api/health`
- `POST /api/documents/upload`
- `GET /api/documents`
- `POST /api/research`
- `POST /api/evaluate`

OpenAPI docs are available at `/docs`.

## Quality controls

The response generator is instructed to:
1. Use supplied context only for factual claims.
2. Cite local chunks as `[L1]`, `[L2]`, etc.
3. Cite web results as `[W1]`, `[W2]`, etc.
4. Explicitly say when evidence is insufficient.
5. Avoid fabricating references.

The evaluator reports:
- retrieval coverage
- citation coverage
- unsupported-claim ratio heuristic
- source diversity
- context utilization

These are intentionally transparent heuristics, not a replacement for a benchmark such as RAGAS.

## Security notes

- Never commit `.env`.
- API keys are loaded from environment variables.
- Uploaded files are stored under `data/uploads`.
- The app does not execute uploaded PDF content.
- Web results are treated as untrusted external context.
- In production, add authentication, file-size limits, malware scanning, rate limiting and structured audit logging.

## Tests

```bash
pytest -q
```

## Docker

```bash
docker compose up --build
```

## Learning material

Read:
- `docs/architecture.md`
- `docs/rag-and-prompt-engineering.md`
- `docs/agentic-workflows.md`
- `docs/evaluation.md`
- `docs/demo-script.md`
