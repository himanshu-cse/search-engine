import wikipediaapi
import json

wiki = wikipediaapi.Wikipedia(user_agent='Wekipedia Search Engine', language='en')

visited = set()

queue = [
    "Python_(programming_language)",
    "Django_(web_framework)",
    "FastAPI",
    "Machine_learning",
    "Database",
]

total_documents = 0

while queue and total_documents < 100:
    title = queue.pop(0)

    if title in visited:
        continue

    visited.add(title)

    page = wiki.page(title)

    if not page.exists():
        continue

    doc = {
        "title": page.title,
        "url": page.fullurl,
        "summary": page.summary,
        "content": page.text,
        "categories": list(page.categories.keys())
    }

    with open('documents.jsonl', "a", encoding="utf-8") as file:
        file.write(json.dumps(doc))
        file.write("\n")

    for link in list(page.links.keys())[:10]:
        if link not in visited:
            queue.append(link)

