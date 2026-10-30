from typing import Literal
from pydantic import BaseModel, Field, HttpUrl

class ResearchRequest(BaseModel):
    question: str = Field(min_length=8, max_length=1500)

class ResearchRequirement(BaseModel):
    id: str
    description: str
    priority: Literal["critical", "high", "optional"] = "high"
    expected_evidence: str

class ResearchPlan(BaseModel):
    objective: str
    requirements: list[ResearchRequirement]
    search_queries: list[str] = Field(min_length=1, max_length=8)
    tools_to_use: list[Literal["tavily_search", "tavily_extract"]]
    assumptions: list[str] = []

class Source(BaseModel):
    source_id: str
    title: str
    url: str
    domain: str = ""
    snippet: str = ""

class Evidence(BaseModel):
    requirement_id: str
    source_id: str
    entity: str = ""
    evidence: str
    relevance: Literal["high", "medium", "low"] = "medium"

class RequirementAssessment(BaseModel):
    requirement_id: str
    status: Literal["met", "partial", "missing"]
    explanation: str

class EvidenceEvaluation(BaseModel):
    assessments: list[RequirementAssessment]
    contradictions: list[str] = []
    weak_sources: list[str] = []
    recovery_queries: list[str] = Field(default_factory=list, max_length=4)
    overall_assessment: str

class KeyFinding(BaseModel):
    heading: str
    detail: str
    supporting_source_ids: list[str] = []

class FinalReport(BaseModel):
    user_question: str
    short_answer: str
    key_findings: list[KeyFinding]
    sources: list[Source]
    confidence: Literal["high", "medium", "low"]
    confidence_reason: str
    limitations_assumptions: list[str]
    next_steps: list[str]
