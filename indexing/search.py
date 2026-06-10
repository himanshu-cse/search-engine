import json
from collections import Counter
from math import log, sqrt

from indexing.db_reader import get_documents
from indexing.preprocess import preprocess
from indexing.build_vocabulary import build_vocabulary

documents = get_documents()
document_lookup = {str(doc.id): doc for doc in documents}


with open("indexing/tfidf_index.json") as f:
    document_vectors = json.load(f)

_, document_frequency, total_documents = (build_vocabulary())

def query_tfidf(query):
    tokens = preprocess(query)
    counts = Counter(tokens)
    total_terms = len(tokens)
    vector = {}
    for term, count in counts.items():
        tf = count / total_terms
        df = document_frequency.get(term, 1)  # get function get(x, default) if x not found then gives default
        # idf = log(total_documents / df)
        idf = log((total_documents + 1) / (df + 1)) # smoothing
        vector[term] = tf * idf
    return vector

def similarity(query_vector, document_vector):
    score = 0
    for term, query_weight in query_vector.items():
        score += (query_weight * document_vector.get(term, 0))
    return score

def cosine_similarity(query_vector, document_vector):
    dot_product = 0

    for term, weight in query_vector.items():
        dot_product += (weight * document_vector.get(term, 0))

    query_norm = sqrt(sum(value * value for value in query_vector.values()))
    document_norm = sqrt(sum(value * value for value in document_vector.values()))

    if query_norm == 0 or document_norm == 0:
        return 0

    return (dot_product / (query_norm * document_norm))

def search(query, top_k=10):
    query_terms = set(preprocess(query))
    query_vector = query_tfidf(query)
    scores = []
    for doc_id, doc_vector in document_vectors.items():
        score = cosine_similarity(query_vector, doc_vector)

        title_terms = set(preprocess(document_lookup[doc_id].title))
        matches = len(query_terms.intersection(title_terms))
        score *= (1 + matches * 0.3)

        if score > 0:
            scores.append((doc_id, score))

    scores.sort(key=lambda x: x[1], reverse=True)

    results = []
    for doc_id, score in scores[:top_k]:
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
                "score": round(score, 4)
            }
        )

    return results

if __name__ == "__main__":
    results = search("python web framework")
    for result in results:
        print(result)
