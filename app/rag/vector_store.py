from functools import lru_cache

from langchain_chroma import Chroma
from langchain_core.documents import Document

from app.core.config import get_settings
from app.rag.embeddings import get_embeddings


@lru_cache
def get_vector_store() -> Chroma:
    settings = get_settings()
    return Chroma(
        collection_name=settings.collection_name,
        embedding_function=get_embeddings(settings.embedding_model),
        persist_directory=settings.chroma_dir,
    )


def add_documents(documents: list[Document]) -> int:
    if not documents:
        return 0
    store = get_vector_store()
    ids = [
        f"{doc.metadata.get('filename', 'unknown')}:"
        f"{doc.metadata.get('page', 0)}:"
        f"{doc.metadata.get('chunk_id', i)}"
        for i, doc in enumerate(documents)
    ]
    store.add_documents(documents, ids=ids)
    return len(documents)


def count_documents() -> int:
    try:
        return get_vector_store()._collection.count()
    except Exception:
        return 0
