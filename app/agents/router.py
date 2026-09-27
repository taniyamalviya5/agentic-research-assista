import json
import re
from dataclasses import dataclass

from app.core.config import get_settings


@dataclass
class RouteDecision:
    route: str
    summary: str


def heuristic_route(query: str, use_web: bool = True) -> RouteDecision:
    q = query.lower()
    current_markers = [
        "today", "latest", "current", "recent", "news", "2026", "price",
        "release", "version", "this week", "now",
    ]
    if use_web and any(marker in q for marker in current_markers):
        return RouteDecision("web", "The query contains a current-information signal.")
    if use_web and any(marker in q for marker in ["compare", "outside the paper", "industry", "other research"]):
        return RouteDecision("hybrid", "The query asks for information that can benefit from external sources.")
    return RouteDecision("local", "The query is primarily document-grounded.")


def crewai_route(query: str, use_web: bool) -> RouteDecision | None:
    """CrewAI-based router.

    CrewAI is deliberately isolated behind this function so the core application
    remains testable and can fall back to deterministic routing.
    """
    settings = get_settings()
    if not settings.groq_api_key:
        return None

    try:
        from crewai import Agent, Crew, Process, Task
        from langchain_groq import ChatGroq

        llm = ChatGroq(
            api_key=settings.groq_api_key,
            model=settings.groq_model,
            temperature=0,
        )

        router = Agent(
            role="Research Source Router",
            goal="Select local, web, or hybrid information sources for a research query.",
            backstory=(
                "You are a routing specialist. You do not answer the question. "
                "You classify the source strategy and return compact JSON."
            ),
            llm=llm,
            allow_delegation=False,
            verbose=False,
        )

        task = Task(
            description=(
                "Classify this query into exactly one route: local, web, hybrid. "
                f"Web is allowed: {use_web}. Query: {query}\n"
                'Return JSON only: {"route":"local|web|hybrid","summary":"short reason"}'
            ),
            expected_output='{"route":"local|web|hybrid","summary":"short reason"}',
            agent=router,
        )

        crew = Crew(
            agents=[router],
            tasks=[task],
            process=Process.sequential,
            verbose=False,
        )
        raw = str(crew.kickoff()).strip()
        match = re.search(r"\{.*\}", raw, re.DOTALL)
        if not match:
            return None
        data = json.loads(match.group(0))
        route = data.get("route")
        if route not in {"local", "web", "hybrid"}:
            return None
        if route in {"web", "hybrid"} and not use_web:
            route = "local"
        return RouteDecision(route, data.get("summary", "CrewAI route selected."))
    except Exception:
        return None


def route_query(query: str, use_web: bool = True) -> RouteDecision:
    return crewai_route(query, use_web) or heuristic_route(query, use_web)
