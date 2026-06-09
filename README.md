# Architecture v1

                +------------+
                | Wikipedia Data|
                +------------+
                       |
                       v
                ETL / Indexer
                       |
                       v
                PostgreSQL
                 + Indexes
                       |
                       v
    FastAPI Search API <----> TF-IDF Search Service
           |
           v
    Django Frontend
           |
           v
    Search Results UI

# User Flow

Wikipedia Search Engine

User Query
    ↓
FastAPI
    ↓
TF-IDF Search
    ↓
Wikipedia Documents
    ↓
PostgreSQL
    ↓
Django Frontend


# Tech Stack 
* Backend Search API: FastAPI
* Frontend: Django
* Database: PostgreSQL

# Step 1: Crawler
* get the pages from wiki api
    * ` pip install wikipediaapi `
# Step 2: Indexing
* do pre processing (lowercase -> tokenize -> store)
    * ` pip install nltk `
    * "https://www.nltk.org/book/ch03.html"
* build TF-IDf 
    * ` pip install scikit-learn `
    * "https://nlp.stanford.edu/IR-book/html/htmledition/irbook.html" - ch 1 & 6
    * "https://jalammar.github.io/illustrated-word2vec/"
* search through the docs, rank on cosine similarity and get the title of doc with most similarity
    * ` python web framework `


