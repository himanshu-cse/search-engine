from sqlmodel import Session, select

from crawler.wikipedia_scraper.db import engine
from crawler.wikipedia_scraper.models import Document

def get_documents():
    with Session(engine) as session:
        documents = session.exec(select(Document)).all()
        return documents