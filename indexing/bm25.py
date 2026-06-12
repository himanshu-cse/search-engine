import json
from math import log

with open("indexing/inverted_index.json") as f:
    inverted_index = json.load(f)

with open("indexing/document_frequency.json") as f:
    document_frequency = json.load(f)

with open("indexing/document_lengths.json") as f:
    document_lengths = json.load(f)

N = len(document_lengths)
avgdl = (sum(document_lengths.values())/ N)

K1 = 1.5
B = 0.75

def bm25_score(query_terms, doc_id):
    score = 0
    doc_length = document_lengths[str(doc_id)]
    for term in query_terms:
        postings = inverted_index.get(term)
        if not postings:
            continue

        tf = postings.get(str(doc_id), 0)
        if tf == 0:
            continue

        df = document_frequency.get(term, 0)
        idf = log((N - df + 0.5)/(df + 0.5) + 1)

        numerator = tf * (K1 + 1)
        denominator = (tf + K1 * (1 - B + B * (doc_length / avgdl)))

        score += idf * (numerator / denominator)

    return score