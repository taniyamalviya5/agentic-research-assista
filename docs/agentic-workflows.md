# Milestone 4 — Agentic Workflows and Multi-Agent Systems

## Agents vs chains

A chain follows a mostly predetermined sequence.

An agent can:
- choose tools
- decide which action to take
- adapt based on tool results
- delegate work

This project uses an agent for routing, while keeping retrieval and response generation bounded.

## CrewAI

CrewAI provides role-based agents, tasks and crews. The project uses:
- Router Agent
- Research Analyst
- Evidence Critic

The multi-agent crew is isolated in `app/agents/research_crew.py`.

## Roles and responsibilities

### Router Agent
Determines whether the question should use local documents, web search, or both.

### Research Analyst
Extracts supported findings from retrieved evidence.

### Evidence Critic
Checks whether proposed findings are supported and flags citation gaps.

## Planning and execution

A safe research workflow is:

```text
PLAN
  -> classify source
  -> retrieve
  -> normalize
  -> synthesize
  -> validate
  -> respond
```

Each step has a clear contract.

## Multi-agent collaboration

A sequential crew can pass the research analyst output to the evidence critic. For higher scale, agents can run in parallel on independent subtasks and a final synthesizer can merge the results.

## LangChain + CrewAI integration

The libraries have different responsibilities:
- LangChain: document/RAG plumbing
- CrewAI: agent orchestration
- Groq: model inference
- Tavily: web retrieval
- ChromaDB: vector storage

This separation keeps components replaceable.

## Determinism vs autonomy

Autonomy is not automatically better. Use agents where the decision is open-ended. Use explicit functions for security-sensitive or compliance-sensitive operations.
