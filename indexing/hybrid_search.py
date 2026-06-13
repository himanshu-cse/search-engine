import json
from math import log, sqrt, ceil
from sentence_transformers import SentenceTransformer

from indexing.preprocess import preprocess
from indexing.db_reader import get_documents
from indexing.bm25 import bm25_score

documents = get_documents()
document_lookup = {str(doc.id): doc for doc in documents}

with open("indexing/inverted_index.json") as f:
    inverted_index = json.load(f)

model = SentenceTransformer("all-MiniLM-L6-v2")

with open("indexing/document_embeddings.json", "r") as f:
    document_embeddings = json.load(f)

def cosine_similarity(v1, v2):
    dot = sum(a*b for a,b in zip(v1,v2))

    norm1 = sqrt(sum(x*x for x in v1))
    norm2 = sqrt(sum(x*x for x in v2))

    if norm1 == 0 or norm2 == 0:
        return 0

    return float(dot / (norm1 * norm2))

def hybrid_search(query, page=1, page_size=10):
    query_terms = preprocess(query)
    query_embedding = model.encode(query, normalize_embeddings=True)

    candidate_docs = set()
    for term in query_terms:
        postings = inverted_index.get(term)
        if postings:
            candidate_docs.update(postings.keys())

    scores = []
    for doc_id in candidate_docs:
        if str(doc_id) not in document_embeddings:
            continue
        bm25 = bm25_score(query_terms,doc_id)
        bm25_sc = bm25 / (bm25+1) # normalize so its doesnt completely dominate hybrid
        semantic_sc = cosine_similarity(query_embedding, document_embeddings[str(doc_id)])

        score = 0.7 * bm25_sc + 0.3 * semantic_sc   # score 0 -> 1

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
                "score": float(round(score, 4))
            }
        )

    return {
        "results": results,
        "total_pages": total_pages,
        "current_page": page,
        "total_results": len(scores),
    }    
    
