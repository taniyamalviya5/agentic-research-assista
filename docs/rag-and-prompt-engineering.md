# Milestone 3 — Prompt Engineering and RAG

## Prompt engineering foundations

A strong production prompt normally has:
1. Role
2. Objective
3. Constraints
4. Evidence/context
5. Output contract
6. Failure behavior

Example:

```text
ROLE
You are an evidence-grounded research assistant.

OBJECTIVE
Answer the question using only supplied evidence.

CONSTRAINTS
Do not invent facts, URLs, page numbers or references.

EVIDENCE
[L1] ...
[W1] ...

OUTPUT
Concise answer with inline [Lx]/[Wx] citations.
```

## Chain-of-thought

The system should not ask the model to expose private chain-of-thought. Instead, use concise reasoning summaries, explicit intermediate artifacts, tool traces, and citations that can be audited.

## ReAct

ReAct-style agents interleave reasoning with actions/tools. In this project, the conceptual loop is:

```text
Question -> route -> retrieve -> inspect evidence -> answer
```

The implementation keeps tool execution bounded and auditable instead of allowing unrestricted autonomous loops.

## Tree-of-thought

Tree-of-thought is useful when multiple candidate approaches must be explored. For this basic research assistant, a full branching search would add cost and complexity. A practical extension is to create multiple query rewrites, retrieve each, then rerank the union.

## Retrieval-augmented prompting

RAG separates:
- retrieval: find evidence
- generation: explain evidence

This reduces reliance on model parametric memory for document-specific questions.

## Chunking

Current defaults:
- chunk size: 900 characters
- overlap: 150 characters

Why overlap? It reduces the probability that an important sentence split at a boundary loses context.

## Recursive chunking

The splitter prefers paragraph and line boundaries before falling back to sentence and character boundaries.

## Metadata-aware retrieval

Metadata is attached to each chunk so answers can identify filename/page.

## Vector store

ChromaDB stores embeddings and supports similarity retrieval.

## Query routing

The router chooses:
- local: document-specific questions
- web: current/external questions
- hybrid: questions requiring both

This is a policy, not a claim that one source is always correct.

## Evaluation

The project exposes:
- retrieval coverage
- citation coverage
- unsupported-claim ratio heuristic
- source diversity

For serious evaluation, build a gold dataset of questions, expected evidence chunks and reference answers, then compare changes in CI.
