from app.evaluation.metrics import citation_coverage, retrieval_coverage


def test_citation_coverage():
    answer = "The model uses attention. [L1] It scales efficiently. [L2]"
    assert citation_coverage(answer, ["L1", "L2"]) == 1.0


def test_retrieval_coverage():
    score = retrieval_coverage("attention mechanism paper", ["The paper describes an attention mechanism."])
    assert score > 0.5
