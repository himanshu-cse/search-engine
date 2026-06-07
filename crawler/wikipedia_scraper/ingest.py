import wikipediaapi
from collections import deque
from sqlmodel import Session, select

from db import engine
from models import Document


wiki = wikipediaapi.Wikipedia(
    user_agent="search-engine",
    language="en"
)

MAX_PAGES = 100

visited = set()

queue = deque([
    "Python_(programming_language)",
    "Django_(web_framework)",
    "FastAPI",
    "Machine_learning",
    "Database",
])


def save_page(page):

    document = Document(
        title=page.title,
        url=page.fullurl,
        summary=page.summary,
        content=page.text,
        source="wikipedia",
        content_length=len(page.text)
    )

    with Session(engine) as session:

        existing = session.exec(select(Document).where(Document.url == page.fullurl)).first()

        if existing:
            return False

        session.add(document)
        session.commit()

        return True


while queue and len(visited) < MAX_PAGES:

    title = queue.popleft()
    if title in visited:
        continue

    visited.add(title)

    page = wiki.page(title)
    if not page.exists():
        continue

    print(f"Crawling: {page.title}")
    save_page(page)

    links = list(page.links.keys())
    for link in links[:15]:
        if link not in visited:
            queue.append(link)

print(f"Done. Crawled {len(visited)} pages.")