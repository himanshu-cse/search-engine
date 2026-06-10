from sqlmodel import Session, select

from database.db import engine
from database.models import Document

def get_documents():
    with Session(engine) as session:
        documents = session.exec(select(Document)).all()
        return documents