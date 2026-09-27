from app.agents.router import route_query
from app.core.config import get_settings
from app.evaluation.metrics import evaluate
from app.llm.groq_client import chat
from app.models.schemas import ResearchResponse, Source
from app.rag.retriever import search_local
from app.search.tavily_client import search_web


def _local_context(chunks):
    sources = []
    context_parts = []
    for i, item in enumerate(chunks, start=1):
        label = f"L{i}"
        page = item.metadata.get("page")
        filename = item.metadata.get("filename", "local document")
        title = f"{filename} (page {int(page) + 1})" if page is not None else filename
        context_parts.append(f"[{label}] {item.content}")
        sources.append(
            Source(
                id=label,
                source_type="local",
                title=title,
                page=(int(page) + 1 if page is not None else None),
                score=round(item.score, 4),
                snippet=item.content[:350].replace("\n", " "),
            )
        )
    return context_parts, sources


def _web_context(results):
    context_parts = []
    sources = []
    for i, result in enumerate(results, start=1):
        label = f"W{i}"
        title = result.get("title") or result.get("url") or "Web result"
        content = result.get("content") or result.get("snippet") or ""
        context_parts.append(f"[{label}] {title}\n{content}")
        sources.append(
            Source(
                id=label,
                source_type="web",
                title=title,
                url=result.get("url"),
                score=float(result.get("score", 0.0) or 0.0),
                snippet=content[:350].replace("\n", " "),
            )
        )
    return context_parts, sources


def answer_query(query: str, use_web: bool = True, top_k: int = 5) -> ResearchResponse:
    settings = get_settings()
    decision = route_query(query, use_web)

    local_chunks = []
    web_results = []

    if decision.route in {"local", "hybrid"}:
        local_chunks = search_local(query, k=top_k)

    if decision.route in {"web", "hybrid"}:
        web_results = search_web(query, settings.tavily_max_results)

    local_context, local_sources = _local_context(local_chunks)
    web_context, web_sources = _web_context(web_results)

    contexts = local_context + web_context
    sources = local_sources + web_sources

    if not contexts:
        answer = (
            "I could not retrieve supporting evidence from the configured sources. "
            "Upload a PDF or configure Tavily/Groq and try again."
        )
        metrics = evaluate(query, answer, [], [])
        return ResearchResponse(
            answer=answer,
            route=decision.route,
            reasoning_summary=decision.summary,
            sources=[],
            metrics=metrics,
        )

    context_text = "\n\n".join(contexts)
    system_prompt = """You are an evidence-grounded research assistant.

Rules:
- Answer the user's question using only the supplied evidence.
- Do not invent facts, citations, papers, URLs, or page numbers.
- Put [Lx] after claims supported by local document chunks.
- Put [Wx] after claims supported by web results.
- If evidence conflicts, state the conflict and identify the sources.
- If evidence is insufficient, say so explicitly.
- Give a concise, technically useful answer with headings when appropriate.
- Do not expose hidden chain-of-thought. Provide only a short reasoning summary if asked.
"""

    user_prompt = f"""Question:
{query}

Evidence:
{context_text}

Write the final answer with inline source markers such as [L1] or [W2].
"""

    answer = chat(system_prompt, user_prompt)

    citation_ids = [s.id for s in sources]
    metrics = evaluate(query, answer, [s for s in contexts], citation_ids)

    return ResearchResponse(
        answer=answer,
        route=decision.route,
        reasoning_summary=decision.summary,
        sources=sources,
        metrics=metrics,
    )
