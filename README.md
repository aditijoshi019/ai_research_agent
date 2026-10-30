# AI Research Agent

A focused, single-agent research workflow built with FastAPI, LangGraph, Groq, Tavily Search, and Tavily Extract.

## Features
- LLM-generated research plan with question-specific requirements and queries.
- Two research tools: Tavily Search and Tavily Extract.
- Source filtering and deduplication.
- Evidence evaluation against dynamic requirements.
- One conditional recovery round for critical/high-priority gaps.
- Structured report with sources, confidence, limitations, and next steps.
- Visible execution trace in the React UI.
- Basic validation, timeouts/retries from clients, logging, and error handling.

## Architecture

`Question -> Planner -> Plan validation -> Tavily Search -> Filter sources -> Tavily Extract -> Build evidence -> LLM evaluator -> Conditional recovery -> Synthesizer -> Pydantic validation -> Report`

LangGraph manages state and conditional routing. Python controls the recovery budget and validates output. The LLM does semantic planning, evidence assessment, and synthesis.

## Requirements
- Python 3.10+
- Node.js 18+
- Groq API key
- Tavily API key

## Backend setup
```bash
cd backend
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate
pip install -r requirements.txt
copy .env.example .env
# On macOS/Linux use: cp .env.example .env
```
Add `GROQ_API_KEY` and `TAVILY_API_KEY` to `backend/.env`.

Run:
```bash
uvicorn app.main:app --reload
```
API docs: http://localhost:8000/docs

## Frontend setup
```bash
cd frontend
npm install
npm run dev
```
Open http://localhost:5173.

## API
`POST /api/research`
```json
{"question":"Compare the top 3 open-source vector databases for a startup building RAG products."}
```

## Important design decisions and limitations
- Search fan-out is concurrent, but each query can produce an individual Tavily HTTP request. One LangGraph node is not necessarily one provider request.
- Tavily Extract accepts a URL list; extraction falls back to individual URLs if the batch request fails.
- One recovery round is allowed to control latency and cost.
- The evaluator is an LLM judge, not ground truth. Its output is schema-validated and its decisions are bounded by deterministic Python routing.
- Evidence snippets are bounded to control prompt size. A production version should chunk long pages and preserve exact quoted spans.
- Search ranking and source reliability are imperfect. A production version should add domain policies, freshness checks, source diversity, and stronger citation-span verification.
- Web pages are untrusted input. The prompts explicitly treat page text as data, not instructions; stronger deployments should add content isolation and URL/SSRF controls.
- Add LangSmith or OpenTelemetry tracing, caching, rate limits, authentication, persistent graph checkpoints, and background jobs before production deployment.
- The sample CORS origin is localhost only. Restrict it to the deployed frontend domain.

## Evaluation plan
Run at least these five questions and record expected behavior, observed output, sources, confidence, latency, and failures:
1. Compare three open-source vector databases for a startup building RAG products.
2. Find five Indian B2B SaaS startups in HR tech and summarize positioning.
3. Explain pros and cons of multi-agent architecture for customer support automation.
4. Compare approaches to adding memory in an AI support agent.
5. Ask a narrow question where credible sources are scarce; the agent should return low confidence and explain the gap.

Suggested metrics:
- Requirement coverage: met / partial / missing per planner requirement.
- Citation validity: fraction of cited source IDs that exist.
- Source relevance: manual 1-5 rating.
- Factual support: manual 1-5 rating of whether cited evidence supports each claim.
- Reliability: successful runs / total runs.
- Latency and cost: record wall-clock duration and provider usage.

## Tests
```bash
cd backend
pytest
```

## Submission checklist
- Source repository
- README
- 3-5 minute demo: one normal query and one failure/edge case
- Evaluation document with at least five queries and results
- Two or three sample outputs
