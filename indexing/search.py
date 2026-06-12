import json
from math import ceil

from indexing.preprocess import preprocess
from indexing.db_reader import get_documents
from indexing.bm25 import bm25_score

documents = get_documents()
document_lookup = {str(doc.id): doc for doc in documents}

with open("indexing/inverted_index.json") as f:
    inverted_index = json.load(f)

def search(query, page=1, page_size=10):
    query_terms = preprocess(query)

    candidate_docs = set()
    for term in query_terms:
        postings = inverted_index.get(term)
        if postings:
            candidate_docs.update(postings.keys())

    scores = []
    for doc_id in candidate_docs:
        score = bm25_score(query_terms,doc_id)

        # title boost
        title_terms = preprocess(document_lookup[str(doc_id)].title)
        matches = len(set(query_terms).intersection(set(title_terms)))
        score *= (1+matches*0.3)

        if score > 0:
            scores.append((doc_id, score))

    scores.sort(key=lambda x: x[1], reverse=True)

    total_pages = ceil(len(scores)/page_size)
    start = (page - 1) * page_size
    end = start + page_size

    results = []
    for doc_id, score in scores[start:end]:
        doc = document_lookup[str(doc_id)]
        results.append(
            {
                "id": doc.id,
                "title": doc.title,
                "url": doc.url,
                "summary": (doc.summary[:200] if doc.summary else ""),
                "score": round(score, 4)
            }
        )

    return {
        "results": results,
        "total_pages": total_pages,
        "current_page": page,
        "total_results": len(scores),
    }