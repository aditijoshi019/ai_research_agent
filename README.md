# AI Research Agent

An agentic AI research system that autonomously plans research tasks, retrieves information from the web, evaluates evidence, and generates structured, source-backed reports.

Built using **React, FastAPI, LangGraph, Groq, and Tavily**.

## 1. Project Overview

The AI Research Agent is designed to answer research-oriented questions through an automated research workflow.

Instead of directly generating an answer from an LLM, the system:
- Understands the user's research question.
- Generates a dynamic research plan.
- Identifies relevant research requirements and search queries.
- Retrieves information using external search and extraction tools.
- Evaluates the collected evidence.
- Performs targeted recovery when important information is missing.
- Generates a structured answer with sources, confidence, limitations, and recommendations.

The system uses a single-agent architecture orchestrated through LangGraph.

## 2. Technology Stack

| Component | Technology | Purpose |
|---|---|---|
| Frontend | React.js, Vite | User interface |
| Backend | FastAPI | API and request handling |
| Orchestration | LangGraph | Agent workflow and conditional routing |
| LLM | Groq API (GPT-OSS 120B) | Planning, evaluation, and synthesis |
| Search Tool | Tavily Search API | Web information retrieval |
| Extraction Tool | Tavily Extract API | Webpage content extraction |
| Validation | Pydantic | Structured data validation |
| Language | Python, JavaScript | Backend and frontend development |

## 3. System Architecture

The system follows a planner-executor-evaluator-synthesizer workflow.

### Workflow

1. **User Input:** The user submits a research question through the React frontend.

2. **Planning:** The LLM analyzes the question and generates a dynamic research plan containing specific requirements, priorities, and search queries.

3. **Plan Validation:** Python validates the generated plan using Pydantic.

4. **Information Retrieval:** Tavily Search retrieves relevant webpages for the generated queries.

5. **Source Processing:** Python filters duplicate and invalid URLs and selects relevant sources.

6. **Content Extraction:** Tavily Extract retrieves webpage content from the selected URLs.

7. **Evidence Preparation:** The system creates structured evidence records associated with their source IDs.

8. **Evidence Evaluation:** The LLM evaluates whether the collected information satisfies the research requirements, identifies missing information, and suggests recovery queries.

9. **Conditional Recovery:** If critical or high-priority requirements remain incomplete, LangGraph routes the workflow through one targeted recovery round.

10. **Answer Synthesis:** The LLM generates a structured research report using the collected evidence.

11. **Output Validation:** Pydantic validates the final report, and source references are checked before returning the response.

### Architecture Flow

```text
                User Question
                      |
                      v
                 React Frontend
                      |
                      v
                  FastAPI
                      |
                      v
              LangGraph Workflow
                      |
                      v
                   Planner
                      |
                      v
               Validate Plan
                      |
                      v
                Tavily Search
                      |
                      v
             Filter and Deduplicate
                      |
                      v
                Tavily Extract
                      |
                      v
               Build Evidence
                      |
                      v
              Evidence Evaluator
                      |
                      v
              Conditional Routing
                 /          \
          Insufficient      Sufficient
              |                 |
              v                 |
       Targeted Recovery        |
       Search + Extract         |
              |                 |
              v                 |
        Re-evaluate Evidence ---+
                      |
                      v
                  Synthesizer
                      |
                      v
              Validate Final Report
                      |
                      v
               Structured Response
                      |
                      v
                React Frontend
```

## 4. Why Did You Choose an Agentic Approach?

Traditional LLM-based question answering generates responses directly from the model, which can lead to outdated information, unsupported claims, and hallucinations.

Research questions often require different types of information depending on the topic. For example, comparing technologies requires feature and pricing information, while researching startups requires company discovery and positioning analysis.

An agentic approach allows the system to dynamically determine what information is required, select appropriate tools, evaluate retrieved evidence, and perform additional research when necessary.

LangGraph was selected because it provides explicit state management, workflow orchestration, and conditional routing.

A single-agent architecture was preferred over a multi-agent architecture to keep the implementation simple, reduce coordination overhead, and make the workflow easier to debug.

## 5. What Tools Did You Use, and Why?

The system uses two external research tools.

### Tavily Search API

Used to retrieve relevant webpages, titles, URLs, and search-result content.

It helps the agent discover information based on dynamically generated search queries.

### Tavily Extract API

Used to extract webpage content from selected URLs.

It provides the information required for evidence evaluation and answer synthesis.

### Groq LLM API

Used for three major tasks:

- Planning: Generates research requirements and search queries.
- Evaluation: Checks evidence coverage, missing information, and contradictions.
- Synthesis: Generates the final structured research report.

### LangGraph

Used to orchestrate the workflow through nodes, shared state, normal edges, and conditional edges.

LangGraph also enables the system to implement a controlled recovery loop.

## 6. How Does the System Handle Bad Tool Results?

The system includes basic failure-handling mechanisms:

- **Duplicate search results:** Duplicate URLs are removed before extraction.
- **Invalid URLs:** URLs without valid HTTP or HTTPS schemes are filtered.
- **Extraction failures:** If batch extraction fails, the system attempts individual extraction.
- **Empty content:** Sources without usable content are excluded from evidence preparation.
- **Malformed LLM output:** Pydantic structured-output validation checks the generated data.
- **Incomplete evidence:** The evaluator identifies missing requirements and suggests targeted recovery queries.
- **Recovery limits:** The system permits only one additional recovery round to control execution time and API usage.
- **Workflow errors:** FastAPI logs failures and returns an appropriate error response.

If evidence remains insufficient after recovery, the system should report the limitations rather than inventing missing information.

## 7. How Do You Reduce Hallucinations?

The system uses multiple mechanisms to reduce unsupported answers:

1. **Source-grounded synthesis:** The synthesizer receives retrieved evidence and source metadata rather than relying only on the original question.
2. **Evidence evaluation:** An LLM evaluator checks whether the collected evidence satisfies each research requirement.
3. **Source traceability:** Evidence records contain source IDs, allowing findings to reference the sources used.
4. **Structured output:** Pydantic enforces a predictable final report structure.
5. **Confidence reporting:** The final answer includes a confidence level and an explanation.
6. **Explicit limitations:** Missing or incomplete evidence is reported instead of being presented as established fact.
7. **Prompt-injection awareness:** Retrieved webpage content is treated as untrusted information, not as instructions to the agent.

These mechanisms reduce hallucination risk but do not guarantee that every generated statement is factually correct. Citation support and factual accuracy still require evaluation.

## 8. How Would You Make This Production-Ready?

The current implementation demonstrates the core agentic workflow. Further improvements would include:

- **Stronger source verification:** Prefer official documentation, research papers, and reliable publications.
- **Citation verification:** Associate individual claims with exact supporting evidence spans.
- **Improved content processing:** Use content cleaning, paragraph filtering, and semantic chunking.
- **Caching:** Cache search and extraction results to reduce repeated API calls.
- **Rate limiting:** Control concurrent API requests and respect provider limits.
- **Asynchronous execution:** Use background jobs for long-running research tasks.
- **Persistent state:** Add LangGraph checkpointing to preserve workflow state.
- **Security:** Add authentication, URL/SSRF protection, secret management, and stronger prompt-injection defenses.
- **Testing:** Add unit, integration, and end-to-end tests.
- **Observability:** Integrate tracing and monitoring for workflow execution.

## 9. What Would You Monitor in Production?

Important monitoring metrics include:

| Metric | Purpose |
|---|---|
| Request success rate | Measures successful research executions |
| Average execution time | Measures research latency |
| LLM token usage | Tracks model consumption and cost |
| Tavily API usage | Tracks external tool consumption |
| Tool failure rate | Identifies search and extraction failures |
| Recovery frequency | Measures how often additional research is required |
| Requirement coverage | Measures completeness of collected evidence |
| Citation validity | Measures whether cited source IDs exist |
| Source relevance | Measures the quality of retrieved sources |
| Confidence distribution | Helps evaluate confidence calibration |

Logs should also capture node execution times, error messages, retry attempts, and workflow status.

## 10. Key Design Trade-offs

### Single-Agent vs Multi-Agent

A single-agent architecture was selected because the assignment requires a focused research workflow. It avoids unnecessary communication and coordination overhead.

### Dynamic Planning vs Fixed Research Categories

Dynamic research requirements were chosen because different questions require different kinds of evidence. A fixed set of categories would not generalize well across technology comparisons, company discovery, and general research.

### LLM-Based Evaluation vs Rule-Based Evaluation

An LLM evaluator was chosen for semantic assessment because determining whether evidence actually answers a requirement requires contextual understanding.

Python handles deterministic checks such as schema validation, source ID validation, limits, and conditional routing.

### Conditional Recovery vs Unlimited Research

Only one recovery round is permitted. This balances answer completeness against API cost, latency, and token consumption.

### Evidence Quality vs Retrieval Quantity

The system limits the number and size of sources sent to the LLM to control token usage. This reduces unnecessary context but can also exclude useful information.

## 11. Installation and Setup

### Prerequisites

- Python 3.10+
- Node.js 18+
- Groq API key
- Tavily API key

### Backend Setup

Navigate to the backend directory:

```bash
cd backend
```

Create and activate a virtual environment:

```bash
python -m venv .venv
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file inside the backend directory:

```env
GROQ_API_KEY=your_groq_api_key
TAVILY_API_KEY=your_tavily_api_key
GROQ_MODEL=openai/gpt-oss-120b

MAX_SEARCH_QUERIES=4
MAX_SOURCES=8
MAX_RECOVERY_ROUNDS=1
```

Start the backend:

```bash
uvicorn app.main:app --reload
```

Backend URL: `http://localhost:8000`

API documentation: `http://localhost:8000/docs`

### Frontend Setup

Open another terminal:

```bash
cd frontend
npm install
npm run dev
```

Frontend URL: `http://localhost:5173`

## 12. API Usage

### Endpoint

```http
POST /api/research
```

### Request

```json
{
  "question": "Compare Pinecone and Qdrant for building a small RAG application."
}
```

### Response

The API returns:

- Research plan
- Evidence evaluation
- Structured final report
- Source information
- Confidence and limitations
- Agent execution trace
- Recovery count

## 13. Evaluation Strategy

The system will be evaluated using at least five research questions covering different task types.

| Test Case | Research Query | Expected Behavior |
|---|---|---|
| 1 | Compare three open-source vector databases for RAG applications. | Generate a feature comparison with supporting sources. |
| 2 | Find five Indian B2B SaaS startups in HR technology. | Discover companies and summarize their positioning. |
| 3 | Explain the pros and cons of multi-agent architecture for customer support. | Present balanced findings with evidence. |
| 4 | Compare fixed-size, recursive, and semantic chunking. | Identify and compare the different approaches. |
| 5 | Research a narrow topic with limited public evidence. | Report missing evidence and lower confidence when appropriate. |

### Evaluation Metrics

- Requirement coverage
- Source relevance
- Citation validity
- Factual support
- Confidence calibration
- Execution success rate
- Average latency

Evaluation results, observations, and sample outputs should be documented separately.

## 14. Known Limitations

- Search results may contain irrelevant or low-quality sources.
- Webpage extraction may return incomplete or noisy content.
- LLM-based evidence evaluation may incorrectly assess relevance or completeness.
- Citation references identify sources but do not yet guarantee exact claim-level support.
- A single recovery round may not be sufficient for complex research questions.
- Confidence scores are model-generated assessments and are not statistically calibrated.
- API availability, token limits, and rate limits can affect execution.

## 15. Future Improvements

- Claim-level citation verification.
- Improved evidence extraction and semantic chunking.
- Source reliability and freshness scoring.
- Persistent graph checkpoints.
- Search-result and extraction caching.
- More comprehensive automated evaluation.
- Production monitoring and tracing.
- Authentication and deployment support.

## 16. Project Structure

```text
ai-research-agent/
│
├── backend/
│   ├── app/
│   │   ├── config.py
│   │   ├── graph.py
│   │   ├── llm.py
│   │   ├── main.py
│   │   ├── schemas.py
│   │   └── tools.py
│   │
│   ├── tests/
│   ├── requirements.txt
│   └── test_groq.py
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── style.css
│   ├── index.html
│   └── package.json
│
├── evaluation/
│   └── evaluation_template.md
│
├── .gitignore
└── README.md
```

## 17. Conclusion

The AI Research Agent demonstrates how an LLM can be combined with external research tools and workflow orchestration to perform structured research tasks.

By integrating dynamic planning, web retrieval, evidence evaluation, conditional recovery, and source-backed synthesis, the system goes beyond basic question answering and provides a foundation for building more reliable AI research applications.