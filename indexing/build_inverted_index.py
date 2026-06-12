from collections import defaultdict, Counter
import json

from indexing.db_reader import get_documents
from indexing.preprocess import preprocess

inverted_index = defaultdict(dict)

documents = get_documents()

for i, doc in enumerate(documents, start=1):
    if i%100 == 0:
        print(f"Processed {i}/{len(documents)} docs")

    tokens = preprocess(doc.content)
    counts = Counter(tokens)

    for term, frequency in counts.items():
        inverted_index[term][str(doc.id)] = frequency

with open("indexing/inverted_index.json", "w") as f:
    json.dump(inverted_index, f)

print(f"Built inverted index for {len(documents)} docs in indexing/inverted_index.json")