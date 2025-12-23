from pydantic import BaseModel


class AnalyzeRequest(BaseModel):
    content: str


class AnalyzeResponse(BaseModel):
    length: int
    preview: str
    normalized_text: str

class SearchHit(BaseModel):
    id: str
    title: str | None
    body: str
    score: float
