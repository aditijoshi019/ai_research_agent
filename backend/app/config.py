import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY", "")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
MAX_SEARCH_QUERIES = int(os.getenv("MAX_SEARCH_QUERIES", "4"))
MAX_SOURCES = int(os.getenv("MAX_SOURCES", "8"))
MAX_RECOVERY_ROUNDS = int(os.getenv("MAX_RECOVERY_ROUNDS", "1"))
