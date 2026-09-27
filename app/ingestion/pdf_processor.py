from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document

from app.ingestion.chunking import chunk_documents


def load_pdf(path: str | Path) -> list[Document]:
    loader = PyPDFLoader(str(path))
    return loader.load()


def process_pdf(
    path: str | Path,
    chunk_size: int,
    chunk_overlap: int,
) -> list[Document]:
    docs = load_pdf(path)
    chunks = chunk_documents(docs, chunk_size, chunk_overlap)
    for chunk in chunks:
        chunk.metadata["source_type"] = "local"
        chunk.metadata["filename"] = Path(path).name
    return chunks
