import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from tavily import TavilyClient
from app.config import TAVILY_API_KEY

logger = logging.getLogger(__name__)

def get_tavily():
    if not TAVILY_API_KEY:
        raise RuntimeError("TAVILY_API_KEY is missing. Add it to backend/.env")
    return TavilyClient(api_key=TAVILY_API_KEY)

def _search_one(query: str) -> list[dict]:
    # Tavily's search endpoint accepts one query per request.
    # We fan out several queries concurrently as one logical graph node.
    response = get_tavily().search(
        query=query,
        search_depth="advanced",
        max_results=5,
        include_answer=False,
    )
    return response.get("results", [])

def batch_search(queries: list[str]) -> list[dict]:
    results = []
    unique_queries = list(dict.fromkeys(q.strip() for q in queries if q.strip()))
    with ThreadPoolExecutor(max_workers=min(4, max(1, len(unique_queries)))) as pool:
        futures = {pool.submit(_search_one, q): q for q in unique_queries}
        for future in as_completed(futures):
            query = futures[future]
            try:
                results.extend(future.result())
            except Exception:
                logger.exception("Search failed for query: %s", query)
    # Deduplicate by URL while preserving first occurrence.
    seen, unique = set(), []
    for item in results:
        url = item.get("url")
        if url and url not in seen:
            seen.add(url)
            unique.append(item)
    return unique

def batch_extract(urls: list[str]) -> list[dict]:
    if not urls:
        return []
    try:
        # Tavily Extract accepts multiple URLs in one API call.
        response = get_tavily().extract(urls=urls, extract_depth="advanced")
        return response.get("results", [])
    except Exception:
        logger.exception("Batch extraction failed; attempting individual extraction")
        recovered = []
        client = get_tavily()
        for url in urls:
            try:
                one = client.extract(urls=[url], extract_depth="basic")
                recovered.extend(one.get("results", []))
            except Exception:
                logger.exception("Extraction failed for %s", url)
        return recovered
