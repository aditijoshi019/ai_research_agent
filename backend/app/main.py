import logging
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.schemas import ResearchRequest
from app.graph import run_research

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="AI Research Agent", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/api/research")
def research(request: ResearchRequest):
    try:
        result = run_research(request.question)
        return {
            "report": result["report"],
            "trace": result.get("trace", []),
            "plan": result.get("plan", {}),
            "evaluation": result.get("evaluation", {}),
            "recovery_count": result.get("recovery_count", 0),
        }
    except Exception as exc:
        logger.exception("Research workflow failed")
        raise HTTPException(
            status_code=502,
            detail="The research workflow could not be completed. Check server logs and API keys.",
        ) from exc
