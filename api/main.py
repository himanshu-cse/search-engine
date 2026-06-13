from fastapi import FastAPI
from indexing.search import bm25_search
from indexing.semantic_search import semantic_search
from indexing.hybrid_search import hybrid_search
from indexing.autocomplete import autocomplete
from api.analytics import log_search, get_analytics
from fastapi.middleware.cors import CORSMiddleware 

app = FastAPI()

# Our browser and api are on different ports, and we dont want our browser to block these api calls while fetching using our html
# If you look closely at the Response Headers in your Network tab, the request to 127.0.0.1:8000 returns a 200 OK, 
# but it is entirely missing the Access-Control-Allow-Origin header.
# Because your frontend is on a different port (8001), the browser will block your JavaScript from reading the 
# response due to CORS policy constraints. 

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:8001", "http://localhost:8001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/search")
def search_document(q: str, page: int = 1, type: str = "hybrid"):
    if type == "bm25":
        search_response = bm25_search(q, page=page, page_size=10)
    elif type == "semantic":
        search_response = semantic_search(q, page=page, page_size=10)
    else:
        search_response = hybrid_search(q, page=page, page_size=10)
    log_search(q, search_response["total_results"])
    return search_response

@app.get("/analytics")
def analytics():
    return get_analytics()

@app.get("/autocomplete")
def autocomplete_api(q: str):
    return autocomplete(q)