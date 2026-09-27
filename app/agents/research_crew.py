"""Optional multi-agent CrewAI layer.

This module demonstrates the Milestone-4 pattern without making the entire
application dependent on an autonomous crew. The main service remains
deterministic and auditable; this crew can be used for a richer final synthesis.
"""

from app.core.config import get_settings


def build_research_crew():
    settings = get_settings()
    if not settings.groq_api_key:
        return None

    from crewai import Agent, Crew, Process, Task
    from langchain_groq import ChatGroq

    llm = ChatGroq(
        api_key=settings.groq_api_key,
        model=settings.groq_model,
        temperature=0.1,
    )

    researcher = Agent(
        role="Research Analyst",
        goal="Analyze supplied research evidence and identify supported findings.",
        backstory="You are careful about evidence, citations, uncertainty, and source quality.",
        llm=llm,
        allow_delegation=False,
        verbose=False,
    )
    critic = Agent(
        role="Evidence Critic",
        goal="Check whether conclusions are supported by the supplied evidence.",
        backstory="You challenge unsupported claims and identify missing evidence.",
        llm=llm,
        allow_delegation=False,
        verbose=False,
    )

    return Crew(
        agents=[researcher, critic],
        tasks=[
            Task(
                description="Analyze the evidence and extract the key supported findings.",
                expected_output="A concise evidence summary with explicit uncertainty.",
                agent=researcher,
            ),
            Task(
                description="Critique the findings for unsupported claims or citation gaps.",
                expected_output="A short quality review and corrections.",
                agent=critic,
            ),
        ],
        process=Process.sequential,
        verbose=False,
    )
