import re

def _tokens(text: str) -> set[str]:
    return set(re.findall(r"\b[a-zA-Z0-9]{3,}\b", text.lower()))


def retrieval_coverage(query: str, contexts: list[str]) -> float:
    q = _tokens(query)
    if not q:
        return 0.0
    ctx = _tokens(" ".join(contexts))
    return round(len(q & ctx) / len(q), 3)


def citation_coverage(answer: str, citations: list[str]) -> float:
    if not answer.strip():
        return 0.0
    normalized = re.sub(r"\s+(?=\[(?:L|W)\d+\])", "", answer)
    sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+", normalized) if s.strip()]
    if not sentences:
        return 0.0
    cited = sum(1 for sentence in sentences if re.search(r"\[(?:L|W)\d+\]", sentence))
    return round(cited / len(sentences), 3)


def unsupported_claim_ratio(answer: str, contexts: list[str]) -> float:
    """Transparent lexical heuristic.

    This is not a semantic truth metric. It flags answer sentences that have
    little lexical overlap with retrieved evidence and therefore deserve review.
    """
    context_tokens = _tokens(" ".join(contexts))
    normalized = re.sub(r"\s+(?=\[(?:L|W)\d+\])", "", answer)
    sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+", normalized) if s.strip()]
    if not sentences:
        return 0.0
    unsupported = 0
    for sentence in sentences:
        tokens = _tokens(sentence)
        overlap = len(tokens & context_tokens) / max(len(tokens), 1)
        if overlap < 0.08 and not re.search(r"\[(?:L|W)\d+\]", sentence):
            unsupported += 1
    return round(unsupported / len(sentences), 3)


def source_diversity(citations: list[str]) -> int:
    """Count distinct source families represented by citation IDs (L/W)."""
    families = {c[0] for c in citations if c and c[0] in {"L", "W"}}
    return len(families)


def evaluate(query: str, answer: str, contexts: list[str], citations: list[str]) -> dict:
    return {
        "retrieval_coverage": retrieval_coverage(query, contexts),
        "citation_coverage": citation_coverage(answer, citations),
        "unsupported_claim_ratio": unsupported_claim_ratio(answer, contexts),
        "source_diversity": source_diversity(citations),
        "context_items": len(contexts),
    }
