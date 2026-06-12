import json

from indexing.db_reader import get_documents
from indexing.preprocess import preprocess

documents = get_documents()
document_lengths = {}

for doc in documents:
    tokens = preprocess(doc.content)
    document_lengths[str(doc.id)] = len(tokens)

with open("indexing/document_lengths.json", "w") as f:
    json.dump(document_lengths, f)