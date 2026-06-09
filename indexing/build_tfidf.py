from collections import Counter
from math import log
import json

from indexing.db_reader import get_documents
from indexing.preprocess import preprocess
from indexing.build_vocabulary import build_vocabulary

vocabulary, document_frequency, total_documents = (build_vocabulary())

documents = get_documents()

def calculate_tf(tokens):
    counts = Counter(tokens)
    total_terms = len(tokens)

    tf = {}
    for term, count in counts.items():
        tf[term] = count / total_terms
    return tf

def calculate_idf(term):
    df = document_frequency.get(term, 0)
    if df == 0:
        return 0
    return log(total_documents / df)

# TFIDF(t,d)=TF(t,d)⋅IDF(t)
def calculate_tfidf(tokens):
    tf = calculate_tf(tokens)
    tfidf = {}
    for term, tf_value in tf.items():
        idf = calculate_idf(term)
        tfidf[term] = tf_value * idf
    return tfidf

document_vectors = {}
for doc in documents:
    tokens = preprocess(doc.content)
    tfidf_vector = calculate_tfidf(tokens)
    document_vectors[doc.id] = tfidf_vector

with open("indexing/tfidf_index.json", "w") as f:
    json.dump(document_vectors, f)
