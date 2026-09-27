# 7–10 minute demo script

## 1. Explain the problem
"Users have research papers locally, but current information may require the web. The assistant routes the question to the appropriate source and grounds the response."

## 2. Show architecture
Explain:
- FastAPI
- CrewAI router
- ChromaDB
- BGE embeddings
- Tavily
- Groq

## 3. Upload a PDF
Upload the supplied research paper if available. Show the indexed chunk count.

## 4. Ask a local question
Example:
"What is the key contribution of this paper?"

Expected route: local.

Show `[L1]` citations and page information.

## 5. Ask a current question
Example:
"What are the latest developments related to this topic?"

Expected route: web.

Show Tavily URLs.

## 6. Ask a hybrid question
Example:
"Compare the paper's approach with recent external work."

Expected route: hybrid.

## 7. Explain quality
Show:
- retrieval coverage
- citation coverage
- unsupported-claim heuristic
- source diversity

## 8. Explain agentic behavior
Show the CrewAI router and multi-agent research crew.

## 9. Explain engineering quality
Mention:
- tests
- environment configuration
- failure handling
- separation of concerns
- Docker support
