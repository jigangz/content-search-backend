import logging
from app.schemas import AnalyzeRequest, AnalyzeResponse
from app.services import analyze_text

from fastapi import FastAPI

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)

app = FastAPI(
    title="Content Search Backend",
    description="Backend service for semantic search over business content"
)


def get_service_info() -> dict:
    """
    Returns service metadata for health checks and monitoring.
    """
    return {
        "service": "content-search-backend",
        "status": "ok",
        "domain": "business-content-search"
    }

def preprocess_text(text: str) -> str:
    """
    Pretend preprocessing step:
    - strip whitespace
    - normalize spaces
    """
    return " ".join(text.strip().split())

@app.get("/health")
def health_check() -> dict:
    logger.info("Health check requested")
    return get_service_info()

@app.post("/analyze", response_model=AnalyzeResponse)
def analyze_content(payload: AnalyzeRequest) -> AnalyzeResponse:
    raw_text = payload.content
    clean_text = preprocess_text(raw_text)

    result = analyze_text(clean_text)
    return AnalyzeResponse(**result)



