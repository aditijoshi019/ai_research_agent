from langchain_groq import ChatGroq
from app.config import GROQ_API_KEY, GROQ_MODEL

def get_llm():
    if not GROQ_API_KEY:
        raise RuntimeError("GROQ_API_KEY is missing. Add it to backend/.env")
    return ChatGroq(
        api_key=GROQ_API_KEY,
        model=GROQ_MODEL,
        temperature=0,
        max_retries=2,
        timeout=45,
    )
