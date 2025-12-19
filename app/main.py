import logging
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


@app.get("/health")
def health_check() -> dict:
    logger.info("Health check requested")
    return get_service_info()
