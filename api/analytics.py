from re import search

from sqlmodel import Session, select
from collections import Counter

from database.db import engine
from database.models import SearchQuery

def log_search(query: str, result_count: int):
    with Session(engine) as session:
        search = SearchQuery(query=query, result_count=result_count)
        session.add(search)
        session.commit()

def get_analytics():
    with Session(engine) as session:
        searches = session.exec(select(SearchQuery)).all()
        total_searches = len(searches)

        top_queries = Counter(search.query for search in searches).most_common(10)

        average_results = 0

        if total_searches:
            average_results = (sum(search.result_count for search in searches)) / total_searches

        return {
            "total_searches": total_searches,
            "top_queries": top_queries,
            "average_results": round(average_results, 2)
        }