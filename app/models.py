from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class ContentCreate(BaseModel):
    title: Optional[str] = None
    body: str


class ContentOut(BaseModel):
    id: str
    title: Optional[str] = None
    body: str
    created_at: datetime


class SearchRequest(BaseModel):
    query: str
    top_k: int = 5


class SearchHit(BaseModel):
    id: str
    title: Optional[str] = None
    body: str
    score: float


class SearchResponse(BaseModel):
    results: List[SearchHit]
