import json
from sentence_transformers import SentenceTransformer

from indexing.db_reader import get_documents

def build_embeddings():
    model = SentenceTransformer("all-MiniLM-L6-v2")

    documents = get_documents()

    texts = [f"{doc.title}. {doc.summary}" for doc in documents]
    vectors = model.encode(texts, normalize_embeddings=True, show_progress_bar=True)

    embeddings = {
        str(doc.id): vector.tolist()
        for doc, vector in zip(documents, vectors)
    }

    with open("indexing/document_embeddings.json", "w") as f:
        json.dump(embeddings, f)

if __name__ == "__main__":
    build_embeddings()