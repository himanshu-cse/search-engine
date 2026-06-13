import json
from math import log, sqrt, ceil
from sentence_transformers import SentenceTransformer

from indexing.db_reader import get_documents

documents = get_documents()
document_lookup = {str(doc.id): doc for doc in documents}
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

def semantic_search(query, page=1, page_size=10):
    query_embedding = model.encode(query, normalize_embeddings=True)

    scores = []
    for doc in documents:
        if str(doc.id) not in document_embeddings:
            continue
        score = cosine_similarity(query_embedding, document_embeddings[str(doc.id)])
        if score > 0:
            scores.append((str(doc.id), score))

    scores.sort(key=lambda x: x[1], reverse=True)

    total_pages = ceil(len(scores) / page_size)

    results = []
    start = (page-1)*page_size
    end = start + page_size
    for doc_id, score in scores[start:end]:
        doc = document_lookup[doc_id]
        results.append(
            {
                "id": doc.id,
                "title": doc.title,
                "url": doc.url,
                "summary": (
                    doc.summary[:200]
                    if doc.summary
                    else ""
                ),
                "score": float(round(score, 4))
            }
        )

    return {
        "results": results, 
        "total_pages": total_pages,
        "current_page": page,
        "total_results": len(scores),
    }