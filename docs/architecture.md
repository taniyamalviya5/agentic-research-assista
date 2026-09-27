# Architecture and design

## 1. Request lifecycle

1. User submits a question.
2. CrewAI router classifies it as `local`, `web`, or `hybrid`.
3. Local route queries ChromaDB.
4. Web route calls Tavily.
5. Hybrid route executes both.
6. Results are normalized into a common source structure.
7. A grounded Groq prompt generates the answer.
8. Evaluation heuristics calculate quality signals.
9. API returns answer, route, sources and metrics.

## 2. Why this architecture

A deterministic application shell surrounds the agents. This matters because the assignment asks for intelligent agents, but production software still benefits from explicit boundaries, validation and observability.

CrewAI handles agent-oriented routing and can host a multi-agent research crew. LangChain handles document loaders, chunking, embeddings and vector-store integration.

## 3. Data flow

```text
PDF
 |
 | PyPDFLoader
 v
Documents + metadata
 |
 | RecursiveCharacterTextSplitter
 v
Chunks
 |
 | BGE embeddings
 v
ChromaDB
 |
 +---- similarity search ----+
                              |
Query -> CrewAI Router -------+----> Context Aggregator -> Groq -> Answer
                              |
                              +---- Tavily search
```

## 4. Metadata strategy

Every local chunk carries:
- filename
- page
- source_type
- chunk_id

This makes retrieval traceable and allows page-level citations.

## 5. Failure strategy

- Missing Groq key: retrieval still works; generation returns a configuration message.
- Missing Tavily key: web route returns no web results; local route still works.
- CrewAI failure: deterministic heuristic router takes over.
- Empty retrieval: the system refuses to invent an answer.
- Bad PDF: API returns a 422 and removes the uploaded file.

## 6. Production hardening

For production:
- authentication and authorization
- per-user collections
- asynchronous ingestion jobs
- object storage for PDFs
- malware scanning
- rate limiting
- request IDs
- structured logs/traces
- vector index lifecycle management
- evaluation dataset and CI regression tests
- secret manager rather than `.env`
