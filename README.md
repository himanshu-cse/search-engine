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
