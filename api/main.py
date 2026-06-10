from fastapi import FastAPI
from indexing.search import search
from api.analytics import log_search, get_analytics

app = FastAPI()

@app.get("/search")
def search_document(q: str, page: int = 1):
    search_response = search(q, page=page, page_size=10)
    log_search(q, search_response["total_results"])
    return search_response

@app.get("/analytics")
def analytics():
    return get_analytics()