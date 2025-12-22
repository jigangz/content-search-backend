import logging

from fastapi import FastAPI, HTTPException

from app.schemas import AnalyzeRequest, AnalyzeResponse
from app.services import analyze_text
from app.models import (
    ContentCreate,
    ContentOut,
    SearchRequest,
    SearchResponse,
    SearchHit,
)
from app.validators import validate_body_not_empty

from app.db import SessionLocal
from app.repositories.contents import (
    create_content,
    get_content,
    list_contents,
)

# -----------------------
# Logging
# -----------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)

# -----------------------
# App
# -----------------------
app = FastAPI(
    title="Content Search Backend",
    description="Backend service for semantic search over business content"
)

# -----------------------
# Utils
# -----------------------
def get_service_info() -> dict:
    return {
        "service": "content-search-backend",
        "status": "ok",
        "domain": "business-content-search",
    }


def preprocess_text(text: str) -> str:
    return " ".join(text.strip().split())

# -----------------------
# Routes
# -----------------------
@app.get("/health")
def health_check() -> dict:
    logger.info("Health check requested")
    return get_service_info()


# -------- Debug / Analyze（保留，不进 DB）--------
@app.post("/analyze", response_model=AnalyzeResponse)
def analyze_content(payload: AnalyzeRequest) -> AnalyzeResponse:
    clean_text = preprocess_text(payload.content)
    result = analyze_text(clean_text)
    return AnalyzeResponse(**result)


# -------- Business APIs（Day3：走数据库）--------
@app.post("/contents", response_model=ContentOut)
def create_content_api(payload: ContentCreate) -> ContentOut:
    validate_body_not_empty(payload.body)

    db = SessionLocal()
    try:
        row = create_content(
            db=db,
            title=payload.title,
            body=payload.body.strip(),
        )

        if not row:
            raise HTTPException(status_code=500, detail="failed to create content")

        logger.info(f"Content created in DB: {row.id}")

        return ContentOut(
            id=str(row.id),
            title=row.title,
            body=row.body,
            created_at=row.created_at,
        )
    finally:
        db.close()


@app.get("/contents/{content_id}", response_model=ContentOut)
def get_content_api(content_id: str) -> ContentOut:
    db = SessionLocal()
    try:
        row = get_content(db=db, content_id=content_id)
        if not row:
            raise HTTPException(status_code=404, detail="content not found")

        return ContentOut(
            id=str(row.id),
            title=row.title,
            body=row.body,
            created_at=row.created_at,
        )
    finally:
        db.close()


@app.post("/search", response_model=SearchResponse)
def search_contents(payload: SearchRequest) -> SearchResponse:
    """
    Day3: 仍然是 mock search
    Day5: 这里会整体换成 embedding + pgvector
    """
    query = payload.query.lower()
    top_k = payload.top_k

    db = SessionLocal()
    try:
        rows = list_contents(db=db)
    finally:
        db.close()

    results: list[SearchHit] = []

    for row in rows:
        if query in row.body.lower():
            results.append(
                SearchHit(
                    id=str(row.id),
                    title=row.title,
                    body=row.body,
                    score=1.0,
                )
            )

    return SearchResponse(results=results[:top_k])
