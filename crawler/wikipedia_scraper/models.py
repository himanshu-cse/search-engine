from pydantic import BaseModel
from sqlmodel import SQLModel, Field
from sqlalchemy import Column, Integer, String, Text
from datetime import datetime

class Document(SQLModel, table=True):
    __tablename__ = "documents"

    id: int | None = Field(default=None, primary_key=True)     # SERIAL
    title: str
    url: str = Field(unique=True)
    summary: str = Field(sa_column=Column(Text))
    content: str = Field(sa_column=Column(Text))
    source: str = "wikipedia"
    content_length: int
    created_at: datetime = Field(default_factory=datetime.now)