from dataclasses import dataclass

from app.core.config import get_settings
from app.rag.vector_store import get_vector_store


@dataclass
class RetrievedChunk:
    content: str
    metadata: dict
    score: float


def search_local(query: str, k: int | None = None) -> list[RetrievedChunk]:
    settings = get_settings()
    k = k or settings.top_k
    results = get_vector_store().similarity_search_with_relevance_scores(query, k=k)

    retrieved: list[RetrievedChunk] = []
    for doc, score in results:
        if score < settings.min_relevance:
            continue
        retrieved.append(
            RetrievedChunk(
                content=doc.page_content,
                metadata=doc.metadata,
                score=float(score),
            )
        )
    return retrieved
