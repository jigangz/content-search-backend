from pydantic import BaseModel


class AnalyzeRequest(BaseModel):
    content: str


class AnalyzeResponse(BaseModel):
    length: int
    preview: str
    normalized_text: str

