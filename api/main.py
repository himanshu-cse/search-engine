from fastapi import FastAPI
from indexing.search import search
from api.analytics import log_search, get_analytics

app = FastAPI()

@app.get("/search")
def search_document(q: str):
    results = search(q)
    log_search(q, len(results))
    return results

@app.get("/analytics")
def analytics():
    return get_analytics()