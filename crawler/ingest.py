import random
from collections import deque

import wikipediaapi
from sqlmodel import Session, select

from database.db import engine
from database.models import Document

wiki = wikipediaapi.Wikipedia(user_agent="search-engine", language="en")

MAX_PAGES = 10000
VISITED_PATH = "crawler/visited.txt"

session = Session(engine)

# Existing URLs in DB
existing_urls = set(session.exec(select(Document.url)).all())

visited = set()
visited_file = open(VISITED_PATH, "a", encoding="utf-8")


def mark_visited(title: str):
    visited.add(title)
    visited_file.write(title + "\n")
    visited_file.flush()


def is_article(title: str) -> bool:
    """
    Real Wikipedia articles generally do not contain namespace prefixes.
    """
    return ":" not in title


def save_page(page):
    if page.fullurl in existing_urls:
        return False

    document = Document(
        title=page.title,
        url=page.fullurl,
        summary=page.summary,
        content=page.text,
        source="wikipedia",
        content_length=len(page.text),
    )

    session.add(document)
    session.commit()

    existing_urls.add(page.fullurl)
    return True


# Collect seed articles from Vital Articles hierarchy
seed_queue = deque(["Wikipedia:Vital articles/Level/5"])
seen_vital = set()
seed_articles = set()

while seed_queue:
    title = seed_queue.popleft()

    if title in seen_vital:
        continue

    seen_vital.add(title)

    try:
        page = wiki.page(title)

        if not page.exists():
            continue

        links = list(page.links.keys())

    except Exception as e:
        print(f"Seed fetch failed for {title}: {e}")
        continue

    for link in links:
        if link.startswith("Wikipedia:Vital articles"):
            seed_queue.append(link)

        elif is_article(link):
            seed_articles.add(link)

seed_articles = list(seed_articles)
random.shuffle(seed_articles)

print(f"Collected {len(seed_articles)} unique seed articles")

# Main crawl
queue = deque(seed_articles)
queued_set = set(seed_articles)

stored_count = 0
processed = 0

while queue and stored_count < MAX_PAGES:

    title = queue.popleft()

    if title in visited:
        continue

    try:
        page = wiki.page(title)

        if not page.exists():
            continue

    except Exception as e:
        print(f"Error fetching {title}: {e}")
        continue

    # mark visited after successful fetch
    mark_visited(title)

    processed += 1

    if processed % 100 == 0:
        print(f"Stored: {stored_count} | "f"Visited: {len(visited)} | "f"Queue: {len(queue)}")

    if len(page.text) < 1000 or len(page.summary) < 100:
        continue

    try:
        saved = save_page(page)
    except Exception as e:
        print(f"Error saving {title}: {e}")
        session.rollback()
        continue

    if saved:
        stored_count += 1

    links = list(page.links.keys())
    random.shuffle(links)

    for link in links[:20]:
        if not is_article(link):
            continue

        if link not in visited and link not in queued_set:
            queue.append(link)
            queued_set.add(link)

visited_file.close()

print(f"Done. Processed {processed} pages, "f"visited {len(visited)} pages, "f"stored {stored_count} documents.")