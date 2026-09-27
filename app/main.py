from pathlib import Path
from uuid import uuid4

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.core.config import get_settings
from app.ingestion.pdf_processor import process_pdf
from app.models.schemas import DocumentInfo, EvaluationRequest, ResearchRequest, ResearchResponse
from app.evaluation.metrics import evaluate
from app.rag.vector_store import add_documents, count_documents
from app.services.research_service import answer_query

settings = get_settings()
settings.ensure_dirs()

app = FastAPI(
    title="Agentic Research Assistant",
    version="1.0.0",
    description="Hybrid local RAG + Tavily web research assistant using CrewAI and LangChain.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
def root():
    return FileResponse("static/index.html")


@app.get("/api/health")
def health():
    return {
        "status": "ok",
        "groq_configured": bool(settings.groq_api_key),
        "tavily_configured": bool(settings.tavily_api_key),
        "vector_chunks": count_documents(),
        "embedding_model": settings.embedding_model,
        "groq_model": settings.groq_model,
    }


@app.get("/api/documents")
def documents():
    upload_dir = Path(settings.upload_dir)
    files = sorted(p.name for p in upload_dir.glob("*.pdf"))
    return {"documents": files, "chunks": count_documents()}


@app.post("/api/documents/upload", response_model=DocumentInfo)
async def upload_document(file: UploadFile = File(...)):
    if not file.filename or not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")

    safe_name = Path(file.filename).name
    target = Path(settings.upload_dir) / f"{uuid4().hex[:8]}_{safe_name}"

    data = await file.read()
    if len(data) > 25 * 1024 * 1024:
        raise HTTPException(status_code=413, detail="PDF exceeds 25 MB limit.")

    target.write_bytes(data)

    try:
        chunks = process_pdf(target, settings.chunk_size, settings.chunk_overlap)
        count = add_documents(chunks)
    except Exception as exc:
        target.unlink(missing_ok=True)
        raise HTTPException(status_code=422, detail=f"Could not process PDF: {exc}") from exc

    return DocumentInfo(filename=safe_name, chunks=count, status="indexed")


@app.post("/api/research", response_model=ResearchResponse)
def research(request: ResearchRequest):
    return answer_query(request.query, request.use_web, request.top_k)


@app.post("/api/evaluate")
def evaluation(request: EvaluationRequest):
    return evaluate(
        query="",
        answer=request.answer,
        contexts=request.context,
        citations=request.citations,
    )
