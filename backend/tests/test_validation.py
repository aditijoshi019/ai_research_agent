from app.schemas import ResearchRequest, FinalReport

def test_research_request_rejects_short_question():
    try:
        ResearchRequest(question="short")
        assert False, "Expected validation error"
    except Exception:
        assert True

def test_final_report_schema():
    report = FinalReport(
        user_question="Compare two databases",
        short_answer="A concise answer.",
        key_findings=[],
        sources=[],
        confidence="low",
        confidence_reason="No evidence was retrieved.",
        limitations_assumptions=["Insufficient sources"],
        next_steps=["Retry with focused queries"],
    )
    assert report.confidence == "low"
