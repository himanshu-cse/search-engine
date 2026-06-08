from collections import Counter, defaultdict
from encodings import unicode_escape
import json

from indexing.db_reader import get_documents
from indexing.preprocess import preprocess

def build_vocabulary():
    docs = get_documents()
    vocabulary = Counter()
    document_frequency = defaultdict(int)
    total_documents = len(docs)

    for doc in docs:
        tokens = preprocess(doc.content)

        # Vocabulary count
        vocabulary.update(tokens)

        # Document Frequency
        unique_tokens = set(tokens)

        for token in unique_tokens:
            document_frequency[token] += 1

    return vocabulary, document_frequency, total_documents

if __name__ == "__main__":

    vocabulary, document_frequency, total_documents = (build_vocabulary())

    print(f"Documents: {total_documents}")

    print("\nTop 20 Terms:")
    print(vocabulary.most_common(20))

    print("\nDocument Frequency Examples:")

    for term in ["python", "language", "database", "algorithm"]:
        print(term,document_frequency.get(term, 0))

    with open("indexing/vocabulary.json", "w") as f:
        json.dump(dict(vocabulary), f, indent=2)

    with open("indexing/document_frequency.json", "w") as f:
        json.dump(dict(document_frequency), f, indent=2)

