import logging
from fastapi import Depends
from app.auth import get_current_user

from fastapi import FastAPI, HTTPException

from app.schemas import AnalyzeRequest, AnalyzeResponse
from app.services import analyze_text, embed_text

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
    semantic_search,
)
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError

from app.exceptions import (
    validation_exception_handler,
    sqlalchemy_exception_handler,
    generic_exception_handler,
)

# -----------------------
# Logging
# -----------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

logger = logging.getLogger(__name__)

# -----------------------
# App
# -----------------------
app = FastAPI(
    title="Content Search Backend",
    description="Backend service for semantic search over business content",
)
app.add_exception_handler(
    RequestValidationError,
    validation_exception_handler,
)

app.add_exception_handler(
    SQLAlchemyError,
    sqlalchemy_exception_handler,
)

app.add_exception_handler(
    Exception,
    generic_exception_handler,
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


# -------- Debug / Analyze--------
@app.post("/analyze", response_model=AnalyzeResponse)
def analyze_content(payload: AnalyzeRequest) -> AnalyzeResponse:
    clean_text = preprocess_text(payload.content)
    result = analyze_text(clean_text)
    return AnalyzeResponse(**result)


# -------- Business APIs--------
@app.post("/contents", response_model=ContentOut)
def create_content_api(
    payload: ContentCreate,
    user=Depends(get_current_user),  
) -> ContentOut:
    validate_body_not_empty(payload.body)

   
    embedding = embed_text(payload.body)

    db = SessionLocal()
    try:
        row = create_content(
            db=db,
            title=payload.title,
            body=payload.body.strip(),
            embedding=embedding,
        )

        if not row:
            raise HTTPException(status_code=500, detail="failed to create content")

        logger.info(
            f"Content created | id={row.id} | user={user.get('sub')}"
        )

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
def search_contents(
    payload: SearchRequest,
    user=Depends(get_current_user),  
) -> SearchResponse:
    query = payload.query
    top_k = payload.top_k

    
    query_embedding = embed_text(query)

    db = SessionLocal()
    try:
        rows = semantic_search(
            db=db,
            query_embedding=query_embedding,
            top_k=top_k,
        )
    finally:
        db.close()

    results: list[SearchHit] = []

    for row in rows:
        results.append(
            SearchHit(
                id=str(row.id),
                title=row.title,
                body=row.body,
                score=float(row.score),
            )
        )

    return SearchResponse(results=results)
