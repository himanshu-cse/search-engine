# Wikipedia Search Engine

A small search engine built from scratch to learn how real search systems work.

Started with a simple TF-IDF implementation and gradually evolved into a more complete search engine with crawling, indexing, autocomplete, BM25 ranking, semantic search and a web UI.

---

# Architecture

```text
Wikipedia
    ↓
Crawler
    ↓
PostgreSQL
    ↓
Indexing Pipeline
    ├── Vocabulary
    ├── Document Frequency
    ├── TF-IDF
    ├── Inverted Index
    ├── Trie
    └── Embeddings
    ↓
FastAPI
    ↓
Django Frontend
```

---

# User Flow

```text
User Query
    ↓
Django Frontend
    ↓
FastAPI Search API
    ↓
Search Engine
    ↓
Rank Results
    ↓
Return Results
    ↓
Display Results
```

---

# Tech Stack

* Backend API: FastAPI
* Frontend: Django
* Database: PostgreSQL
* NLP: NLTK
* Semantic Search: Sentence Transformers
* Data Source: Wikipedia API

---

# Features

## Crawler

Built a Wikipedia crawler that:

* Starts from seed pages
* Follows links using BFS
* Stores pages in PostgreSQL
* Avoids duplicates
* Supports resuming crawls

Current corpus:

```text
~8000 Wikipedia articles
```

---

## Text Processing

Using NLTK:

* Lowercasing
* Tokenization
* Stopword removal
* Lemmatization

Pipeline:

```text
Raw Text
    ↓
Lowercase
    ↓
Tokenize
    ↓
Remove Stopwords
    ↓
Lemmatize
```

---

## TF-IDF Search (v1)

First version of the search engine.

Implemented:

* Vocabulary building
* Document frequency calculation
* TF-IDF vectors
* Cosine similarity ranking

Query:

```text
python web framework
```

↓

Rank documents using TF-IDF similarity.

---

## Inverted Index

Built an inverted index to avoid scanning every document.

Structure:

```python
{
    "python": {
        "12": 5,
        "48": 2,
        "92": 7
    }
}
```

Instead of searching all documents, search only candidate documents containing query terms.

---

## BM25 Ranking

Replaced TF-IDF ranking with BM25.

Benefits:

* Better term frequency handling
* Better document length normalization
* More realistic search ranking

---

## Autocomplete

Implemented autocomplete using a Trie.

As the user types:

```text
py
```

↓

Suggestions:

```text
python
pytest
pytorch
```

Autocomplete requests are fetched asynchronously using JavaScript and FastAPI.

---

## Pagination

Added pagination to avoid loading all results at once.

Features:

* Previous / Next navigation
* Smart page numbers
* Preserves query state

---

## Analytics Dashboard

Tracks:

* Search queries
* Number of results returned

Can be used to understand search behavior and debug ranking quality.

---

## Semantic Search

Added semantic search using:

```python
sentence-transformers
all-MiniLM-L6-v2
```

Instead of matching only keywords, documents are converted into embeddings.

This allows:

```text
doctor
```

to match:

```text
physician
medical practitioner
```

even if exact keywords differ.

---

## Hybrid Search

Current default search mode.

Combines:

```text
BM25
+
Semantic Search
```

Formula:

```text
0.7 * BM25
+
0.3 * Semantic Similarity
```

Also includes title boosting.

This usually performs better than either method alone.

---

# Search Modes

### BM25

Traditional keyword search.

### Semantic

Embedding-based search.

### Hybrid

BM25 + Semantic Search.

Recommended mode.

---

# Things I Learned

* Crawling large document collections
* PostgreSQL basics
* NLP preprocessing
* TF-IDF
* BM25
* Inverted indexes
* Tries
* FastAPI
* Django
* AJAX / Fetch API
* CORS
* Sentence embeddings
* Search ranking systems

---

# Future Improvements

* Better analytics dashboard
* Hybrid score tuning
* Query suggestions
* Search result snippets
* Vector database (FAISS)
* Learning-to-rank experiments
* More data sources beyond Wikipedia

---

# Why I Built This

Mostly to understand what happens behind a search box.

Instead of relying on Elasticsearch or a vector database, the goal was to implement the core pieces manually and learn how search engines work from crawling all the way to ranking results.
