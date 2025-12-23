import logging
from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError

logger = logging.getLogger(__name__)


def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.warning(f"Validation error: {exc.errors()}")
    return JSONResponse(
        status_code=422,
        content={
            "error": "validation_error",
            "detail": exc.errors(),
        },
    )


def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
    logger.exception("Database error occurred")
    return JSONResponse(
        status_code=500,
        content={
            "error": "internal_server_error",
            "detail": "Database operation failed",
        },
    )


def generic_exception_handler(request: Request, exc: Exception):
    logger.exception("Unhandled exception")
    return JSONResponse(
        status_code=500,
        content={
            "error": "internal_server_error",
            "detail": "Unexpected server error",
        },
    )
