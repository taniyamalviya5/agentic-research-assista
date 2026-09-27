from functools import lru_cache

from app.core.config import get_settings


@lru_cache
def get_tavily_client():
    settings = get_settings()
    if not settings.tavily_api_key:
        return None
    from tavily import TavilyClient
    return TavilyClient(api_key=settings.tavily_api_key)


def search_web(query: str, max_results: int | None = None) -> list[dict]:
    settings = get_settings()
    client = get_tavily_client()
    if client is None:
        return []

    response = client.search(
        query=query,
        max_results=max_results or settings.tavily_max_results,
        search_depth="advanced",
        include_answer=False,
        include_raw_content=False,
    )
    return response.get("results", [])
