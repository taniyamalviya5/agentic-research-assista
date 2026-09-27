# Evaluation and QA

## Metrics

### Retrieval coverage
Fraction of query terms found in retrieved context. This is a lexical diagnostic, not a semantic metric.

### Citation coverage
Fraction of answer sentences containing a source marker.

### Unsupported claim ratio
Fraction of sentences with weak lexical evidence overlap and no citation marker.

### Source diversity
Number of source categories used, e.g. local + web.

## Recommended benchmark

Create 30–100 representative questions:
- factual document questions
- cross-document questions
- current web questions
- ambiguous questions
- impossible/insufficient-evidence questions

For each:
- expected route
- expected evidence
- reference answer
- acceptable citations

Track metrics before and after changes.

## Hallucination controls

1. Retrieval threshold.
2. Grounded system prompt.
3. Inline citations.
4. Explicit insufficient-evidence behavior.
5. Post-generation evaluation.
6. Regression tests.

## Faithfulness

A strong future implementation can add an LLM-as-judge or RAGAS-style evaluator, but judge-based metrics must be validated against human labels.

## Observability

Recommended production fields:
- request_id
- route
- retrieval count
- source URLs
- retrieval scores
- latency by stage
- token usage
- model ID
- evaluation metrics
