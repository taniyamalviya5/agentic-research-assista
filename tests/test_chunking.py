from langchain_core.documents import Document

from app.ingestion.chunking import chunk_documents


def test_chunking_preserves_metadata():
    docs = [Document(page_content="A " * 1000, metadata={"filename": "paper.pdf", "page": 0})]
    chunks = chunk_documents(docs, chunk_size=100, chunk_overlap=20)
    assert len(chunks) > 1
    assert all(c.metadata["filename"] == "paper.pdf" for c in chunks)
    assert all("chunk_id" in c.metadata for c in chunks)
