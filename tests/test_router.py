from app.agents.router import heuristic_route


def test_current_question_goes_web():
    decision = heuristic_route("What is the latest version?", use_web=True)
    assert decision.route == "web"


def test_document_question_goes_local():
    decision = heuristic_route("What is the key contribution of the paper?", use_web=True)
    assert decision.route == "local"


def test_hybrid_question():
    decision = heuristic_route("Compare the paper with other research", use_web=True)
    assert decision.route == "hybrid"
